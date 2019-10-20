# libraries
import os

#os.environ["PROJ_LIB"] = "/home/arcturus/miniconda3/share/proj"
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

if __name__ == '__main__':

    # Control the position of the square. Give the coordinate of 2 corners
    m = Basemap(width=12000000,
                height=9000000,
                projection='lcc',
                resolution='l',  ## c, l, i, h, f
                lat_1=45.,
                lat_2=55,
                lat_0=50,
                lon_0=-107.,
    #             llcrnrlon=-160,
    #             llcrnrlat=-60,
    #             urcrnrlon=160,
    #             urcrnrlat=70
               )
    # m = Basemap(llcrnrlon=-100, llcrnrlat=-58,urcrnrlon=-30,urcrnrlat=15)
        
    # Draw the components of the map
#    m.drawmapboundary(fill_color='#A6CAE0', linewidth=0)
#    m.fillcontinents(color='brown', alpha=0.6, lake_color='grey')
#    m.drawcoastlines(linewidth=0.1, color="white")

#    m.drawmapboundary(fill_color='#A6CAE0')
#    m.drawcountries(color="white")

#    m.drawlsmask(land_color='coral',ocean_color='aqua',lakes=True)

    m.bluemarble()

    plt.show()
