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

    for i in range(book.nsheets):
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

def pd_load_and_combine(dt_root_path):
    list_of_dirs = [x[0] for x in os.walk(dt_root_path)]
    for dir in list_of_dirs:
        print(dir)
        if dir.split('/')[-1].startswith('pair'):
            os.chdir(dir)
            list_of_dataframes = []
            for i, file in enumerate([x for x in os.listdir(os.getcwd())]):
                df = pd.read_csv(os.getcwd() + "/"+file)
                keep_cols = ['pos x', 'pos y', 'ori',  'wing l x',
                             'wing l y', 'wing r x', 'wing r y',
                             'wing l ang','wing r ang', 'vel',
                             'ang_vel', 'min_wing_ang',
                             'max_wing_ang', 'dist_to_wall', 'dist_to_other',
                             'angle_between','facing_angle', 'leg_dist']
                # Rename columns that are exculsive to one fly and reasssign
                # dataframe with new column sheet
                col_list = []
                for col_name in keep_cols:
                    if col_name not in ['dist_to_other','angle_between', 'leg_dist']:
                        col_list.append('Fly{} '.format(i+1) + col_name)
                    else:
                        col_list.append(col_name)
                new_df = pd.DataFrame(df[keep_cols]).copy()
                new_df.columns=col_list
                list_of_dataframes.append(new_df)

            joint_df = pd.DataFrame()
            for j, dataframe in enumerate(list_of_dataframes):
                if j==0:
                    joint_df = list_of_dataframes[0]
                else:
                    joint_df = joint_df.merge(list_of_dataframes[1])

            transform_cols = ['Fly1 pos x', 'Fly1 pos y', 'Fly1 wing l x', 'Fly1 wing l y', 'Fly1 wing r x', 'Fly1 wing r y',
                              'Fly2 pos x', 'Fly2 pos y', 'Fly2 wing l x', 'Fly2 wing l y', 'Fly2 wing r x', 'Fly2 wing r y']



            # this probably isnt the best way to do this...
            # need to normalize to arenas somehow for positions
            # does the tracker output arena params somewhere?
            # what are the units here scaled to?
            # mm?


            def sub_min(key):
                joint_df[key] = joint_df[key] - joint_df[key].min()

            for tcol in transform_cols:
                sub_min(tcol)


            print(joint_df['Fly2 wing l y'])











if __name__=='__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--xlpath', type=str)
    args = parser.parse_args()

    path = args.xlpath
    # dt_path = csv_from_excel(path)
    pd_load_and_combine('/home/patrick/Desktop/behavior-net/data/csv/12_20_2018_1057')
