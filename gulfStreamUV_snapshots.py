# This script takes velocity data from within the Gulf Stream and makes
# a stream plot.

import numpy as np
import matplotlib.pyplot as plt
import scipy.io as sio


########## Prepare data ##########

data = sio.loadmat('data/uv.mat')

u = np.transpose( data['u_all'], (1,0,2) )
v = np.transpose( data['v_all'], (1,0,2) )

lon, lat = np.linspace( -80, -50, 121 ), np.linspace( 30, 50, 81 )

lon1 = lon[:-1]
lat1 = lat[:-1]

speed = np.sqrt( np.square( u, u ) + np.square( v, v ) )

# make a land mask (from nan values)
landMask = np.squeeze( speed[:,:,100] )
landMask[ ~np.isnan( landMask ) ] = 0
landMask[ np.isnan( landMask ) ] = 1
landMask[ landMask == 0 ] = np.nan

lonGrid, latGrid = np.meshgrid( lon1, lat1 )

#lonLand, latLand = lonGrid[ np.isnan( landMask ) ], latGrid[ np.isnan( landMask ) ]
#land = landMask[ np.isnan( landMask ) ]
#land = 1

########## Plotting ##########

# prepare subplots
fig, axArr = plt.subplots(2,2, sharex=True, sharey=True )
fig.set_size_inches( (11,8) )

# sub-sampling rate for quiver
n=1

# choose which day to plot
t0 = 1


# use each method
im0 = axArr[0,0].pcolor( lon[:-1], lat[:-1], speed[:,:,t0], cmap='hot', vmin=0, vmax=1.6 )
im1 = axArr[0,1].contourf( lon[:-1], lat[:-1], speed[:,:,t0], cmap='hot', vmin=0, vmax=1.6 )
im2 = axArr[1,0].quiver( lon1[::n], lat1[::n], u[::n,::n,t0], v[::n,::n,t0], speed[::n,::n,t0], cmap='hot', clim=(0,1.6) )
im3 = axArr[1,1].streamplot( lon[:-1], lat[:-1], u[:,:,t0], v[:,:,t0], color=speed[:,:,t0],
                             density=[7,7], cmap='hot', linewidth=2*speed[:,:,t0], arrowsize=0.5 )

# add land to each plot
axArr[0,0].contourf( lonGrid, latGrid, landMask, cmap='Greys' )
axArr[0,1].contourf( lonGrid, latGrid, landMask, cmap='Greys' )
axArr[1,0].contourf( lonGrid, latGrid, landMask, cmap='Greys' )
axArr[1,1].contourf( lonGrid, latGrid, landMask, cmap='Greys' )

# polish each plot
axArr[0,0].set_ylim( (30,50) )
axArr[0,1].set_ylim( (30,50) )
axArr[1,0].set_ylim( (30,50) )
axArr[1,1].set_ylim( (30,50) )

axArr[0,0].set_xlim( (-80,-50) )
axArr[0,1].set_xlim( (-80,-50) )
axArr[1,0].set_xlim( (-80,-50) )
axArr[1,1].set_xlim( (-80,-50) )

axArr[0,0].set_title( 'pcolor of $\sqrt{u^2+v^2}$', weight='bold' )
axArr[0,1].set_title( 'contourf of $\sqrt{u^2+v^2}$', weight='bold' )
axArr[1,0].set_title( 'quiver of $(u,v)$', weight='bold' )
axArr[1,1].set_title( 'streamplot of $(u,v)$', weight='bold' )

axArr[0,0].set_yticks( [32,36,40,44,48] )
axArr[1,0].set_yticks( [32,36,40,44,48] )

axArr[0,0].set_yticklabels( ['32$^\circ$','36$^\circ$','40$^\circ$','44$^\circ$','48$^\circ$'])
axArr[1,0].set_yticklabels( ['32$^\circ$','36$^\circ$','40$^\circ$','44$^\circ$','48$^\circ$'])

axArr[1,0].set_xticks( [-75,-70,-65,-60,-55] )
axArr[1,1].set_xticks( [-75,-70,-65,-60,-55] )

axArr[1,0].set_xticklabels( ['75$^\circ$','70$^\circ$','65$^\circ$','60$^\circ$','55$^\circ$'])
axArr[1,1].set_xticklabels( ['75$^\circ$','70$^\circ$','65$^\circ$','60$^\circ$','55$^\circ$'])

# adjust spacing and add colorbar
plt.subplots_adjust( wspace=0, hspace=0.15 )
plt.subplots_adjust( right=0.88 )

cbarAx = fig.add_axes( [0.9,0.11,0.03,0.77] )
cbar = fig.colorbar( im0, cax=cbarAx )
cbar.set_label('Speed (ms$^{-1}$)', weight='bold', fontsize=11 )
cbar.ax.tick_params( labelsize=12 )


# save the figure
plt.savefig( 'gulfStreamUV_snapshots.png', format='png', dpi=600 )

plt.show()