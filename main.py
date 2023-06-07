# Import des classes nécessaires.
from image_downloader import ImageDownloader

from pollens_data import PollensDataManager

from gazs_data import GazsData

# Téléchargement des images de polluants
# Utilisation de la classe ImageDownloader pour télécharger des images depuis l'URL spécifiée.
url_image = "http://www.prevair.org/donneesmisadispo/public/?C=N;O=A"
folder_image = "D:/ESGI/projet4iabd/image"

image_downloader = ImageDownloader(url_image, folder_image)
image_downloader.create_polluant_folders()  # Crée les dossiers nécessaires pour chaque polluant.
image_downloader.download_images()  # Télécharge les images.

# Téléchargement et sauvegarde des données sur les pollens
# Utilisation de la classe PollensDataManager pour télécharger et sauvegarder les données de pollens.
url_pollens = "https://api.airparif.fr/pollens/bulletin"
folder_path = "D:/ESGI/projet4iabd/pollens"
pollens_data_manager = PollensDataManager(url_pollens, folder_path)
pollens_data_manager.save_pollens_data_to_csv()  # Sauvegarde les données de pollens dans un fichier CSV.

# Téléchargement et fusion des données sur les gaz
# Utilisation de la classe GazsData pour télécharger et fusionner les données sur les gaz.
download_folder = 'D:/ESGI/projet4iabd/gazs'
gazs_data = GazsData(download_folder)
gazs_data.download_csv_files()  # Télécharge les fichiers CSV contenant les données sur les gaz.
gazs_data.merge_csv_data()  # Fusionne les données sur les gaz.
