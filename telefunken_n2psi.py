import telefunken_operations as t


def get_new_N_guess(data_dict, Dtilde, N, omega, S, Ds):
    Rs = []
    Xpsis = []
    denominator = 0
    # numerator and denominator
    for coupon in data_dict['all_coupons']:  # for each coupon/participant in the sample,
        # numerator
        # get the hashes that the participant provided that are not part of the participant's family
        Rs.extend(t.get_my_nonrdsstory_but_friends_hashes(coupon, data_dict))
        # denominator
        # get the hashes that the participant provided that are not part of the participant's family
        # but are part of the participant pool
        Xpsis.extend(t.get_my_nonrdsstory_inrespondents_hashes(coupon, data_dict))

    numerator = S * len(Rs) * (Ds - 1) / Dtilde

    # denominator
    for hash in Xpsis:
        # get all the coupons with that hash code
        Sy = t.get_coupons_by_hash(hash, data_dict)
        for coupon in Sy:
            Z1 = (N - 1) / omega
            Z2 = Dtilde / (t.get_my_network_size(coupon, data_dict) - 1)
            denominator += 1 / (Z1 * Z2 + 1)

    if denominator == 0:
        return "Estimation failed because number of matches was 0"
    else:
        return numerator / denominator


def run_telefunken(data_dict, omega, N=1000, max_iterations=1000):
    Dtilde = t.get_harmonic_mean(data_dict)
    S = data_dict['num_resp']

    sum_net_size = 0
    for row in data_dict['data']:
        sum_net_size += int(row[1])
    Ds = sum_net_size / S

    converged = False
    counter = 0
    while not converged:
        counter += 1
        new_N = get_new_N_guess(data_dict, Dtilde, N, omega, S, Ds)
        if abs(N - new_N) < 0.1 or counter > max_iterations:
            converged = True
        N = new_N
        #print(N)

    return round(N)
