import cartopy
import matplotlib.pyplot as plt


def main():

    ax = plt.axes([0,0,1,1], projection=cartopy.crs.TransverseMercator())

    ax.set_extent([-20, 0, 50, 55])
    ax.add_feature(cartopy.feature.COASTLINE)
    ax.add_geoms(geoms)
    plt.show()


if __name__ == '__main__':
    main()