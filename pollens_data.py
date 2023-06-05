import os
import pandas as pd
import datetime
import requests


class PollensData:
    def __init__(self, url_pollens):
        self.url_pollens = url_pollens
        self.headers = {
            "X-Api-Key": "06a92dff-35b2-2308-cf68-95f2c55fc427",
        }

    def get_pollens_data(self):
        res = requests.get(self.url_pollens, headers=self.headers)
        dataAirParif = res.json()
        data = dataAirParif['data']
        columns = []
        pollen_names = data[0]['taxons']

        for observation in data:
            values = observation['valeurs']

            for departement, pollen_counts in values.items():
                row = {'departement': departement}

                for i, count in enumerate(pollen_counts):
                    pollen_name = pollen_names[i]
                    row[pollen_name] = count

                columns.append(row)

        df_pollens = pd.DataFrame(columns)
        df_pollens['departement'] = df_pollens['departement'].astype(int)
        df_pollens['time'] = pd.Timestamp.today().date()

        return df_pollens


class PollensDataManager:
    def __init__(self, url_pollens, folder_path):
        self.pollens_data = PollensData(url_pollens)
        self.folder_path = folder_path

    def save_pollens_data_to_csv(self):
        df_pollens = self.pollens_data.get_pollens_data()
        nom_fichier = f"csv_pollen_{datetime.date.today().strftime('%d-%m-%Y')}.csv"
        chemin_fichier = os.path.join(self.folder_path, nom_fichier)

        if os.path.exists(chemin_fichier):
            print(f"Le fichier {nom_fichier} existe déjà.")
        else:
            df_pollens.to_csv(chemin_fichier, index=False)

            print(f"Le DataFrame a été enregistré sous le nom de fichier : {chemin_fichier}")
            print(df_pollens)
