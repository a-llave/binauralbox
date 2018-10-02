%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
% Description   Unitary test for import/export Hrtf data pipeline of Python
%               binauralbox
%
% Author        A. Llave - CentraleSupélec
%
% Date          24 July 2018
%
% Version       1.0
%
%
%   History
% Date      Author  Version     Content
% 18/07/24  ALl     1.0         Initialization
%
    %----------------------------------------------------------------------
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

clear all
close all
clc

dao = hm.dao.HrirDAO();

path_s = 'D:\MATLAB\database_HA_HRTF';
filename_inp_s = [ path_s filesep 'hrir48000_6.mat'];
filename_inp2_s = [ path_s filesep 'hrir48000_6_test.mat'];

[hl, hr] = dao.getHRIRsFromFilename( filename_inp_s );
[hl2, hr2] = dao.getHRIRsFromFilename( filename_inp_s );

fs_eq_l = ~isequal(hl.fs, hl2.fs)
hrir_eq_l = ~isequal(hl.hrir, hl2.hrir)
azim_eq_l = ~isequal(hl.phis, hl2.phis)
elev_eq_l = ~isequal(hl.thetas, hl2.thetas)
dist_eq_l = ~isequal(hl.radii, hl2.radii)

fs_eq_r = ~isequal(hr.fs, hr2.fs)
hrir_eq_r = ~isequal(hr.hrir, hr2.hrir)
azim_eq_r = ~isequal(hr.phis, hr2.phis)
elev_eq_r = ~isequal(hr.thetas, hr2.thetas)
dist_eq_r = ~isequal(hr.radii, hr2.radii)

disp('LEFT CHECK (0 expected)')
sum(fs_eq_l + hrir_eq_l + azim_eq_l + elev_eq_l + dist_eq_l)

disp('RIGHT CHECK (0 expected)')
sum(fs_eq_r + hrir_eq_r + azim_eq_r + elev_eq_r + dist_eq_r)


