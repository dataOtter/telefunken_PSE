import telefunken_operations as t


def get_new_N_guess(data_dict, Dtilde, N, omega, S):
    Rs = []
    Xpsis = []
    denominator = 0
    # numerator & denominator
    # for each participant in the sample,
    for coupon in data_dict['all_coupons']:
        # numerator
        # get all hashes provided by this participant
        Rs.extend(t.get_my_friends_hashes(coupon, data_dict))
        #denominator
        # get all hashes provided by the participant that also exist in the sample
        Xpsis.extend(t.get_my_friends_inrespondents_hashes(coupon, data_dict))

    numerator = S * len(Rs)

    # denominator
    for hash in Xpsis:
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

    converged = False
    counter = 0
    while not converged:
        counter += 1
        new_N = get_new_N_guess(data_dict, Dtilde, N, omega, S)
        if abs(N - new_N) < 0.1 or counter > max_iterations:
            converged = True
        N = new_N
        #print(N)

    return round(N)
