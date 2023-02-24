import numpy as np
import math
# import matplotlib.pyplot as plt
from scipy import interpolate
import ctypes

lib = ctypes.cdll.LoadLibrary('racing_track_generator/libConsoleDrawRacingTrack.so')
my_c_function = lib.my_c_function
my_c_function.argtypes = [ctypes.POINTER(ctypes.POINTER(ctypes.c_double)), ctypes.c_int, ctypes.c_int, ctypes.c_int]


# init vars
error = 20
x_initial = 1
y_initial = 1
r0 = 30
count = 1
x_sets = []
y_sets = []
for i in range(count):
    # get angle from 0 to 2pi
    alpha = np.linspace(0, 2 * math.pi, 15, endpoint=False)

    # slightly randomise the "radius"
    r = r0 + error * np.random.random(len(alpha))

    # plot point of circle where radius of the circle is randomised
    x = x_initial + r * np.cos(alpha)
    y = y_initial + r * np.sin(alpha)

    # add more noise
    noise_std = 6

    # use numpy normal distribution function to add noise
    x += np.random.normal(0, noise_std, len(x))
    y += np.random.normal(0, noise_std, len(y))

    # create copies of x,y for plotting
    x_copy = np.copy(x)
    y_copy = np.copy(y)

    # append start point to end of np list
    x_copy = np.append(x_copy, x_copy[0])
    y_copy = np.append(y_copy, y_copy[0])

    # spline magic
    tck,t = interpolate.splprep([x_copy,y_copy], s=0, per=1)
    x_sets.append(x_copy)
    y_sets.append(y_copy)

    # save arrays to a file
    arr = np.column_stack((x, y))
    # Get a pointer to the array data
    arr_ptr = arr.ctypes.data_as(ctypes.POINTER(ctypes.POINTER(ctypes.c_double)))

    # Call the C++ function with the pointer and the array size
    my_c_function(arr_ptr, arr.shape[0], arr.shape[1], i)
    
    








# param for spline
# t_vals = np.linspace(0, 1, 1000)

# # points of spline
# x_spline, y_spline = interpolate.splev(t_vals, tck)

# # ignore last point
# x_spline = x_spline[:-1]
# y_spline = y_spline[:-1]



# plt.figure()
# plt.plot(x_copy, y_copy, 'o', x_copy, y_copy, 'b')
# plt.plot(x, y, 'o', x_spline, y_spline)
# plt.show()