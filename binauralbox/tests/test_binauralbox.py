import numpy as np
import src.pkg.binauralbox as bbox
import matplotlib.pyplot as plt
import pyaudio
import src.pkg.RTAudioProc as rt
import time


# ----------------------------------------------------------------
def callback(in_data, frame_count, time_info, status):
    # INPUT DECODING
    npdata_in = rt.decode(in_data, nb_channels)
    # BINAURALIZER
    npdata_in = np.tile(npdata_in[:, 0], (2, 1)).T
    npdata_out = bino.process(npdata_in)
    # OUTPUT ENCODING
    data = rt.encode(npdata_out)

    return data, pyaudio.paContinue


# ----------------------------------------------------------------
nb_channels = 2
samp_freq = 44100
nb_bufsamp = 20

p = pyaudio.PyAudio()

filename_s = '../resources/HATS44100_BnK.mat'
filename2_s = '../resources/HATS44100_BTEback.mat'

# CALL OBJ HRTF DATA
l_hrtf = bbox.HrtfData(fs_f=samp_freq)
r_hrtf = bbox.HrtfData(fs_f=samp_freq)
l_hrtf2 = bbox.HrtfData(fs_f=samp_freq)
r_hrtf2 = bbox.HrtfData(fs_f=samp_freq)

# IMPORT HRTF DATA
l_hrtf.import_hrir_from_matfile(filename_s, ear_side='left')
r_hrtf.import_hrir_from_matfile(filename_s, ear_side='right')
l_hrtf2.import_hrir_from_matfile(filename_s, ear_side='left')
r_hrtf2.import_hrir_from_matfile(filename_s, ear_side='right')


grid = l_hrtf.get_grid(norm_s='spherical_1')

l_hrtf.data_m = l_hrtf.data_m / 1.
r_hrtf.data_m = r_hrtf.data_m / 1.

point_v = np.array([1., 0., 0.])

closestpoint_v, idx, trash = grid.find_closest_point(point_v=point_v, norm_s='spherical_1')

print('---------------')
print('target point coordinates', point_v)
print('closest point coordinates', closestpoint_v)
print('index closest point', grid.coords_m[idx, :])

#  PLOT
# fig, ax = plt.subplots()
# ax.plot(l_hrtf.xaxis_v, l_hrtf.data_m[idx, :])
# ax.plot(r_hrtf.xaxis_v, r_hrtf.data_m[idx, :])
# ax.set(xlabel='time (s)', ylabel='Magnitude',
#        title='my HRIR')
# ax.grid()
# plt.show()


# CALL BINAURALIZER
bino = bbox.RTBinauralizer(l_hrtf=l_hrtf, r_hrtf=r_hrtf, nb_bufsamp=nb_bufsamp)

grid_target = bbox.Grid(norm_s='spherical_1',
                        coords_m=np.array([1., l_hrtf.azim_v[idx], l_hrtf.elev_v[idx]])[np.newaxis, :])
bino.update_positions(grid_target=grid_target)

# STREAM
stream = p.open(format=pyaudio.paInt16,
                channels=nb_channels,
                rate=samp_freq,
                input=True,
                output=True,
                input_device_index=16,
                output_device_index=16,
                frames_per_buffer=nb_bufsamp,
                stream_callback=callback)

stream.start_stream()

hrtfset_n = 0
theta = 0.
grid_target = bbox.Grid(norm_s='spherical_1',
                        coords_m=np.array([1., theta, 0.])[np.newaxis, :])


while stream.is_active():
    theta = np.mod(theta - 5., 360)
    grid_target.coords_m[0, 1] = theta
    bino.update_positions(grid_target=grid_target)
    if theta == 0.:
        if hrtfset_n == 0:
            print('go to second')
            bino.update_hrir(l_hrtf2, r_hrtf2)
            hrtfset_n = 1
        else:
            print('go to first')
            bino.update_hrir(l_hrtf, r_hrtf)
            hrtfset_n = 0
    time.sleep(0.1)

stream.stop_stream()
stream.close()

p.terminate()







