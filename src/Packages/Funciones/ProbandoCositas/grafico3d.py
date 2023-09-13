import matplotlib.pyplot as plt
import numpy as np


ax = plt.axes(projection='3d')

# Data for a three-dimensional line
zline = np.linspace(0, 15, 100)
print(len(zline))

xline = np.sin(zline)
print(len(xline))

yline = np.cos(zline)
print(len(yline))

ax.plot3D(xline, yline, zline, 'gray')


plt.show()