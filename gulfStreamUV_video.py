# This script takes velocity data within the Gulf Stream and makes a video of 
# of the flow evolving. The data is from AVISO satellite altimetry data.

import matplotlib
matplotlib.use("TkAgg")

import numpy as np
import matplotlib.pyplot as plt
import scipy.io as sio
import pandas as pd

from matplotlib.cm import get_cmap
import matplotlib.animation as manimation

# uncomment this line if you want to see the plots as they are saved
#plt.ion()

########## Prepare data ##########

data = sio.loadmat('data/uv.mat')

u = np.transpose( data['u_all'], (1,0,2) )
v = np.transpose( data['v_all'], (1,0,2) )

lon, lat = np.linspace( -80, -50, 121 ), np.linspace( 30, 50, 81 )

speed = np.sqrt( np.square( u, u ) + np.square( v, v ) )

# make a land mask (from nan values)
landMask = np.squeeze( speed[:,:,100] )
landMask[ ~np.isnan( landMask ) ] = 0
landMask[ np.isnan( landMask ) ] = 1
landMask[ landMask == 0 ] = np.nan

lon1 = lon[:-1]
lat1 = lat[:-1]
lonGrid, latGrid = np.meshgrid( lon1, lat1 )

# define ADT spacings for contourf function and the datelist for title
adtSpacings = np.linspace( -1.2, 1.2, num=13 )
dateList = pd.date_range( '1993-01-01', periods=u.shape[2], freq='D' ).tolist()

########## Make video ##########

fig = plt.figure( figsize=(12,8) )

# quiver sub-sampling
n = 1

FFMpegWriter = manimation.writers['ffmpeg']
metadata = dict( title='Gulf Stream UV', artist='Tom Bolton', comment='Gulf Stream Visualization of AVISO UV data.' )
writer = FFMpegWriter( fps=24, metadata=metadata, bitrate=30000, codec='libx264' )

with writer.saving( fig, "gulfStreamUV.gif", 100 ) :

    for t in range(1, 31, 1):

        print (t)


        # make quiver plt
        plt.quiver( lon1[::n], lat1[::n], u[::n,::n,t], v[::n,::n,t], speed[::n,::n,t], cmap='hot', clim=(0,1.6) )

        # add land
        plt.contourf(lonGrid, latGrid, landMask, cmap='Greys')
        
        # plot title
        titleString = str(dateList[t])
        titleString = titleString[0:10]
        plt.title( "Velocity field    " + titleString, fontsize=20 )

        # tidy up the axis
        ax = plt.gca()

        ax.set_xticks( [-75,-70,-65,-60,-55] )
        ax.set_xticklabels( ['75$^\circ$', '70$^\circ$', '65$^\circ$', '60$^\circ$', '55$^\circ$' ] )
        plt.xticks( fontsize=15 )

        ax.set_yticks( [32,36,40,44,48] )
        ax.set_yticklabels( ['32$^\circ$','36$^\circ$','40$^\circ$','44$^\circ$','48$^\circ$' ] )
        plt.yticks( fontsize=15 )

        # save this figure as a frame
        plt.pause(0.1)
        writer.grab_frame()

        # clear the axis data so it doesn't accumulate
        plt.cla()
