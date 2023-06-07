from collections import defaultdict

from os import (
    listdir,
    path,
)

from bs4 import BeautifulSoup
from pandas import (
    DataFrame,
    concat,
    read_csv,
)

from requests import (
    get,
)

#################################################################################################################
# Cette classe permet de télécharger, de lire et de fusionner des fichiers CSV contenant des données sur les gaz.
class GazsData:
    # Initialisation de la classe avec le dossier de téléchargement des fichiers CSV.
    def __init__(self, download_folder):
        self.download_folder = download_folder
        self.url = "https://files.data.gouv.fr/lcsqa/concentrations-de-polluants-atmospheriques-reglementes/temps-reel/"

    # Télécharge les fichiers CSV depuis une URL donnée.
    def download_csv_files(self):
        downloaded_files = listdir(self.download_folder)
        response = get(self.url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Parcoure les dossiers de chaque année sur la page web.
        for year_folder in soup.select('a[href$="/"]'):
            year_url = self.url + year_folder['href']
            response_year = get(year_url)
            soup_year = BeautifulSoup(response_year.text, 'html.parser')

            # Parcoure les fichiers CSV dans chaque dossier annuel.
            for csv_file in soup_year.select('a[href$=".csv"]'):
                csv_url = year_url + csv_file['href']
                csv_filename = path.join(self.download_folder, csv_file['href'])

                # Si le fichier CSV n'a pas encore été téléchargé, le télécharge.
                if csv_file['href'] not in downloaded_files:
                    with open(csv_filename, 'wb') as f:
                        f.write(get(csv_url).content)

                        print(f"Le fichier {csv_file['href']} a été téléchargé avec succès.")

                    downloaded_files.append(csv_file['href'])

    # Lit un fichier CSV spécifique et renvoie un DataFrame pandas.
    def read_csv(self, f):
        df = read_csv(path.join(self.download_folder, f), sep=';')
        return df

    # Fusionne tous les fichiers CSV téléchargés en un seul DataFrame pandas.
    def merge_csv_data(self):
        csv_files = [f for f in listdir(self.download_folder) if f.endswith(".csv")]
        dfs = defaultdict(DataFrame)

        # Parcoure tous les fichiers CSV et les ajoute à un dictionnaire de DataFrames par année et mois.
        for file in csv_files:
            _, _, date_str = file.split('_')
            year, month, _ = date_str.split('-')
            temp_df = self.read_csv(file)
            dfs[(year, month)] = concat([dfs[(year, month)], temp_df], ignore_index=True)

        # Crée des DataFrames consolidés pour chaque année.
        pollution_df_2021 = concat([df for (year, month), df in dfs.items() if year == '2021'], ignore_index=True)
        pollution_df_2022 = concat([df for (year, month), df in dfs.items() if year == '2022'], ignore_index=True)
        pollution_df_2023 = concat([df for (year, month), df in dfs.items() if year == '2023'], ignore_index=True)

        # Affiche les DataFrames consolidés.
        print(pollution_df_2021)
        print(pollution_df_2022)
        print(pollution_df_2023)
