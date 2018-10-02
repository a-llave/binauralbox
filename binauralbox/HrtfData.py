import numpy as np
import copy
import os
import scipy.io as sio
from binauralbox.Grid import *


class HrtfData:
    def __init__(self,
                 fs_f=16000,
                 type_s='time',
                 azim_v=np.array([0.0]),
                 elev_v=np.array([0.0]),
                 dist_v=np.array([1.0]),
                 data_m=np.concatenate((np.array([1.0])[np.newaxis, :].T, np.zeros((1, 127))), axis=1),
                 comments='',
                 ear_side='left'):
        """
        Constructor
        """

        # CHECK
        assert azim_v.shape == elev_v.shape == dist_v.shape, 'azim_v, elev_v and dist_v have to have the same shape'
        assert azim_v.shape[0] == data_m.shape[0], 'azim_v and data_m have to have the same number of lign'

        # CONSTRUCTOR
        self.type_s = type_s
        self.fs_f = fs_f
        self.azim_v = azim_v
        self.elev_v = elev_v
        self.dist_v = dist_v
        self.data_m = data_m
        self.xaxis_v = np.linspace(0, self.data_m.shape[1], self.data_m.shape[1])
        self.comments = comments
        self.ear_side = ear_side

        self.update_xaxis()

    def import_hrir_from_matfile(self, filename_s, ear_side='left'):
        """

        :param filename_s:
        :param ear_side:
        :return:
        """
        print('LOAD HRIR MAT-FILE: ' + filename_s)
        if os.path.isfile(filename_s):
            raw_data = sio.loadmat(filename_s)
            self.type_s = 'time'
            assert raw_data['Fs'] == self.fs_f, \
                'The initial sampling rate and the imported HRIR set sampling rate must be the same'
            self.fs_f = raw_data['Fs']
            self.azim_v = raw_data['coords'][:, 1]
            self.elev_v = raw_data['coords'][:, 2]
            self.dist_v = raw_data['coords'][:, 0]
            if ear_side == 'left':
                self.data_m = raw_data['hl']
                self.ear_side = 'left'
            elif ear_side == 'right':
                self.data_m = raw_data['hr']
                self.ear_side = 'right'
            else:
                print('Ear side have to be ''left'' or ''right''')
            self.update_xaxis()
        else:
            print('WARNING: ' + filename_s + 'DOES NOT EXIST')
        return

    def time2freq(self, num_freq_n=None):
        """
        Conversion of self.data_m from time domain to frequency domain
        :param num_freq_n:
        :return:
        """

        if self.type_s == 'time':
            self.type_s = 'freq'
            self.data_m = np.fft.fft(self.data_m, (num_freq_n - 1) * 2)
            self.data_m = self.data_m[:, 0:num_freq_n]
        else:
            # info('Unvalid type')
            pass

        self.update_xaxis()

        return

    def freq2time(self, num_sample_n=None):
        """
        Conversion of self.data_m from frequency domain to time domain
        """
        if self.type_s == 'freq':
            self.type_s = 'time'
            self.data_m = np.concatenate((self.data_m, np.conj(np.fliplr(self.data_m[1:self.data_m.shape[1]]))), axis=1)
            self.data_m = np.fft.ifft(self.data_m, num_sample_n)
        else:
            # info('Unvalid type')
            pass

        self.update_xaxis()

        return

    def update_xaxis(self):
        """
        Update the time axis or freq axis according to the data type
        Useful for plot data
        """
        num_sample_n = self.data_m.shape[1]

        if self.type_s == 'time':
            self.xaxis_v = np.linspace(0., float(num_sample_n / self.fs_f), num=num_sample_n)
        elif self.type_s == 'freq':
            self.xaxis_v = np.linspace(0., float(self.fs_f / 2.), num=num_sample_n)
        else:
            # info('Unvalid type')
            pass

        return

    def subset(self, grid_target):
        grid = self.get_grid(norm_s='cartesian')
        subgrid = Grid(norm_s='cartesian', coords_m=np.zeros((grid_target.coords_m.shape[0], 3)))
        idx_v = np.zeros((grid_target.coords_m.shape[0],), dtype=np.int16)
        for dd in range(grid_target.coords_m.shape[0]):
            subgrid.coords_m[dd, :], idx_v[dd], trash = grid.find_closest_point(
                point_v=grid_target.coords_m[dd, :][np.newaxis],
                norm_s=grid_target.norm_s)

        data_subset = copy.copy(self)
        data_subset.data_m = data_subset.data_m[idx_v, :]
        data_subset.dist_v = data_subset.dist_v[idx_v]
        data_subset.azim_v = data_subset.azim_v[idx_v]
        data_subset.elev_v = data_subset.elev_v[idx_v]

        return data_subset

    def get_grid(self, norm_s='spherical_1'):
        """

        :param norm_s: coordinates norm 'cartesian', 'spherical_1'
        :return: Grid object corresponding to the HRTF set
        """
        grid = Grid(norm_s='spherical_1')
        grid.coords_m = np.zeros((self.dist_v.shape[0], 3))
        grid.coords_m[:, 0] = self.dist_v
        grid.coords_m[:, 1] = self.azim_v
        grid.coords_m[:, 2] = self.elev_v

        grid.convert_coordinates(new_norm_s=norm_s)

        return grid
