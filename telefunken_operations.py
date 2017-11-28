import csv
import copy
import math
from scipy.special import lambertw


def get_csv_as_list(full_path):
    """Input: File path of the csv to return.
    Output: Returns list containing each row of the csv file as another list."""
    with open(full_path, "r") as f:
        reader = csv.reader(f, delimiter=",")
        csv_list = list(reader)
    return csv_list


def get_data_info_dict(the_data, hash_missing_code):
    info_dict = {}
    header = the_data[1]
    info_dict['num_resp'] = int(header[0])
    info_dict['num_coupons'] = int(header[1])
    info_dict['num_hashes'] = int(the_data[3][3 + info_dict['num_coupons']])
    info_dict['my_hash_idx'] = 4 + info_dict['num_coupons']
    info_dict['missing_code'] = header[2]
    data = []
    end_relevant_cols = info_dict['my_hash_idx'] + info_dict['num_hashes'] + 1
    # remove missing codes from friends hashes -
    # cannot remove from coupons given else getting values from each row will be very difficult
    for row in the_data[2:]:
        row_relevant = row[:end_relevant_cols]
        while hash_missing_code in row_relevant:
            row_relevant.remove(hash_missing_code)
        data.append(row_relevant)
    info_dict['data'] = data

    info_dict['all_coupons'] = get_all_coupons(info_dict)
    info_dict['all_seed_coupons'] = get_all_seed_coupons(info_dict)
    info_dict['coupon_to_seed_dict'] = get_coupon_to_seed_coupon_dict(info_dict)
    info_dict['hash_to_prob_dict'] = get_hash_to_prob_dict(info_dict)

    return info_dict


def get_entropy_of_hashes(info_dict):
    accum = 0.0
    for hash,prob in info_dict['hash_to_prob_dict'].items():
        accum += prob * math.log2(prob)
    accum *= -1.0
    return accum


def get_hashspace_size_entropy_based(info_dict):
    sz = 2.0 * math.pow(2.0, get_entropy_of_hashes(info_dict))
    return sz


def get_hashspace_size(info_dict):
    psi_S = len(info_dict['hash_to_prob_dict'])
    return psi_S**5


def get_omega(info_dict):
    S = info_dict['num_resp']
    psiS = len(set(get_all_participant_hashes(info_dict)))
    omega = (S * psiS) / (psiS * lambertw([-(math.exp(-S / psiS) * S) / psiS]) + S)
    return int(omega[0])


def get_hash_to_prob_dict(info_dict):
    hashes_list = get_all_participant_hashes(info_dict)
    hashes_count = len(hashes_list)

    hash_to_count_dict = {}
    for hash in hashes_list:
        if hash in hash_to_count_dict:
            hash_to_count_dict[hash] += 1
        else:
            hash_to_count_dict[hash] = 1

    hash_to_prob_dict = {}
    for hash,count in hash_to_count_dict.items():
        hash_to_prob_dict[hash] = count / hashes_count

    return hash_to_prob_dict


def get_coupon_to_seed_coupon_dict(info_dict):
    coupon_to_seed = {}
    for coupon in info_dict['all_coupons']:
        coupon_to_seed[coupon] = get_my_seed(coupon, info_dict)
    return coupon_to_seed


def get_all_coupons(info_dict):
    """get S"""
    all_rds_ids = []
    for row in info_dict['data']:
        all_rds_ids.append(row[2])
    return all_rds_ids


def get_all_participant_hashes(info_dict):
    all_hashes = []
    for row in info_dict['data']:
        all_hashes.append(row[info_dict['my_hash_idx']])
    return all_hashes


def get_all_hashes(info_dict):
    all_hashes = []
    for row in info_dict['data']:
        all_hashes.append(row[info_dict['my_hash_idx']])
        friends_hashes = get_my_friends_hashes(row[2], info_dict)
        all_hashes.extend(friends_hashes)
    return all_hashes


def get_all_hashes_diffseed(info_dict, seed):
    all_hashes_diffseed = []
    my_hash_idx = info_dict['my_hash_idx']
    for row in info_dict['data']:
        row_seed = info_dict['coupon_to_seed_dict'][row[2]]  # look up this row's seed
        if row_seed != seed:  # if this seed is different from my seed,
            all_hashes_diffseed.append(row[my_hash_idx])  # keep it
    return all_hashes_diffseed


def get_my_parent(coupon, info_dict):
    """get RDS parent"""
    for row in info_dict['data']:  # for each row of the data
        row_coupons = row[3:(3+info_dict['num_coupons'])]  # get the coupons given to the participant in that row
        if coupon in row_coupons:  # if my coupon is in that row, this is my parent
            return [row[2]]  # get this row's/my parent's coupon
    return []


