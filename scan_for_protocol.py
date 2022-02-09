
'''
Dump protocol details
Rhodri Cusack, Trinity College Dublin 2021-06-18, cusackrh@tcd.ie
'''

from os import path
from pydicom import dcmread
from pathlib import Path
import os
from io import BytesIO 
import pandas as pd
import requests

fle = 'series_details.tsv'
df=pd.DataFrame()
if path.exists(fle):
    with open(fle,'r') as f:
        df = pd.read_csv(f, sep='\t')
else:
    # Get a list of all series in Orthanc
    response = requests.get('https://hprc-guest-114-231.tchpc.tcd.ie/series')
    if not response.ok:
        raise Exception('Error downloading series list')

    allseries=response.json()


    # Process each of the series
    allprotocolnames=[]
    cols=['ProtocolName', 'SeriesDescription', 'SequenceName']

    # Header, tab delimited
    print('Series', end='\t')
    for col in cols:
        print(col, end='\t')

    # Go through each series
    df=pd.DataFrame()



    print(f"Total number of series: {len(allseries)}")

    for series in allseries:
        response = requests.get(f'https://hprc-guest-114-231.tchpc.tcd.ie/series/{series}')
        tags=response.json()['MainDicomTags']
        tags['series'] = series
        df = df.append(tags, ignore_index=True)


# Write out
df_selected = df[['ProtocolName', 'SequenceName', 'SeriesDescription']]
df.to_csv('series_details.tsv', sep='\t', index=False)
df_selected.to_csv('series_details_selected.tsv', sep='\t', index=False)
df_selected = df_selected.groupby(df_selected.columns.tolist(),as_index=False).size()
df_selected = df_selected.sort_values('SeriesDescription')
df_selected = df_selected.to_csv('series_details_selected_unique.tsv', sep='\t', index=False)
