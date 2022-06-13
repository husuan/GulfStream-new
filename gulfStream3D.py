# This script takes a snapshot of sea-surface height and makes a
# 3D visualisation of the data.


import matplotlib


import numpy as np
import matplotlib.pyplot as plt
import scipy.io as sio
import pandas as pd

from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm

########## Prepare data ##########

# load data
adt = np.transpose( sio.loadmat('data/adt.mat')['adt_all'], (1,0,2) )

# choose day to visualise
t0 = 100
snapshot = np.squeeze( adt[:,:,t0] )

# change land values
adt[ np.isnan( adt ) ] = -0.5

# define lon and lat
lon, lat = np.linspace(-80,-50,121), np.linspace(30,50,81)
lon, lat = np.meshgrid( lon, lat )

########## Plotting #########

fig = plt.figure( figsize=(11,6) )
ax3D = fig.add_subplot( 111, projection='3d' )

# make custom palette
cMap = cm.bone
cMap.set_under( 'saddlebrown' )

# draw surface
surf3D = ax3D.plot_surface( lon[:-1,:-1], lat[:-1,:-1], snapshot, cmap=cMap, vmin=-0.4, vmax=1.5 )

# tidy up
ax3D.set_zlim( (-1.5,8) )
ax3D.set_xlim( (-80,-50) )
ax3D.set_ylim( (30,50) )

ax3D.set_xticks( [-75,-70,-65,-60,-55] )
ax3D.set_xticklabels( ['75$^\circ$','70$^\circ$','65$^\circ$','60$^\circ$','55$^\circ$'] )
ax3D.set_yticks( [32,36,40,44,48] )
ax3D.set_yticklabels( ['32$^\circ$','36$^\circ$','40$^\circ$','44$^\circ$','48$^\circ$'])

ax3D.xaxis.set_tick_params( labelsize=12 )
ax3D.yaxis.set_tick_params( labelsize=12 )
ax3D.zaxis.set_tick_params( labelsize=12 )

ax3D.set_ylabel('Latitude')
ax3D.set_xlabel('Longitude')
ax3D.set_zlabel('Height')

# add colorbar
cBar = fig.colorbar( surf3D, extend='both' )
cBar.set_label('Sea surface heigt (m)', fontsize=12 )

# change 'camera' position
ax3D.view_init( elev=30, azim=-150 )


plt.savefig( 'gulfStreamSSH3D_snapshot.png', format='png', dpi=800 )

plt.show()