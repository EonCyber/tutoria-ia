import os
from pathlib import Path
import pandas as pd

class CsvToSqlPipeline:

    def __init__(self, data_path):
        self.data_path = data_path
       

    def populate_data_list(self):
        file_list = []
        for root, _, files in os.walk(self.data_path):
            for file in [f for f in files if f.lower().endswith(".csv")]:
                name_without_ext = os.path.splitext(file)[0]
                full_path = Path(root, file).as_posix()
                file_list.append((name_without_ext, full_path))
        return file_list
    
    def run(self, engine):
        print('INFO: Migrating csv data to sql database.')
        files = self.populate_data_list()
        for name, path in files:
            df = pd.read_csv(path)
            df.to_sql(name=name, con=engine, if_exists='append', index=False)
        print('INFO: Migration Pipeline Success!')