def get_my_seed(coupon, info_dict):
    temp_seed = [coupon]  # I might be the seed
    all_seeds = info_dict['all_seed_coupons']
    while temp_seed[0] not in all_seeds:  # check if I am the seed, then continue to check my parents up my family tree
        temp_seed = get_my_parent(temp_seed[0], info_dict)  # get the next parent
    return temp_seed[0]


def get_all_seed_coupons(info_dict):
    """get D"""
    seed_coupons = copy.deepcopy(info_dict['all_coupons'])
    for potential_seed_coupon in info_dict['all_coupons']:  # for each potential seed coupon,
        for row in info_dict['data']:  # go through each row in the data,
            row_coupons = row[3:(3+info_dict['num_coupons'])]  # get the coupons given to the participant in that row
            if potential_seed_coupon in row_coupons:  # if the potential seed coupon is in that row's coupons,
                seed_coupons.remove(potential_seed_coupon)  # it is not a seed coupon, so remove it
                break
    return seed_coupons


def get_all_my_coupons(coupon, info_dict):
    """get Coupons Given"""
    my_row_index = info_dict['all_coupons'].index(coupon)
    my_row = info_dict['data'][my_row_index]
    my_coupons = my_row[3:3+info_dict['num_coupons']]
    while info_dict['missing_code'] in my_coupons:
        my_coupons.remove(info_dict['missing_code'])
    return my_coupons


def get_my_rds_story_children(coupon, info_dict):
    """get RDS Children"""
    my_coupons = get_all_my_coupons(coupon, info_dict)
    to_remove = []
    for coupon in my_coupons:
        if coupon not in info_dict['all_coupons']:  # if there is no participant with this coupon,
            to_remove.append(coupon)  # this coupon is not a child
    for coupon in to_remove:
        my_coupons.remove(coupon)
    # of the coupons I was given, return only those that are children i.e. are associated with a participant
    return my_coupons


def get_my_hash(coupon, info_dict):
    """psi"""
    my_row_index = info_dict['all_coupons'].index(coupon)  # use the list of all coupons the get this coupon's row index
    my_row = info_dict['data'][my_row_index]
    my_hash = my_row[info_dict['my_hash_idx']]
    return my_hash


def get_my_friends_hashes(coupon, info_dict):
    my_row_index = info_dict['all_coupons'].index(coupon)  # use the list of all coupons the get this coupon's row index
    my_row = info_dict['data'][my_row_index]
    #hshs_strt_idx = info_dict['my_hash_idx'] + 1
    #hshs_end_idx = hshs_strt_idx + info_dict['num_hashes']
    #my_friends_hashes = my_row[hshs_strt_idx : hshs_end_idx]
    #while info_dict['missing_code'] in my_friends_hashes:
        #my_friends_hashes.remove(info_dict['missing_code'])
    #return my_friends_hashes
    return my_row[info_dict['my_hash_idx']+1:]


def get_my_friends_inrespondents_hashes(coupon, info_dict):
    """
    Returns list of hashes that were provided by the given participant that are part of the overall participant pool"""
    friends_hashes = get_my_friends_hashes(coupon, info_dict)
    friends_inrespondents_hashes = []
    all_participant_hashes = get_all_participant_hashes(info_dict)
    # for each hash the participant provided,
    for friend_hash in friends_hashes:
        if friend_hash in all_participant_hashes:  # if that hash is in the list of all participants' hashes,
            # append it to the list of hashes that were provided by the participant
            # and are part of the overall participant pool
            friends_inrespondents_hashes.append(friend_hash)

    return friends_inrespondents_hashes


def get_coupons_by_hash(hash_code, info_dict):
    """psi_inverse (returns a list of coupons)"""
    coupon = []
    for row in info_dict['data']:
        if row[info_dict['my_hash_idx']] == hash_code:  # if this row's hash equals the hash we are looking up,
            coupon.append(row[2])  # get this row's coupon
    return coupon


def get_my_network_size(coupon, info_dict):
    """get_d"""
    my_row_index = info_dict['all_coupons'].index(coupon)  # use the list of all coupons the get this coupon's row index
    my_net_size = info_dict['data'][my_row_index][1]
    return int(my_net_size)

# This is weird as it could be negative, at least in our sample data
def get_my_non_rdsstory_net_size(coupon, info_dict):
    """get_dfree"""
    net_size = get_my_network_size(coupon, info_dict)
    parent = get_my_parent(coupon, info_dict)
    #print(parent, len(parent))
    children = get_my_rds_story_children(coupon, info_dict)
    #print(children, len(children))
    return net_size - len(parent) - len(children)


def get_harmonic_mean(info_dict):
    """get_dG_tilda"""
    net_sum = 0
    for row in info_dict['data']:
        row_net_size = int(row[1])
        net_sum += 1/row_net_size
    #print(net_sum, len(all_rds_ids))
    return info_dict['num_resp']/net_sum


