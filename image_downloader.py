import os
from bs4 import BeautifulSoup
import requests

class ImageDownloader:
    def __init__(self, url_image, folder_image):
        self.url_image = url_image
        self.folder_image = folder_image
        self.maxj_folder = os.path.join(folder_image, "maxj")
        self.moyj_folder = os.path.join(folder_image, "moyj")
        self.polluants = ["NO2", "O3", "PM10", "PM25"]

    def create_polluant_folders(self):
        for folder in [self.maxj_folder, self.moyj_folder]:
            for polluant in self.polluants:
                os.makedirs(os.path.join(folder, polluant), exist_ok=True)

    def download_images(self):
        response = requests.get(self.url_image)
        soup = BeautifulSoup(response.content, "html.parser")
        file_links = [link.get("href") for link in soup.find_all("a") if link.get("href").endswith(".jpg")]

        for file_link in file_links:
            download_url = "http://www.prevair.org/donneesmisadispo/public/" + file_link
            filename = os.path.basename(download_url)
            
            if "MAXJ" in filename:
                dest_folder = self.maxj_folder
            elif "MOYJ" in filename:
                dest_folder = self.moyj_folder
            else:
                continue
            
            for polluant in self.polluants:
                if polluant in filename:
                    polluant_folder = os.path.join(dest_folder, polluant)
                    break
            else:
                continue

            dest_path = os.path.join(polluant_folder, filename)

            if os.path.isfile(dest_path):
                print(f"Le fichier {filename} a déjà été téléchargé.")
                continue
            
            response = requests.get(download_url)
            with open(dest_path, "wb") as f:
                f.write(response.content)
                print(f"Le fichier {filename} a été téléchargé avec succès.")
