import telefunken_operations as t


def get_new_N_guess(D, data_dict, Dtilde, N, omega):
    numerator, denominator = 0, 0

    # numerator and denominator
    for seed_rds_id in D:  # for each seed coupon in the sample:
        # numerator
        Dsx_num = 0  # cumulative network size of everyone whose seed IS NOT the current seed_rds_id
        Sx = 0  # number of coupons whose seed IS NOT the current seed_rds_id
        Rs = []  # to get hashes of "friends not in rds story" of everyone whose seed IS the current seed_rds_id

        # denominator
        Xpsis = []

        for rds_id in data_dict['all_coupons']:  # for each coupon in the sample:
            # numerator
            my_seed = data_dict['coupon_to_seed_dict'][rds_id]  # get the coupon's seed

            # numerator
            if my_seed != seed_rds_id:  # if the coupon's seed IS NOT the current seed coupon in the sample
                Dsx_num += t.get_my_network_size(rds_id, data_dict)  # cumulatively add network size of these coupons
                Sx += 1  # count these coupons

            # numerator and denominator
            elif my_seed == seed_rds_id:  # if the coupon's seed IS the current seed coupon in the sample
                # numerator
                # get hashes of the coupon's "friends who are not in these coupons' rds story"
                Rs.extend(t.get_my_nonrdsstory_but_friends_hashes(rds_id, data_dict))

                # denominator
                # get hash codes of those friends of thia coupon who were not in this coupon's RDS story
                # but are respondents in the sample, and whose seed is different from this coupon's seed
                Xpsis.extend(t.get_my_nonrdsstory_inrespondents_diffseed_hashes(rds_id, data_dict))

        # numerator
        Dsx = Dsx_num/Sx  # average network size of everyone whose seed IS NOT the current seed_rds_id

        numerator += Sx * len(Rs) * (Dsx - 1) / Dtilde

        # denominator
        for hash_code in Xpsis:  # for each hash code in Xpsis (see explanation above):
            Sy = t.get_coupons_by_hash(hash_code, data_dict)  # get all coupon's with that hash code
            for rds_id in Sy:  # for each of those coupons:
                my_seed = data_dict['coupon_to_seed_dict'][rds_id]  # get the coupon's seed
                if my_seed != seed_rds_id:   # if the coupon's seed IS NOT the current seed coupon in the sample
                    Z1 = (N - 1.0) / omega
                    Z2 = Dtilde / (t.get_my_network_size(rds_id, data_dict) - 1.0)
                    denominator += 1.0 / ((Z1 * Z2) + 1.0)

    if denominator == 0:
        return "Estimation failed because number of matches was 0"
    else:
        return numerator / denominator


def run_telefunken(filepath, omega=256000, N=1000, max_iterations=1000, hash_missing_code='NA'):
    data_dict = t.init_operations(filepath, hash_missing_code)
    D = data_dict['all_seed_coupons']
    Dtilde = t.get_harmonic_mean(data_dict)

    #omega = t.get_hashspace_size(data_dict)

    converged = False
    counter = 0
    while not converged:
        counter += 1
        new_N = get_new_N_guess(D, data_dict, Dtilde, N, omega)
        if abs(N - new_N) < 0.1 or counter > max_iterations:
            converged = True
        N = new_N
        print(N)

    return round(N, 2)