def get_my_nonrdsstory_but_friends_hashes(coupon, info_dict):
    """get_R_psi
    Returns list of all hashes the given participant provided,
    without the hashes of the participant's parent and/or child(ren)"""
    my_friends_hashes = get_my_friends_hashes(coupon, info_dict)
    parent = get_my_parent(coupon, info_dict)
    children = get_my_rds_story_children(coupon, info_dict)
    family_hashes = []

    if parent:  # if I have a parent i.e. am not a seed,
        family_hashes.append(get_my_hash(parent[0], info_dict))  # append my parent's hash to my family's hashes

    if children:  # if I have children,
        for child in children:
            family_hashes.append(get_my_hash(child, info_dict))  # append each child's hash to my family's hashes
    #print(family_hashes)

    for hash in family_hashes:  # for each of my family's hashes,
        if hash in my_friends_hashes:  # if it is in the list of hashes I provided,
            my_friends_hashes.remove(hash)  # remove it from that list
    return my_friends_hashes


def get_my_nonrdsstory_inrespondents_hashes(coupon, info_dict):
    """get_M_psi
    Returns a list of hashes that were provided by the given participant,
    but are not part of the participant's family, and are part of the overall participant pool"""
    nonrdsstory_hashes = get_my_nonrdsstory_but_friends_hashes(coupon, info_dict)
    nonrdsstory_inrespondents_hashes = []
    all_participant_hashes = get_all_participant_hashes(info_dict)

    # for each hash the participant provided but that is not part of the participant's family tree,
    for nonrds_hash in nonrdsstory_hashes:
        if nonrds_hash in all_participant_hashes:  # if that hash is in the list of all participants' hashes,
            # append it to the list of hashes that were provided by the participant,
            # but are not part of the participant's family, and are part of the overall participant pool
            nonrdsstory_inrespondents_hashes.append(nonrds_hash)

    return nonrdsstory_inrespondents_hashes


def get_my_nonrdsstory_inrespondents_diffseed_hashes(coupon, info_dict):
    """get_X_psi
    Returns a list of hashes that were provided by the given participant,
    but are not part of the participant's family, and are from a participant that had a different seed"""
    # all hashes the participant provided, without those that are part of the participant's family
    nonrdsstory_hashes = get_my_nonrdsstory_but_friends_hashes(coupon, info_dict)
    # all hashes from participants that had a different seed than this participant
    all_diffseed_participant_hashes = get_all_hashes_diffseed(info_dict, get_my_seed(coupon, info_dict))
    nonrdsstory_inrespondents_diffseed_hashes = []

    # for each hash the participant provided but that is not part of the participant's family tree,
    for nonrds_hash in nonrdsstory_hashes:
        # if that hash is in the list of all participants' hashes that had a different seed,
        if nonrds_hash in all_diffseed_participant_hashes:
            # append it to the list of hashes that were provided by the participant,
            # but are not part of the participant's family, and are from a participant that had a different seed
            nonrdsstory_inrespondents_diffseed_hashes.append(nonrds_hash)

    return nonrdsstory_inrespondents_diffseed_hashes


def init_operations(filepath, hash_missing_code):
    the_data = get_csv_as_list(filepath)
    info_dict = get_data_info_dict(the_data, hash_missing_code)
    return info_dict


def run_all_on_csv():
    coupon = '1010'
    seed = '1001'
    hash_code = 'x4'
    #info_dict = init_operations()
    #print(info_dict['data'])
    #print(get_coupon_to_seed_coupon_dict(info_dict))
    #print(get_all_coupons(info_dict))
    #print(get_all_participant_hashes(info_dict))
    #print(get_all_hashes_diffseed(info_dict, seed))
    #print(get_my_parent(coupon, info_dict))
    #print(get_my_seed(coupon, info_dict))
    #print(get_all_seed_coupons(info_dict))
    #print(get_all_my_coupons(coupon, info_dict))
    #print(get_my_rds_story_children(coupon, info_dict))
    #print(get_my_hash(coupon, info_dict))
    #print(get_my_friends_hashes(coupon, info_dict))
    #print(get_coupons_by_hash(hash_code, info_dict))
    #print(get_my_network_size(coupon, info_dict))
    #print(get_my_non_rdsstory_net_size(coupon, info_dict))
    #print(get_harmonic_mean(info_dict))
    #print(get_my_nonrdsstory_but_friends_hashes(coupon, info_dict))
    #print(get_my_nonrdsstory_inrespondents_hashes(coupon, info_dict))
    #print(get_my_nonrdsstory_inrespondents_diffseed_hashes(coupon, info_dict))
