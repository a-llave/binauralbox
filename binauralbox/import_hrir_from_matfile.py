from .HrtfData import *


def import_hrir_from_matfile(filename_s):
    """

    :param filename_s:
    :return:
    """
    print('LOAD HRIR MAT-FILE: ' + filename_s)
    if os.path.isfile(filename_s):
        raw_data = sio.loadmat(filename_s)
        fs_f = int(raw_data['Fs'][0][0])
        hl = HrtfData(fs_f=fs_f,
                      type_s='time',
                      azim_v=raw_data['coords'][:, 1],
                      elev_v=raw_data['coords'][:, 2],
                      dist_v=raw_data['coords'][:, 0],
                      data_m=raw_data['hl'],
                      comments=raw_data['comments'],
                      ear_side='left')

        hr = HrtfData(fs_f=fs_f,
                      type_s='time',
                      azim_v=raw_data['coords'][:, 1],
                      elev_v=raw_data['coords'][:, 2],
                      dist_v=raw_data['coords'][:, 0],
                      data_m=raw_data['hr'],
                      comments=raw_data['comments'],
                      ear_side='right')
    else:
        print('WARNING: ' + filename_s + 'DOES NOT EXIST')
        hl = HrtfData(ear_side='left')
        hr = HrtfData(ear_side='right')
    return hl, hr
