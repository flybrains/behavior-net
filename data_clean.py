import pandas as pd
import numpy as np
import xlrd as xl
import argparse
import csv
import os
from datetime import datetime



def csv_from_excel(path, n_inds=2):
    """
    Takes Excel .xls workbook as input and saves

    """

    try:
        os.mkdir(os.getcwd() + "/data/csv")
    except FileExistsError:
        pass

    name = (path.split('/')[-1]).split('.')[0]
    book = xl.open_workbook(path)

    dt = datetime.now()
    dt_string = str(dt.month)+"_"+str(dt.day)+"_"+str(dt.year)+"_"+str(dt.hour)+str(dt.minute)
    os.mkdir(os.getcwd() + "/data/csv/" + dt_string)

    for i in range(book.nsheets)
        sheet = book.sheet_by_index(i)
        if sheet.name[0:3]=='fly':
            fly_n = int(sheet.name[3])
            csv_name = name + '_Fly' + sheet.name[3] + '.csv'
            csv_file = open(csv_name, 'w')
            wr = csv.writer(csv_file, quoting=csv.QUOTE_ALL)

            for row_n in range(sheet.nrows):
                wr.writerow(sheet.row_values(int(row_n)))
            csv_file.close()

            pair_string = "pair_{}".format(int(np.ceil(fly_n/n_inds)))

            if pair_string in os.listdir(os.getcwd()+"/data/csv/" + dt_string):
                pass
            else:
                os.mkdir(os.getcwd()+"/data/csv/"+dt_string+"/"+pair_string)

            os.rename(os.getcwd()+"/"+csv_name, os.getcwd()+"/data/csv/"+dt_string+"/"+pair_string+"/"+csv_name)

    return os.getcwd()+"/data/csv/"+dt_string

def pd_load_and_combine(dt_root_path)






if __name__=='__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--xlpath', type=str)
    args = parser.parse_args()

    path = args.xlpath
    csv_from_excel(path)
