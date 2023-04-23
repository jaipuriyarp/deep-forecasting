import os
import argparse
import pandas as pd
import yaml
import math
from pathlib import Path

with open("../model/params.yaml", "r") as params_file:
    params = yaml.safe_load(params_file)

data_dir = params['data_dir']

def load_data(
        file_name
):
    data = pd.read_csv(Path(data_dir, file_name))
    return data


def addLabel(
        data,
        colName
):
    col = data[colName]
    label = [1 if math.isnan(x) else -1 for x in col]
    data['Label'] = label
    return data

def cleanData(
    data,
    colNameForTrain
):
    column_names = list(data.columns.values)
    columnToPreserve = [colNameForTrain, 'Label']
    for x in column_names:
        if x not in columnToPreserve:
            data = data.drop(columns=x)

    return data

def preprocessData(
    data,
    colNameForLabel='Gann Swing High Plots-Triangles Down Top of Screen',
    colNameForTrain='close'
):
    dataLabelled = addLabel(data, colNameForLabel)
    data_clean = cleanData(dataLabelled,colNameForTrain)
    data_clean.rename(columns={"close": "Close"},inplace=True)
    # print (dataLabelled)
    return data_clean

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file-name", type=str, default=params['file_name'])
    # parser.add_argument("--train-frac", type=float, default=params['train_frac'])
    args = parser.parse_args()

    df = load_data(args.file_name)
    final_data = preprocessData(df)
    newFile = args.file_name.strip(".csv") + "_closePriceNLabel.csv"
    final_data.to_csv(Path(data_dir, newFile), index=False)
    print("INFO: File: " + newFile + "saved to the dir: " + data_dir)