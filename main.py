import argparse
import logging
import os
from extract_transactions_xlsx_files import extract_xlsx_files
from convert_xlsx_files_to_csv_files import convert_xlsx_to_csv, str2bool
from analyze_transactions import AnalizeBourseData

logging.basicConfig(filename='error.log', encoding='utf-8', level=logging.INFO)

parser = argparse.ArgumentParser(description="extract exel files of bourse from start_date to end_date and convert them to csv and save them to stage_directory in stage folder and then analyze them.")
parser.add_argument("start_date",type=str,help="starting date of exel files we want to extract")
parser.add_argument("end_date",type=str,help="end date of exel files we want to extract")
parser.add_argument("stage_directory",type=str,help="convert xlsx files to csv in a stage directory given by user")
parser.add_argument("-c","--clear_xlsx_files", default=False, type=str2bool, help="directory that user wants to make a stage folder in it")
args = parser.parse_args() 

extract_xlsx_files(args.start_date.split("-"),args.end_date.split("-"))

convert_xlsx_to_csv(args.stage_directory,args.clear_xlsx_files)

stocks_info_list = AnalizeBourseData.extract_csv_files_from_stage_folder(os.path.join(args.stage_directory,"stage"))
print("\nStocks with most volume of transactions:")
print(AnalizeBourseData.n_most_affected_stocks(field ="Volume", casting_type = int, n = 10, stock_info_list = stocks_info_list, positive = True))
print("\nStocks with most price increase:")
print(AnalizeBourseData.n_most_affected_stocks(field = "Final_Price_change", casting_type = float, n = 10,  stock_info_list = stocks_info_list, positive = True))
print("\nStocks with most price decrease:")
print(AnalizeBourseData.n_most_affected_stocks(field = "Final_Price_change", casting_type = float, n = 10,stock_info_list = stocks_info_list, positive = False))