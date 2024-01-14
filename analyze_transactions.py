from operator import itemgetter
from typing import Dict, TypeVar
from dataclasses import dataclass
import glob
from typing import List
import csv
import os

@dataclass
class StockInfo:
    Mark: str
    Name: str
    Count: str
    Volume: str
    Value: str
    Yesterday_Price: str
    First_Transaction_Price: str
    Last_Transaction_Price: str
    Last_Transaction_change: str
    Last_Transaction_Percent: str
    Final_Price: str
    Final_Price_change: str
    Final_Price_percent: str
    Least_transaction_Price: str
    most_transaction_Price: str



def read_csv_file(file_path: str) -> List[StockInfo]:
    stocks_info = []
    with open(file_path, 'r', newline='', encoding="utf8") as csvfile:
        csv_reader = csv.DictReader(csvfile)
        
        # Get the field names from the CSV headers
        heading = csv_reader.fieldnames
        for row in csv_reader:
            stock_info = StockInfo(
                Mark=row[heading[0]],
                Name=row[heading[1]],
                Count=row[heading[2]],
                Volume=row[heading[3]],
                Value=row[heading[4]],
                Yesterday_Price=row[heading[5]],
                First_Transaction_Price=row[heading[6]],
                Last_Transaction_Price=row[heading[7]],
                Last_Transaction_change=row[heading[8]],
                Last_Transaction_Percent=row[heading[9]],
                Final_Price=row[heading[10]],
                Final_Price_change=row[heading[11]],
                Final_Price_percent=row[heading[12]],
                Least_transaction_Price=row[heading[13]],
                most_transaction_Price=row[heading[14]]
            )
            stocks_info.append(stock_info)

    return stocks_info

def n_most_affected_stocks(field: str, casting_type, n: int, stock_info_list, positive: bool):
    analyze_dict= {}
    for stocks_info in stock_info_list:
        for row in stocks_info:
            if not row.Mark in analyze_dict.keys():
                analyze_dict[row.Mark] = casting_type(getattr(row,field))
            else:
                analyze_dict[row.Mark]+= casting_type(getattr(row,field))
    return dict(sorted(analyze_dict.items(), key=itemgetter(1), reverse = positive)[:n])

def extract_csv_files_from_stage_folder(stage_directory:str):
    csv_files = glob.glob(os.path.join(stage_directory,"*.csv"))
    stocks_info_list = []
    for f in csv_files:
        stocks_info_list.append(read_csv_file(f))
    return stocks_info_list

# Example usage:
if __name__ =="__main__":
    stage_directory = "stage"
    stocks_info_list = extract_csv_files_from_stage_folder(stage_directory=stage_directory)
    stock = stocks_info_list[0][0].Mark
    print("\nStocks with most volume of transactions:")
    print(n_most_affected_stocks(field ="Volume", casting_type = int, n = 10, stock_info_list = stocks_info_list, positive = True))
    print("\nStocks with most price increase:")
    print(n_most_affected_stocks(field = "Final_Price_change", casting_type = float, n = 10,  stock_info_list = stocks_info_list, positive = True))
    print("\nStocks with most price decrease:")
    print(n_most_affected_stocks(field = "Final_Price_change", casting_type = float, n = 10,stock_info_list = stocks_info_list, positive = False))

