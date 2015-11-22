"""
 **********************************************************************
 * Copyright: (C) 2021-2023 International Atomic Energy Agency (IAEA) *
 * Author: Viktor Zerkin, V.Zerkin@iaea.org, (IAEA-NDS)               *
 **********************************************************************
"""
import json
#from pprint import pprint
import sys
sys.path.append('./')
from x4subr import *

print("Program: data1.py, ver. 2023-06-09")
print("Author:  V.Zerkin, IAEA-NDS, Vienna, 2023")
print("Purpose: find datasets by reaction, extract data in computational form\n")

base='./'

#Datasets=read_csv_file('EXFOR-Datasets.csv')
Datasets=read_csv_file('Datasets.csv')
nDatasets=len(Datasets)
print('-0-Datasets:'+str(nDatasets))

Datasets=filter_datasets(Datasets,'ReactionCode','13-AL-27(N,G)13-AL-28,,SIG')
nDatasets=len(Datasets)
print('-1-Datasets:'+str(nDatasets))
if (nDatasets<=0):
    print("---No data found---")
    sys.exit(2)

ii=0
for dataset in Datasets:
    entryfile=base+dataset['dir']+'/'+dataset['Entry']+'.x5.json'
    EntryID=dataset['Entry']
    SubentID=dataset['DatasetID'][:8]
    DatasetID=dataset['DatasetID']
    print(str(ii)+')\tFile:['+entryfile+'] Subent:'+SubentID+' Dataset:'+DatasetID)
    f=open(entryfile)
    Entry=json.load(f)
    ii+=1
    Subent=get_subent(Entry,SubentID)
    if (Subent is None): continue
    ds=get_dataset(Subent,DatasetID)
    if (ds is None): continue
    y=ds['c5data'].get('y')
    x1=ds['c5data'].get('x1')
    if (y is None): continue
    if (x1 is None): continue
    yy=y['y'];	dy=y.get('dy')
    xx1=x1['x1'];	dx1=x1.get('dx1')
    print('\tDataset:'+ds['DatasetID']+' '+str(ds['year1'])+','+ds['author1'])
    print('\t= y:',ds['quantExpan'],',',y['units'])
    print('\t yy:',yy)
    print('\t dy:',dy)
    print('\t=x1:',x1['expansion'],',',x1['units'])
    print('\txx1:',xx1)
    print('\tdx1:',dx1)
    #pprint(ds)
