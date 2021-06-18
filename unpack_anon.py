
import glob
from os import path
from pydicom import dcmread
import zipfile
import tempfile
from pathlib import Path

pth='/home/cusackrh/mridata/zipdownloads'

allzips = glob.glob(path.join(pth,'*.zip'))

for file in allzips:
    # Unpack this zip to a temporary directory
    print(f'Extracting {file}')
    tmpdir = tempfile.mkdtemp(prefix='unpack_anon')
    with zipfile.ZipFile(file) as zip_ref:
        zip_ref.extractall(tmpdir)
    # Find every dcm
    for path in Path(tmpdir).rglob('*.dcm'):
        print(path)
    

