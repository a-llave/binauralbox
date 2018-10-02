
def is_hrtfdata(hrtfdata, verbose_b=False):
    check_test = True
    attribute_list = ['type_s', 'fs_f', 'azim_v', 'elev_v', 'dist_v', 'data_m', 'xaxis_v', 'comments', 'ear_side']

    if not isinstance(hrtfdata, object):
        check_test = False
        if verbose_b:
            print('is_hrtfdata: input argument is not a object')

    for attribute in attribute_list:
        if not hasattr(hrtfdata, attribute):
            check_test = False
            if verbose_b:
                print('is_hrtfdata: input argument has no attribute '+attribute)

    return check_test
