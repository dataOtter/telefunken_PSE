import telefunken_n3psi as t3
import telefunken_n2psi as t2
import telefunken_n1psi as t1
import telefunken_operations as to


def run_selected_formulas(filepath, selected_formulas: list, hash_missing_code='NA'):
    data_dict = to.init_operations(filepath, hash_missing_code)
    omega = to.get_omega(data_dict)
    results_dict = {'omega': omega}

    for selection in selected_formulas:
        if int(selection) == 1:
            results_dict[selection] = t1.run_telefunken(data_dict, omega)
        elif int(selection) == 2:
            results_dict[selection] = t2.run_telefunken(data_dict, omega)
        elif int(selection) == 3:
            results_dict[selection] = t3.run_telefunken(data_dict, omega)
        else:
            results_dict[selection] = 'Internal error. Please try again or contact admin.'

    return results_dict
