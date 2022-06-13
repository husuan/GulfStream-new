# This script takes sea-surface temperature data from Oct 26th 2017 and makes a nice
# plot. The data is high-resolution satellite data.

from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt

from mpl_toolkits.basemap import Basemap

########## 导入数据 ##########

data = Dataset('data/20171027_9.nc')

# get SST data into a numpy array
sst = np.squeeze( np.asarray( data.variables['sst'] ) )

# get lon and lat vectors
lon = np.asarray( data.variables['longitude'] )
lat = np.asarray( data.variables['latitude'] )

# extract the North Atlantic region 
# 显示范围
lonMap, latMap = 270, 20    # lower left corner of region
w, h = 120, 80          # width and height of region in degrees

lon0, lat0 = lonMap-10, latMap-20  # coordinates to extract SST values
# 由于倾斜所以这个范围要显示更大

sst = sst[ (lat>lat0) & (lat<lat0+h), : ]
sst = sst[ :, (lon>lon0) & (lon<lon0+w) ]

lon = lon[ (lon>lon0) & (lon<lon0+w) ]
lat = lat[ (lat>lat0) & (lat<lat0+h) ]

# land values are represented by a large negative number; modify these to NaNs
sst[ sst < 0 ] = 290

########## Construct a basemap instance ##########

fig = plt.figure( figsize=(12,6) )
# ax = fig.add_axes( [0.1,0.1,0.8,0.8], axisbg='white' )
ax = fig.add_axes( [0.1,0.1,0.8,0.8])

# make an initial map  # 显示中心的位置
m0 = Basemap(projection='ortho',lon_0=lonMap+30,lat_0=latMap,resolution=None)

# make a map viewing the edge of the earth
myMap = Basemap( projection='ortho', lon_0=lonMap+10, lat_0=latMap, resolution='l',
            llcrnrx=-1e6,llcrnry=0.,urcrnrx=m0.urcrnrx/(2.),urcrnry=m0.urcrnry/(2.5))

# add details
myMap.drawcoastlines()
myMap.drawmapboundary(fill_color='aqua')
myMap.fillcontinents(color='grey',lake_color='slateblue')
myMap.drawcountries()
myMap.drawparallels( np.arange(-90.,120.,15.), labels=[1,0,0,0] )
myMap.drawmeridians( np.arange(0.,360.,30.), labels=[0,0,0,1] )
myMap.drawmapboundary()


########## Plotting ##########

# get projection coordinates from lat and lon
lon, lat = np.meshgrid( lon, lat )
x, y = myMap( lon, lat )

# plot SST contours
myMap.pcolor( x, y, sst - 273.15, cmap='coolwarm', vmin=5, vmax=28 )

plt.title("Sea-Surface Temperature on 9:00 27/10/2017")

# add a colorbar
cBar = plt.colorbar()
cBar.set_label('Temperature ($^\circ$C)')
cBar.set_ticks( [5,10,15,20,25,28] )
cBar.set_ticklabels( ['<5.0','10.0','15.0','20.0','25.0','>28.0'] )

plt.savefig( 'SST_snapshot.png', format='png', dpi=400 )
plt.show()



