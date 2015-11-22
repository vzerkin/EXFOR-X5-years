"""
 **********************************************************************
 * Copyright: (C) 2021-2023 International Atomic Energy Agency (IAEA) *
 * Author: Viktor Zerkin, V.Zerkin@iaea.org, (IAEA-NDS)               *
 **********************************************************************
"""
import os
import json
import sys
import csv

print("Program: index2datasets.py, ver. 2023-07-11")
print("Author:  V.Zerkin, IAEA-NDS, Vienna, 2023")
print("Purpose: scan dir recursively, load files *.x5.json,")
print("         produce Datasets-index in JSON and CSV\n")

base=''
itot=0
datasetLines=[]

"""
dir,Entry,DatasetID,updated,year1,author1,zTarg1,Targ1,Proj1,Emis1,ReactionType,MF,MT,nPoints,ReactionCode
100,10001,10001002,19990617,1969,R.W.Hockenbury+,13,Al-27,n,G,"CS",3,102,608,"13-AL-27(N,G)13-AL-28,,SIG,,RAW"
100,10001,10001003,19990617,1969,R.W.Hockenbury+,26,Fe-0,n,G,"CS",3,102,3264,"26-FE-0(N,G),,SIG,,RAW"
"""

def processDir(dirName,ext,ilevel):
    global itot
    print("Begin---"+" dir:["+dirName+"] level:"+str(ilevel)+" ext:["+ext+"]")
    if (dirName==''): listOfFiles=os.listdir('.')
    else: listOfFiles=os.listdir(dirName)
    nfiles=0;ndirs=0
    for file1 in listOfFiles:
        #if (itot>=30): break #uncomment for fast test
        fullPath=os.path.join(dirName,file1)
        fullPath=fullPath.replace('\\','/')
        if os.path.isdir(fullPath):
            ndirs+=1
            print(dirName+" "+str(ilevel+1)+" #"+str(ndirs)+" sub-dir: "+fullPath)
            processDir(fullPath,ext,ilevel+1)
        else:
            if not fullPath.endswith(ext): continue
            nfiles+=1
            itot+=1
            print('E:'+str(itot)+' Dir:'+dirName+" "+str(ilevel+1)+" #"+str(nfiles)+" "+fullPath)
            f=open(fullPath)
            Entry=json.load(f)
            entryLine={}
            entryLine['dir']=dirName
            entryLine['Entry']=Entry.get('ENTRY')
            entryLine['updated']=Entry.get('updated')
            x4subents=Entry.get('x4subents')
            if (x4subents is None): continue
            for subent in x4subents:
                if (subent is None): continue
                datasets=subent.get('datasets')
                if (datasets is None): continue
                for dataset in datasets:
                    datasetLine={}
                    datasetLine['dir']=dirName
                    datasetLine['Entry']=Entry.get('ENTRY')
                    datasetLine['DatasetID']=dataset.get('DatasetID')
                    datasetLine['updated']=subent.get('compiled')
                    datasetLine['year1']=dataset.get('year1')
                    datasetLine['author1']=Entry.get('a1')
                    datasetLine['zTarg1']=dataset.get('zTarg1')
                    datasetLine['Targ1']=dataset.get('targ1')
                    datasetLine['Proj1']=dataset.get('proj1')
                    datasetLine['Emis1']=dataset.get('emis1')
                    datasetLine['ReactionType']=dataset.get('ReactionType')
                    datasetLine['MF']=dataset.get('MF')
                    datasetLine['MT']=dataset.get('MT')
                    datasetLine['nPoints']=dataset.get('lc5data')
                    datasetLine['ReactionCode']=dataset.get('reacode')
                    print("\t"+datasetLine['DatasetID'].ljust(9)+' '+str(datasetLine['year1'])+' '+datasetLine['author1']+' '+dataset.get('reacode'))
                    #print("\t"+str(datasetLine))
                    datasetLines.append(datasetLine)
    print("End-----"+" dir:["+dirName+"] level:"+str(ilevel)+" ext:["+ext+"]"
	+" Total: sub-dirs:"+str(ndirs)+" files:"+str(nfiles)+"/"+str(itot))

processDir(base,'.x5.json',0)
print('Total Datasets:',len(datasetLines))


datasetLines=sorted(datasetLines, key=lambda i:i['DatasetID'])

with open('Datasets.json','w') as outfile: json.dump(datasetLines,outfile,indent=2)

cols=['dir','Entry','DatasetID','updated','year1','author1','zTarg1','Targ1','Proj1','Emis1','ReactionType','MF','MT','nPoints','ReactionCode']
with open("Datasets.csv", "w", newline="") as ff:
    writer=csv.DictWriter(ff,fieldnames=cols)
    writer.writeheader()
    writer.writerows(datasetLines)
