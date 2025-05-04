import pandas as pd #used for handling CSV files
import csv
from datetime import datetime 
#This imports just the datetime class from the datetime module directly
from data_entry import get_date,get_amount,get_category,get_description,date_format

class CSV:
    CSV_FILE = "finance_data.csv"
    COLUMNS = "date","amount","category","description"

    @classmethod
    def initialize_csv(cls):
        try:
            pd.read_csv(cls.CSV_FILE) #read the CSV file

        except FileNotFoundError:

            #Creates a new empty DataFrame
            df = pd.DataFrame(columns=["date","amount","category","description"])
            df.to_csv(cls.CSV_FILE, index=False)

    @classmethod
    def add_entry(cls, date, amount, category, description):
        new_entry = {
            "date" : date,
            "amount" : amount,
            "category" : category,
            "description" : description,
        }

        with open(cls.CSV_FILE,"a",newline="") as csvfile:
            writer = csv.DictWriter(csvfile,fieldnames=cls.COLUMNS)
            writer.writerow(new_entry)
        print("Entry added successfully")

    @classmethod
    def get_transactions(cls,start_date,end_date):
        df = pd.read_csv(cls.CSV_FILE)
        df["date"] = pd.to_datetime(df["date"],format = date_format)
        start_date = datetime.strptime(start_date,date_format)
        end_date = datetime.strptime(end_date,date_format)

        mask = (df["date"] >= start_date) & (df["date"]<=end_date)
        filtered_df = df.loc[mask]

        if filtered_df.empty:
            print("No transaction in the given date range")

        else:
            print(f"Transactions from {start_date.strftime(date_format)} to {end_date.strftime(date_format)}")

            print(
                filtered_df.to_string(index=False, formatters={"date": lambda x: x.strftime(date_format)})
            )

            total_income = filtered_df[filtered_df["category"]== "Income"]["amount"].sum()
            #Filters the DataFrame to only include rows where the category is "Income"

            total_expense = filtered_df[filtered_df["category"]=="Expense"]["amount"].sum()

            print(f"Total Income: {total_income:.2f}")
            print(f"Total Expense: {total_expense:.2f}")

def add():
    CSV.initialize_csv()

    date = get_date("Enter the date in (dd-mm-yyyy) format or enter for today's date",allow_default=True)

    amount = get_amount()
    category = get_category()
    description = get_description()

    CSV.add_entry (date,amount,category,description)

def main():
    while True:
        print("\n1. Add a new Transaction")
        print("2. View summary within a date range")
        print("3. Exit")
        choice = input("Enter your choice (1-3)")

        if choice =="1":
            add()
        elif choice == "2":
            start_date = get_date("Enter the start date (dd-mm-yyyy)")
            end_date = get_date("Enter the end date (dd-mm-yyyy)")
            df = CSV.get_transactions(start_date,end_date)
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()
