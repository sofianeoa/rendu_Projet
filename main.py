# Import des classes nécessaires.
from image_downloader import ImageDownloader
from pollens_data import PollensDataManager
from gazs_data import GazsData
from geojson_image_overlay import GeoJsonImageOverlay

# Téléchargement des images de polluants
url_image = "http://www.prevair.org/donneesmisadispo/public/?C=N;O=A"
folder_image = r"C:/Users/sofia/Desktop/4iabd/pa/data/image"

image_downloader = ImageDownloader(url_image, folder_image)
image_downloader.create_polluant_folders()  # Crée les dossiers nécessaires pour chaque polluant.
image_downloader.download_images()  # Télécharge les images.

# Téléchargement et sauvegarde des données sur les pollens
url_pollens = "https://api.airparif.fr/pollens/bulletin"
folder_path = r"C:\Users\sofia\Desktop\4iabd\pa\data\pollens"
pollens_data_manager = PollensDataManager(url_pollens, folder_path)
pollens_data_manager.save_pollens_data_to_csv()  # Sauvegarde les données de pollens dans un fichier CSV.

# Téléchargement et fusion des données sur les gaz
download_folder = r'C:\Users\sofia\Desktop\4iabd\pa\data\gazs'
gazs_data = GazsData(download_folder)
gazs_data.download_csv_files()  # Télécharge les fichiers CSV contenant les données sur les gaz.
gazs_data.merge_csv_data()  # Fusionne les données sur les gaz.

# Chemins d'accès au GeoJSON et à l'image
geojson_path = r"C:\Users\sofia\Desktop\4iabd\pa\data\image\moyj\test\test.geojson"
image_path = r"C:\Users\sofia\Desktop\4iabd\pa\data\image\moyj\test2\PREVAIR.analyse.20230601.MOYJ.PM25.public.jpg"

# Initialisation de la classe GeoJsonImageOverlay avec les chemins d'accès
geojson_image_overlay = GeoJsonImageOverlay(geojson_path, image_path)

# Appel des méthodes pour lire le GeoJSON, afficher ses limites géographiques, 
# et superposer l'image sur les limites géographiques
geojson_image_overlay.read_and_plot_geojson()
geojson_image_overlay.overlay_image_on_geojson()
