import argparse
import datetime
import os
from extract_transactions_xlsx_files import extract_xlsx_files
import logging
import pandas as pd
import glob

def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')
    
def convert_xlsx_to_csv(stage_directory:str, delete_xlsx: bool):
    try:
        xlsx_files = glob.glob(os.path.join("datalake","*.xlsx"))
        for xf in xlsx_files:
            file = pd.read_excel(xf)
            if delete_xlsx == True:
                os.remove(xf)
            file.drop(labels=[0],axis=0,inplace=True)

            #Check if exel file is not empty then create a csv file of it
            if len(file.axes[0]) != 1:
                stage_folder = os.path.join(stage_directory,"stage")
                os.makedirs(stage_folder,exist_ok=True)
                print(stage_folder)
                file.to_csv(os.path.join(stage_folder,os.path.basename(xf).split(".")[0]+".csv"),header=False,index=False)
                print("process was successful for more information see error.log")
                logging.info(os.path.basename(__file__) +" "+ str(datetime.datetime.now()) + f" : {os.path.basename(xf)} was successfully converted to csv and saved to {stage_folder}")
            else:
                print(f"{xf} convert wasn't done because of empty content due to holiday")
                logging.info(os.path.basename(__file__) +" "+ str(datetime.datetime.now()) + f" : {os.path.basename(xf)} was empty.")
    except Exception as err:
        print("something went wrong for more information look error.log")
        logging.error(os.path.basename(__file__) +" "+ str(datetime.datetime.now()) + f" : {err}" )

if __name__ == "__main__":
    logging.basicConfig(filename='error.log', encoding='utf-8', level=logging.INFO)
    parser = argparse.ArgumentParser(description="convert xlsx files to csv in a stage directory given by user")
    parser.add_argument("stage_directory",type=str,help="directory that user wants to make a stage folder in it")
    parser.add_argument("-c","--clear_xlsx_files", default=False, type=str2bool, help="the option that if user wants to clear xlsx files after convertion or not")
    args = parser.parse_args() 
    convert_xlsx_to_csv(args.stage_directory,args.clear_xlsx_files)