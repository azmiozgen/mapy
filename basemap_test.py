import os

from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from config import Continent

TEXT_OFFSET = 10000
COUNTRY_COORDS_FILE = "./asset/eu_country_lon_lat.csv"

if __name__ == '__main__':

    ## Europe coordinates
    eu_llcrnrlon = Continent.europe['llcrnrlon']
    eu_llcrnrlat = Continent.europe['llcrnrlat']
    eu_urcrnrlon = Continent.europe['urcrnrlon']
    eu_urcrnrlat = Continent.europe['urcrnrlat']
    eu_lat0 = Continent.europe['lat_0']
    eu_lon0 = Continent.europe['lon_0']
    eu_lat1 = Continent.europe['lat_1']
    eu_lat2 = Continent.europe['lat_2']

    # Control the position of the square. Give the coordinate of 2 corners
    plt.figure(figsize=(20, 12))
    m = Basemap(
                llcrnrlon=eu_llcrnrlon,
                llcrnrlat=eu_llcrnrlat,
                urcrnrlon=eu_urcrnrlon,
                urcrnrlat=eu_urcrnrlat,
                lat_0=eu_lat0,
                lon_0=eu_lon0,
                lat_1=eu_lat1,
                lat_2=eu_lat2,
                projection='lcc',
                resolution='l',  ## c, l, i, h, f
               )

    # Draw the components of the map
    m.drawmapboundary(fill_color='#A6CAE0', linewidth=0)
    m.fillcontinents(color='coral', alpha=0.6, lake_color='grey')
    m.drawcoastlines(linewidth=0.1, color="white")
    m.drawlsmask(land_color='coral',ocean_color='aqua',lakes=True)

    m.drawcountries(color="white")

    ## Parallels and meridians
    parallels = np.arange(0.,81,10.)
    meridians = np.arange(10.,351.,20.)
    m.drawparallels(parallels, labels=[False,True,True,False])
    m.drawmeridians(meridians, labels=[True,False,False,True])

    ## Read country coordinates
    df = pd.read_csv(COUNTRY_COORDS_FILE)
    eu_array = np.array(df)

    for country in eu_array:
        code, lat, lon, name = country
        x, y = m(lon, lat)   ## Map projection
        x_off, y_off = x + TEXT_OFFSET, y + TEXT_OFFSET
        lon, lat = m(x, y, inverse=True)  ## Back to longitude-latitude
        m.plot(x, y, 'bo')

        # plt.text(x_off, y_off, '{} ({:.1f}, {:.1f})'.format(name, lon, lat))
        plt.text(x_off, y_off, '{}'.format(name))
    plt.show()
