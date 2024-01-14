import argparse
import jdatetime
import logging
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


class AnalizeBourseData:
    @staticmethod
    def read_csv_file(file_path: str) -> List[StockInfo]:
        stocks_info = []
        try:
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
        except Exception as err:
            print("something went wrong for more information look error.log")
            logging.error(os.path.basename(__file__) +" "+ str(jdatetime.datetime.now()) + f" : {err}")
        return stocks_info
    
    @staticmethod
    def n_most_affected_stocks(field: str, casting_type, n: int, stock_info_list, positive: bool):
        analyze_dict= {}
        try:
            for stocks_info in stock_info_list:
                for row in stocks_info:
                    if not row.Mark in analyze_dict.keys():
                        analyze_dict[row.Mark] = casting_type(getattr(row,field))
                    else:
                        analyze_dict[row.Mark]+= casting_type(getattr(row,field))
        except Exception as err:
            print("something went wrong for more information look error.log")
            logging.error(os.path.basename(__file__) +" "+ str(jdatetime.datetime.now()) + f" : {err}")
        return dict(sorted(analyze_dict.items(), key=itemgetter(1), reverse = positive)[:n])
    
    @staticmethod
    def extract_csv_files_from_stage_folder(stage_directory:str):
        stocks_info_list = []
        try:
            csv_files = glob.glob(os.path.join(stage_directory,"*.csv"))
            for f in csv_files:
                stocks_info_list.append(AnalizeBourseData.read_csv_file(f))
        except Exception as err:
            print("something went wrong for more information look error.log")
            logging.error(os.path.basename(__file__) +" "+ str(jdatetime.datetime.now()) + f" : {err}")
        return stocks_info_list


if __name__ == "__main__":
    logging.basicConfig(filename='error.log', encoding='utf-8', level=logging.INFO)
    parser = argparse.ArgumentParser(description="Analyze desired data of user in stage folder")
    parser.add_argument("stage_directory",type=str,help="directory of stage folder")
    args = parser.parse_args() 
    stage_directory = args.stage_directory
    stocks_info_list = AnalizeBourseData.extract_csv_files_from_stage_folder(stage_directory=stage_directory)
    print("\nStocks with most volume of transactions:")
    print(AnalizeBourseData.n_most_affected_stocks(field ="Volume", casting_type = int, n = 10, stock_info_list = stocks_info_list, positive = True))
    print("\nStocks with most price increase:")
    print(AnalizeBourseData.n_most_affected_stocks(field = "Final_Price_change", casting_type = float, n = 10,  stock_info_list = stocks_info_list, positive = True))
    print("\nStocks with most price decrease:")
    print(AnalizeBourseData.n_most_affected_stocks(field = "Final_Price_change", casting_type = float, n = 10,stock_info_list = stocks_info_list, positive = False))

