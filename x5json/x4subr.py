"""
 **********************************************************************
 * Copyright: (C) 2021-2023 International Atomic Energy Agency (IAEA) *
 * Author: Viktor Zerkin, V.Zerkin@iaea.org, (IAEA-NDS)               *
 **********************************************************************
"""
import csv

def read_csv_file(filename):
    reader=csv.reader(open(filename,'r'))
    array=[]
    ii=0
    for row in reader:
        #print(str(ii),'\t',row)
        if (ii==0): header=row;
        else:
            dict1={}
            for i in range(len(header)):
                key=header[i]
                val=row[i]
                dict1[key]=val
            array.append(dict1)
        ii+=1
    return array

def filter_datasets(datasets,nam,val):
    array=[]
    ii=0
    for dataset in datasets:
        #print(str(ii),'\t',dataset)
        xx=dataset.get(nam)
        #print(str(ii),'\txx:',xx)
        if xx is None: continue;
        if (xx!=val): continue
        array.append(dataset)
        ii+=1
        if (True): continue
        print(str(ii)+'\t'+dataset['dir']+'/'+dataset['Entry']+' sub:'+dataset['DatasetID'][:8]
	+' ds:'+dataset['DatasetID'].ljust(9)+' '+dataset['year1']+','+dataset['author1']
#	+' pt:'+dataset['nPoints']
	)
    return array

def get_subent(Entry,SubentID):
    x4subents=Entry["x4subents"]
    if (x4subents is None): return None
    for Subent in x4subents:
        #print('  SUBENT:'+Subent['SUBENT']+' compiled:'+str(Subent['compiled'])+' TransDate:'+str(Subent['TransDate']))
        if (Subent['SUBENT']==SubentID): return Subent
    return None

def get_dataset(Subent,DatasetID):
    datasets=Subent.get('datasets')
    if (datasets is None): return None
    for ds in datasets:
        if (ds['DatasetID']==DatasetID): return ds
    return None
