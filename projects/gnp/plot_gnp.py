import os

import numpy as np

import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
from mapy.config import Continent
from mapy.paths import DATA_DIR, OUTPUT_DIR
from matplotlib.collections import PatchCollection
from matplotlib.patches import Polygon
from mpl_toolkits.basemap import Basemap

# COUNTRY_COORDS_FILE = os.path.join(DATA_DIR, "eu_country_lon_lat_extended.csv")
COUNTRY_COORDS_FILE = os.path.join(DATA_DIR, "world_country_lon_lat.csv")
COUNTRY_GNP_FILE = os.path.join(DATA_DIR, "worldbank_gnp.csv")
SHAPE_FILE = os.path.join(DATA_DIR, "natural_earth/ne_10m_admin_0_countries")  ## w/o extension

YEAR = '2000'
REGION = 'world'
TITLE = "{} GNP (Gross National Product) in {} (US Dollars)".format(REGION.title(), YEAR)
TEXT_OFFSET = 0
LOWER_LATITUDE_OFFSET = 1
N_COLORS = 9
GNP_VALUE_TEXT_FONTSIZE = 5
RESOLUTION = 'l'  ## c, l, i, h, f
FIGURE_SIZE = (50, 10)

OUTPUT_FILE = os.path.join(OUTPUT_DIR, "{}_gnp{}_map.png".format(REGION, YEAR))

if __name__ == '__main__':

    ## Set region and its coordinates
    if REGION == 'europe':
        region = Continent.europe
    elif REGION == 'world':
        region = Continent.world
    else:
        print("{} is not available. Choose from ['world', 'europe']".format(REGION))
        exit()

    region_llcrnrlon = region['llcrnrlon']
    region_llcrnrlat = region['llcrnrlat']
    region_urcrnrlon = region['urcrnrlon']
    region_urcrnrlat = region['urcrnrlat']
    region_lat0 = region['lat_0']
    region_lon0 = region['lon_0']
    region_lat1 = region['lat_1']
    region_lat2 = region['lat_2']

    ## Read country coordinates
    df_region = pd.read_csv(COUNTRY_COORDS_FILE)

    ## Read gnp values
    df_gnp = pd.read_csv(COUNTRY_GNP_FILE)

    ## Merge with region df
    merged = pd.merge(df_gnp, df_region, left_on='Country Name', right_on='name')[['name', YEAR, 'lon', 'lat']]
    df = merged.dropna()

    ## Set digitized color intervals
    gnp_values = df[YEAR]
    cm = plt.get_cmap('Oranges')
    scheme = np.array([cm(i / N_COLORS) for i in range(N_COLORS)])
    bins = np.linspace(gnp_values.min(), gnp_values.max(), N_COLORS)
    df['bin'] = np.digitize(gnp_values, bins) - 1

    ## Figure
    fig = plt.figure(figsize=FIGURE_SIZE)
    ax = fig.add_subplot(111, frame_on=False)
    fig.suptitle(TITLE, fontsize=10, y=.90)

    # Control the position of the square. Give the coordinate of 2 corners
    if REGION == 'world':
        m = Basemap(
                    llcrnrlon=region_llcrnrlon,
                    llcrnrlat=region_llcrnrlat - LOWER_LATITUDE_OFFSET,
                    urcrnrlon=region_urcrnrlon,
                    urcrnrlat=region_urcrnrlat,
                    projection='cyl',
                    resolution=RESOLUTION,
                    area_thresh=1,
                )
    else:
        m = Basemap(
                    llcrnrlon=region_llcrnrlon,
                    llcrnrlat=region_llcrnrlat - LOWER_LATITUDE_OFFSET,
                    urcrnrlon=region_urcrnrlon,
                    urcrnrlat=region_urcrnrlat,
                    lat_0=region_lat0,
                    lon_0=region_lon0,
                    lat_1=region_lat1,
                    lat_2=region_lat2,
                    projection='lcc',
                    resolution=RESOLUTION,
                    area_thresh=1,
                )
    # Draw the components of the map
    m.drawmapboundary(fill_color='aqua', linewidth=0.5)
    # m.drawcountries(color='white', linewidth=0.5)
    # m.drawlsmask(land_color='white',
    #              ocean_color='aqua',
    #              lakes=False,
    #              resolution='f',
    #              grid=1.25)
    
    ## Write GNP value text 
    if REGION != 'world':
        for country in np.array(df):
            name, gnp, lon, lat, _ = country
            x, y = m(lon, lat)   ## Map projection
            x_off, y_off = x + TEXT_OFFSET, y + TEXT_OFFSET
            lon, lat = m(x, y, inverse=True)  ## Back to longitude-latitude
            gnp_str = str(gnp / 1000.) + 'k'
            plt.text(x_off, y_off, '{}'.format(gnp_str), fontsize=GNP_VALUE_TEXT_FONTSIZE)

    ## Color the countries
    m.readshapefile(SHAPE_FILE, 'units', color='#444444', linewidth=.2)
    country_names_in_df = np.array(df['name'])
    for info, shape in zip(m.units_info, m.units):
        ne_name = info['NAME_EN'].strip()
        # if "orea" in ne_name:  ## 
        #     print(ne_name)
        if ne_name not in country_names_in_df: 
            continue
        
        color = scheme[df[df['name'] == ne_name]['bin']]
        patches = [Polygon(np.array(shape), True)]
        pc = PatchCollection(patches)
        pc.set_facecolor(color)
        ax.add_collection(pc)

    ## Draw color legend
    ax_legend = fig.add_axes([0.37, 0.08, 0.3, 0.02], zorder=3)
    cmap = mpl.colors.ListedColormap(scheme)
    cb = mpl.colorbar.ColorbarBase(ax_legend,
                                   cmap=cmap,
                                   ticks=bins,
                                   boundaries=bins,
                                   orientation='horizontal')
    bins_k = bins / 1000.
    cb.ax.set_xticklabels([str(round(i, 1)) + 'k' for i in bins_k])

    ## Save figure
    plt.savefig(OUTPUT_FILE, bbox_inches='tight')
    print(OUTPUT_FILE, "was saved.")
    # plt.show()
