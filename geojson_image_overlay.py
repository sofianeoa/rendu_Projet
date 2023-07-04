import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

class GeoJsonImageOverlay:
    """
    Classe pour lire un GeoJSON, afficher ses limites géographiques,
    et superposer une image sur les limites géographiques.
    """
    def __init__(self, geojson_path, image_path):
        self.geojson_path = geojson_path
        self.image_path = image_path

    def read_and_plot_geojson(self):
        gdf = gpd.read_file(self.geojson_path)
        bounds = gdf.total_bounds
        fig, ax = plt.subplots()
        gdf.plot(ax=ax)
        ax.set_xlim(bounds[0], bounds[2])
        ax.set_ylim(bounds[1], bounds[3])
        ax.grid(True, alpha=0.3)
        plt.show()

    def overlay_image_on_geojson(self):
        gdf = gpd.read_file(self.geojson_path)
        img = Image.open(self.image_path)
        img_array = np.array(img)
        bounds = gdf.total_bounds
        fig, ax = plt.subplots()
        ax.imshow(img_array, extent=[bounds[0], bounds[2], bounds[1], bounds[3]])
        gdf.plot(ax=ax, facecolor='none', edgecolor='red')
        ax.set_xlim(bounds[0], bounds[2])
        ax.set_ylim(bounds[1], bounds[3])
        ax.grid(True, alpha=0.3)
        plt.show()
