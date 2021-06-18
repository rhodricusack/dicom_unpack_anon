
'''
Anomymisation tool for DICOM data from Orthanc.
Unzips DICOM files, removes PatientID and PatientBirthDate, and writes files in new directory structure of form [participant id]/Series_[SeriesNumber]_[SeriesDescription]
Rhodri Cusack, Trinity College Dublin 2021-06-18, cusackrh@tcd.ie
'''

import glob
from os import path
from pydicom import dcmread
import zipfile
import tempfile
from pathlib import Path
import os
import requests
from io import BytesIO 

pth='/home/cusackrh/mridata/zipdownloads'
outpth='/home/cusackrh/mrianon'
donepth = outpth + '/downloaded'

# Make directory in which to record which series have already been processed
os.makedirs(donepth, exist_ok=True)

# Get a list of all series in Orthanc
response = requests.get('https://hprc-guest-114-231.tchpc.tcd.ie/series')
if not response.ok:
    raise Exception('Error downloading series list')

# Process each of the series
for series in response.json():
    doneflag=path.join(donepth, series+'.done')
    if path.exists(doneflag):
        print(f'Already done {series}')
    else:
        print(f'Working on {series}')
        response = requests.get(f'https://hprc-guest-114-231.tchpc.tcd.ie/series/{series}/archive')
        if not response.ok:
            print('Error retrieving series - ignoring')
        else:
            zipdata = BytesIO()
            zipdata.write(response.content)
    
            # Unpack this zip to a temporary directory
            
            tmpdir = tempfile.mkdtemp(prefix='unpack_anon')
            with zipfile.ZipFile(zipdata) as zip_ref:
                zip_ref.extractall(tmpdir)
            
            # Find every dcm
            for fle in Path(tmpdir).rglob('*.dcm'):
                print(fle)
                dcm = dcmread(fle)

                # Only these fields removed
                dcm.PatientName = dcm.PatientID
                dcm.PatientBirthDate = '00000000'
                dcm.PatientWeight = '00.0'

                # Make output directory
                seriespth = path.join(outpth, dcm.PatientID, 'Series_' + str(dcm.SeriesNumber) + '_' + dcm.SeriesDescription)
                os.makedirs(seriespth, exist_ok=True)

                # Save anonymized file
                dcm.save_as(path.join(seriespth, path.basename(fle)))

            # Write done flag to mark this Zip as successfully processed. 
            with open(doneflag,'w') as f:
                f.writelines('Done')
