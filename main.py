import pandas as pd #used for handling CSV files
import csv
from datetime import datetime 
#This imports just the datetime class from the datetime module directly

class CSV:
    CSV_FILE = "finance_data.csv"

    @classmethod
    def initialize_csv(cls):
        try:
            pd.read_csv(cls.CSV_FILE) #read the CSV file
        except FileNotFoundError:
            #Creates a new empty DataFrame
            df = pd.DataFrame(columns=["date","amount","category","description"])
            df.to_csv(cls.CSV_FILE, index=False)