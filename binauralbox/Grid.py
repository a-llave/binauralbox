"""
Description: Grid class

Author: Adrien Llave - CentraleSupelec
Date: 28/03/2018

Version: 1.1

Date    | Auth. | Vers.  |  Comments
18/03/28  ALl     1.0       Initialization
18/12/03  ALl     1.1       Code factorization

TODO: Add lateral-polar coordinates system

"""

import numpy as np
import utils_llave as u


class Grid:
    def __init__(self, norm_s=None, coords_m=None):
        """

        :param norm_s: coordinates norm ('cartesian', 'spherical_1')
        :param coords_m: <Nx3> [x, y, z] [radius, azimuth, elevation]
        """
        self.norm_s = norm_s
        self.coords_m = coords_m

    def convert_coordinates(self, new_norm_s):

        if self.norm_s == new_norm_s:
            return

        if self.norm_s == 'cartesian':
            if new_norm_s == 'spherical_1':
                self.coords_m[:, 0], self.coords_m[:, 1], self.coords_m[:, 2] = u.cart2sph(self.coords_m[:, 0][np.newaxis, :],
                                                                                           self.coords_m[:, 1][np.newaxis, :],
                                                                                           self.coords_m[:, 2][np.newaxis, :])
            else:
                print('Unknown coordinates norm')
        elif self.norm_s == 'spherical_1':
            if new_norm_s == 'cartesian':
                self.coords_m[:, 0], self.coords_m[:, 1], self.coords_m[:, 2] = u.sph2cart(self.coords_m[:, 0],
                                                                                           self.coords_m[:, 1],
                                                                                           self.coords_m[:, 2])
            else:
                print('Unknown coordinates norm')
        else:
            print('Unknown coordinates norm')

        self.norm_s = new_norm_s
        return

    def find_closest_point(self, point_v, norm_s, nb_out_point_n=1):

        oldnorm_s = self.norm_s
        self.convert_coordinates(new_norm_s='cartesian')
        tmppoint_v = np.copy(point_v)
        if norm_s == 'spherical_1':
            tmppoint_v[0, 0], tmppoint_v[0, 1], tmppoint_v[0, 2] = u.sph2cart(tmppoint_v[0, 0], tmppoint_v[0, 1], tmppoint_v[0, 2])
        elif norm_s == 'cartesian':
            pass
        else:
            print('Unknown coordinates norm')

        tmp_m = self.coords_m - tmppoint_v
        dist_v = np.linalg.norm(tmp_m, axis=1)
        idx = np.argmin(dist_v)
        closest_point_v = np.array(self.coords_m[idx, :])[np.newaxis, :].T
        if norm_s == 'spherical_1':
            closest_point_v[0], \
            closest_point_v[1], \
            closest_point_v[2] = u.cart2sph(closest_point_v[0][:, np.newaxis],
                                            closest_point_v[1][:, np.newaxis],
                                            closest_point_v[2][:, np.newaxis])
        elif norm_s == 'cartesian':
            pass
        else:
            print('Unknown coordinates norm')

        self.convert_coordinates(new_norm_s=oldnorm_s)
        return closest_point_v[:, 0], idx, dist_v[idx]

    def get_spherical_weighting_harder(self, grid, nb_dz=10000):
        # PREPARE
        uni_az_v = np.unique(grid.coords_m[:, 1])
        uni_el_v = np.unique(grid.coords_m[:, 2])

        # AVOID MODULO ISSUE
        uni_az_bound_v = np.concatenate((uni_az_v[len(uni_az_v)-1][np.newaxis, np.newaxis] - 360,
                                         uni_az_v[:, np.newaxis],
                                         uni_az_v[0][np.newaxis, np.newaxis] + 360),
                                        axis=0)
        uni_el_bound_v = np.concatenate((uni_el_v[len(uni_el_v)-1][np.newaxis, np.newaxis] - 360,
                                         uni_el_v[:, np.newaxis],
                                         uni_el_v[0][np.newaxis, np.newaxis] + 360),
                                        axis=0)

        nb_dir = len(grid.coords_m[:, 1])
        nb_az = len(uni_az_bound_v)
        nb_el = len(uni_el_bound_v)

        # ELEVATION(EQ 10.3)
        dz = 2 / nb_dz
        zz_v = np.linspace(-1, 1, nb_dz)
        Sel_v = np.zeros((nb_el,))
        for id_el in range(1, nb_el-1):
            u_f = np.sin(np.deg2rad(uni_el_bound_v[id_el] + uni_el_bound_v[id_el + 1]) / 2)
            l_f = np.sin(np.deg2rad(uni_el_bound_v[id_el] + uni_el_bound_v[id_el - 1]) / 2)
            mask_b = np.logical_and(zz_v > l_f, zz_v < u_f)
            segment_v = zz_v[mask_b]

            Sel_v[id_el] = np.sum(2 * np.pi * np.sqrt(1 - segment_v**2) * np.sqrt(1 + (-segment_v / np.sqrt(1 - segment_v**2))**2) * dz)

        # COMPUTE SURFACE AREA(EQ 10.4)
        Sea_m = np.zeros((nb_az, nb_el))
        for id_el in range(nb_el):
            for id_az in range(1, nb_az-1):
                Sea_m[id_az, id_el] = np.deg2rad(uni_az_bound_v[id_az+1] - uni_az_bound_v[id_az-1]) / (4 * np.pi) * Sel_v[id_el]
        Sea_m = Sea_m[1:Sea_m.shape[0]-1, 1:Sea_m.shape[0]-1]

        # VECTORIZE IT TO CORRESPOND TO THE GRID STRUCT
        Sea_v = np.zeros((nb_dir,))
        for dd in range(nb_dir):
            id_az = np.where(uni_az_v == grid.coords_m[dd, 1])
            id_el = np.where(uni_el_v == grid.coords_m[dd, 2])
            Sea_v[dd] = Sea_m[id_az, id_el]

        weight_v = Sea_v / (4 * np.pi)
        weight_v = weight_v / np.sum(weight_v)
        return weight_v
