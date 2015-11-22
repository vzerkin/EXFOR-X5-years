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

print("Program: index2entries.py, ver. 2023-07-11")
print("Author:  V.Zerkin, IAEA-NDS, Vienna, 2023")
print("Purpose: scan dir recursively, load x5.json,")
print("         produce Entry-index in JSON and CSV\n")

base=''
itot=0
entryLines=[]

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
            print(dirName+" "+str(ilevel+1)+" #"+str(nfiles)+"/"+str(itot)+" "+fullPath,end='')
            f=open(fullPath)
            Entry=json.load(f)
            entryLine={}
            entryLine['dir']=dirName
            entryLine['Entry']=Entry.get('ENTRY')
            entryLine['updated']=Entry.get('updated')
            x4subents=Entry.get('x4subents')
            nSubent=0;SPSDD=None
            if (x4subents is not None):
                nSubent=len(x4subents)
                try:
                    stats=x4subents[0]['BIB']['STATUS']
                    for stat1 in stats:
                        x4codes=stat1['x4codes']
                        for x4code1 in x4codes:
                            if x4code1['code']=='SPSDD': SPSDD='SPSDD'
                except Exception as ex:
                    SPSDD=None
            entryLine['nSubent']=nSubent
            entryLine['SPSDD']=SPSDD
            entryLine['year1']=Entry.get('y1')
            entryLine['author1']=Entry.get('a1')
            entryLine['doi1']=Entry.get('doi1')
            entryLine['x4Ref1']=Entry.get('r1')
            entryLine['Ref1']=Entry.get('ref')
            entryLine['Title']=Entry.get('title')

            print(" "+Entry['ENTRY']+' '+str(Entry.get('y1'))+' '+Entry.get('a1')+' ['+Entry.get('r1')+']')
            #print(" "+Entry['ENTRY']+' '+str(Entry.get('y1'))+','+Entry.get('a1')+','+Entry.get('ref'))
            #print("\t"+str(entryLine))
            entryLines.append(entryLine)
    print("End-----"+" dir:["+dirName+"] level:"+str(ilevel)+" ext:["+ext+"]"
	+" Total: sub-dirs:"+str(ndirs)+" files:"+str(nfiles)+"/"+str(itot))

processDir(base,'.x5.json',0)
print('Total Entries:',len(entryLines))

entryLines=sorted(entryLines, key=lambda i:i['Entry'])

with open('Entries.json','w') as outfile: json.dump(entryLines,outfile,indent=2)

cols=['dir','Entry','updated','nSubent','SPSDD','year1','author1','doi1','x4Ref1','Ref1','Title']
with open("Entries.csv", "w", newline="") as ff:
    writer=csv.DictWriter(ff,fieldnames=cols)
    writer.writeheader()
    writer.writerows(entryLines)

#cols=['dir','Entry','SPSDD','year1','author1','doi1','x4Ref1']
#cols=['Entry','author1','x4Ref1']
cols=['Entry','author1']
with open("Entries-short.csv", "w", newline="") as ff:
    writer=csv.DictWriter(ff,fieldnames=cols,extrasaction='ignore')
    writer.writeheader()
    writer.writerows(entryLines)
