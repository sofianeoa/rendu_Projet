from image_downloader import ImageDownloader
from pollens_data import PollensDataManager
from gazs_data import GazsData


# Utilisation des classes
url_image = "http://www.prevair.org/donneesmisadispo/public/?C=N;O=A"
folder_image = "D:/ESGI/projet4iabd/image"

image_downloader = ImageDownloader(url_image, folder_image)
image_downloader.create_polluant_folders()
image_downloader.download_images()

url_pollens = "https://api.airparif.fr/pollens/bulletin"
folder_path = "D:/ESGI/projet4iabd/pollens"
pollens_data_manager = PollensDataManager(url_pollens, folder_path)
pollens_data_manager.save_pollens_data_to_csv()

download_folder = 'D:/ESGI/projet4iabd/gazs'
gazs_data = GazsData(download_folder)
gazs_data.download_csv_files()
gazs_data.merge_csv_data()
