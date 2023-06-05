from os import (
    listdir,
    path,
)

import requests

from collections import defaultdict

import pandas as pd
# convention pep 8 

from bs4 import BeautifulSoup


class GazsData:
    def __init__(self, download_folder):
        self.download_folder = download_folder
        self.url = "https://files.data.gouv.fr/lcsqa/concentrations-de-polluants-atmospheriques-reglementes/temps-reel/"

    def download_csv_files(self):
        downloaded_files = listdir(self.download_folder)
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, 'html.parser')

        for year_folder in soup.select('a[href$="/"]'):
            year_url = self.url + year_folder['href']
            response_year = requests.get(year_url)
            soup_year = BeautifulSoup(response_year.text, 'html.parser')

            for csv_file in soup_year.select('a[href$=".csv"]'):
                csv_url = year_url + csv_file['href']
                csv_filename = path.join(self.download_folder, csv_file['href'])

                if csv_file['href'] not in downloaded_files:
                    with open(csv_filename, 'wb') as f:
                        f.write(requests.get(csv_url).content)

                        print(f"Le fichier {csv_file['href']} a été téléchargé avec succès.")

                    downloaded_files.append(csv_file['href'])

    def read_csv(self, f):
        df = pd.read_csv(path.join(self.download_folder, f), sep=';')

        return df

    def merge_csv_data(self):
        fichiers_csv = [f for f in listdir(self.download_folder) if f.endswith(".csv")]
        dfs = defaultdict(pd.DataFrame)

        for fichier in fichiers_csv:
            _, _, date_str = fichier.split('_')
            year, month, _ = date_str.split('-')
            df_temp = self.read_csv(fichier)
            dfs[(year, month)] = pd.concat([dfs[(year, month)], df_temp], ignore_index=True)

        df_polution_2021 = pd.concat([df for (year, month), df in dfs.items() if year == '2021'], ignore_index=True)
        df_polution_2022 = pd.concat([df for (year, month), df in dfs.items() if year == '2022'], ignore_index=True)
        df_polution_2023 = pd.concat([df for (year, month), df in dfs.items() if year == '2023'], ignore_index=True)

        print(df_polution_2021)
        print(df_polution_2022)
        print(df_polution_2023)
