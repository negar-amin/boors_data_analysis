import datetime
import os
from extract_transactions_xlsx_files import extract_xlsx_files
import logging
import pandas as pd
import glob

def convert_xlsx_to_csv(stage_directory:str, delete_xlsx: bool):
    try:
        xlsx_files = glob.glob(os.path.join("datalake","*.xlsx"))
        for xf in xlsx_files:
            file = pd.read_excel(xf)
            if delete_xlsx:
                os.remove(xf)
            file.drop(labels=[0],axis=0,inplace=True)

            #Check if exel file is not empty then create a csv file of it
            if len(file.axes[0]) != 1:
                file.to_csv(os.path.join(stage_directory,os.path.basename(xf).split(".")[0]+".csv"),header=False,index=False)
                logging.info(os.path.basename(__file__) +" "+ str(datetime.datetime.now()) + f" : {os.path.basename(xf)} was successfully converted to csv and saved to {stage_directory}")
            else:
                logging.info(os.path.basename(__file__) +" "+ str(datetime.datetime.now()) + f" : {os.path.basename(xf)} was empty.")
    except Exception as err:
        logging.error(os.path.basename(__file__) +" "+ str(datetime.datetime.now()) + f" : {err}" )


if __name__ == "__main__":
    stage_directory = os.path.join(os.path.curdir,"stage")
    convert_xlsx_to_csv(stage_directory,False)