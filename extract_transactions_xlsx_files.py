import requests
import os
import re 
import jdatetime
import logging
from urllib.parse import urlparse, unquote
import argparse

# Retrun all dates between start and end date except thursdays and fridays
def date_range(start_date: jdatetime.datetime,end_date: jdatetime.datetime):
    try:
        all_dates=[]
        delta = end_date - start_date   

        for i in range(delta.days + 1):
            date = start_date + jdatetime.timedelta(days=i)
            if date.weekday() not in {5,6}:
                all_dates.append(f"{date.year}-{str(date.month).zfill(2)}-{str(date.day).zfill(2)}")
        return all_dates
    except Exception as err:
        print("something went wrong for more information look error.log")
        logging.error(os.path.basename(__file__) +" "+ str(jdatetime.datetime.now()) + f" : {err}")

# Extract Exel files of transactions
def extract_xlsx_files(start_date: list[str], end_date: list[str]):
    #Check if dates entered in correct format
    if re.fullmatch(r"\d+-\d{2}-\d{2}", "-".join(start_date))!= None and re.fullmatch(r"(\d)+-\d{2}-\d{2}", "-".join(end_date))!= None:
        
        start_date = [int(d) for d in start_date]
        end_date = [int(d) for d in end_date]

        try:
            # Get all dates between start_date and end_date
            all_dates = date_range(jdatetime.datetime(year=start_date[0],month=start_date[1],day=start_date[2]),jdatetime.datetime(year=end_date[0],month=end_date[1],day=end_date[2]))
            
            #For each date in given range save the related xlsx file to stage
            for date in all_dates:
                excel_file_url = 'http://members.tsetmc.com/tsev2/excel/MarketWatchPlus.aspx?d='+ date
                data_folder = 'datalake'
                os.makedirs(data_folder, exist_ok=True)
                file_name = f"{date}.xlsx"
                local_file_path = os.path.join(data_folder, file_name)
                response = requests.get(excel_file_url)

                # Check if the request was successful (status code 200)
                if response.status_code == 200:
                    with open(local_file_path, 'wb') as excel_file:
                        excel_file.write(response.content)
                    print("proccess successfull see error.log for more info")
                    logging.info(os.path.basename(__file__)+" "+ str(jdatetime.datetime.now())+f" : Excel file '{file_name}' saved to '{local_file_path}' successfully.")
                else:
                    print("something went wrong for more information look error.log")
                    logging.warning(os.path.basename(__file__) +" "+ str(jdatetime.datetime.now())+f" : Failed to fetch Excel file. Status code: {response.status_code}")
        except Exception as err:
            print("something went wrong for more information look error.log")
            logging.error(os.path.basename(__file__) +" "+ str(jdatetime.datetime.now()) + f" : {err}")
    else:
        print("something went wrong for more information look error.log")
        logging.error(os.path.basename(__file__) +" "+ str(jdatetime.datetime.now()) +f" start_date:{'-'.join(start_date)} or end_date:{'-'.join(end_date)} were not in correct format")

if __name__ == "__main__": 
    logging.basicConfig(filename='error.log', encoding='utf-8', level=logging.INFO)
    parser = argparse.ArgumentParser(description="extract exel files of bourse from start_date to end_date given by argparse")
    parser.add_argument("start_date",type=str,help="starting date of exel files we want to extract")
    parser.add_argument("end_date",type=str,help="end date of exel files we want to extract")
    args = parser.parse_args() 
    extract_xlsx_files(args.start_date.split("-"),args.end_date.split("-"))