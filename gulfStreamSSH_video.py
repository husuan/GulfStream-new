# This script takes absolute dynamic topography (ADT) satellite altimetry data from
# the Gulf Stream region, and produces an animation from the daily 2D snapshots.

import matplotlib
import matplotlib as mpl
matplotlib.use('TkAgg')
# matplotlib.use("Agg")

import numpy as np
import matplotlib.pyplot as plt
import scipy.io as sio
import pandas as pd

from mpl_toolkits.basemap import Basemap
from matplotlib.cm import get_cmap
import matplotlib.animation as manimation

# uncomment this line if you want to see the plots as they are saved
#plt.ion()

# load data
adt = np.transpose( sio.loadmat('data/adt.mat')['adt_all'], (1,0,2) )
# 转换 经度 纬度

########## Make a basemap instance ##########

cMap = get_cmap('ocean')
lakeColor = cMap(0.5)

fig = plt.figure( figsize=(8,6) )

# set up orthographic map projection with perspective of satellite looking down at 40N, 65W.
map = Basemap( projection='stere', lat_0=40, lon_0=-65, resolution='l', llcrnrlon=-80, llcrnrlat=30., urcrnrlon=-50, urcrnrlat=50, suppress_ticks=True )

# get projections of lon and lat in axis coordinates
lon, lat = np.linspace( -80, -50, num=121 ), np.linspace( 30, 50, num=81 )
lonGrid, latGrid = np.meshgrid( lon, lat )
x, y = map( lonGrid, latGrid )

# get projections for various places  单独的几个城市
xNY, yNY = map( -74.00, 40.71 )     # New York
xCH, yCH = map( -75.54, 35.25 )     # Cape Hatteras
xB, yB = map( -71.06, 42.36 )       # Boston

# define ADT spacings for contourf function and the datelist for title
adtSpacings = np.linspace( -1.2, 1.2, num=13 )
dateList = pd.date_range( '1993-01-01', periods=adt.shape[2], freq='D' ).tolist()


########## Make video ##########

FFMpegWriter = manimation.writers['ffmpeg']
metadata = dict( title='Gulf Stream SSH', artist='Tom Bolton', comment='Gulf Stream Visualization of AVISO ADT data.' )
writer = FFMpegWriter( fps=24, metadata=metadata, bitrate=30000, codec='libx264' )

with writer.saving( fig, "gulfStreamSSH_b.gif", 100 ) :

    for t in range(1, 31, 1):  # t 时间维度

        print(t)

        # draw coastlines, country boundaries, fill continents.
        map.drawcoastlines(linewidth=0.25)
        map.fillcontinents(color='indianred', lake_color=lakeColor)

        # add lon and lat axis labels
        map.drawparallels(np.arange(30, 50, 3), labels=[1, 0, 0, 0], linewidth=0.0)
        map.drawmeridians(np.arange(-80, -50, 5), labels=[0, 0, 0, 1], linewidth=0.0)

        # draw the edge of the map projection region (the projection limb)
        map.drawmapboundary(fill_color=lakeColor)
        map.drawstates()
        map.drawcountries()

        # make a string for the date
        titleString = str(dateList[t])
        titleString = titleString[0:10]

        # plot the sea-surface height contours
        cf = map.contourf(x[:-1, :-1], y[:-1, :-1], adt[:, :, t], levels=adtSpacings, extend='max',
                          cmap='ocean', vmin=adtSpacings[0], vmax=adtSpacings[-1] )

        # if SSH value goes over the max level, make this appear as white
        # cmap = mpl.cm.get_cmap("ocean").copy()
        # cf.cmap.set_over('white')

        # add colorbar
        cbar = map.colorbar( cf, location='right' )
        cbar.set_label('SSH (m)')

        # plot title
        plt.title( "Sea-surface height     " + titleString, fontsize=15 )

        # annotate New York
        plt.text( xNY-50000, yNY, 'New York', ha='right', color='white', fontweight='bold' )
        plt.plot( xNY, yNY, 'o', mfc='red', mec='white', mew=2 )

        # annotate Cape Hatteras
        plt.text(xCH - 50000, yCH, 'Cape\n Hatteras', ha='right', color='white', fontweight='bold')
        plt.plot(xCH, yCH, 'o', mfc='red', mec='white', mew=2)

        # annotate Boston
        plt.text(xB - 50000, yB, 'Boston', ha='right', color='white', fontweight='bold')
        plt.plot(xB, yB, 'o', mfc='red', mec='white', mew=2)

        # save this figure as a frame
        plt.pause(0.1)
        writer.grab_frame()

        # clear the axis data so it doesn't accumulate
        plt.cla()

