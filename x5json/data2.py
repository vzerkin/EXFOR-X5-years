"""
 ***********************************************************************************
 * Copyright (C) 2021-2023 International Atomic Energy Agency (IAEA)               *
 *-----------------------------------------------------------------------------    *
 * Permission is hereby granted, free of charge, to any person obtaining a copy    *
 * of this software and associated documentation files (the "Software"), to deal   *
 * in the Software without restriction, including without limitation the rights    *
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell       *
 * copies of the Software, and to permit persons to whom the Software is furnished *
 * to do so, subject to the following conditions:                                  *
 *                                                                                 *
 * The above copyright notice and this permission notice shall be included in all  *
 * copies or substantial portions of the Software.                                 *
 *                                                                                 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR      *
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,        *
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE     *
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER          *
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,   *
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN       *
 * THE SOFTWARE.                                                                   *
 *                                                                                 *
 *-----------------------------------------------------------------------------    *
 *   AUTHOR:                                                                       *
 *   Viktor Zerkin, PhD                                                            *
 *   e-mail: V.Zerkin@iaea.org                                                     *
 *   International Atomic Energy Agency                                            *
 *   Nuclear Data Section, P.O.Box 100                                             *
 *   Wagramerstrasse 5, Vienna A-1400, AUSTRIA                                     *
 *   Phone: +43 1 2600 21714; Fax: +43 1 26007                                     *
 *                                                                                 *
 ***********************************************************************************
"""

import datetime
import json
import sys
sys.path.append('./')
from x4subr import *
import plotly
from plotly.graph_objs import Scatter, Layout 
from pprint import pprint

print("Program: data2.py, ver. 2024-02-26")
print("Author:  V.Zerkin, IAEA-NDS, Vienna, 2023")
print("Purpose: find datasets by reaction, load X5-json, extract data, plot by Plotly\n")

ct=str(datetime.datetime.now())[:19]
print("Running: "+ct+"\n")
#input("Press the <ENTER> key to continue...")

base='./'

def sort_ya1(ds):
    rr=str(ds['year1'])+','+ds['author1ini']+ds['author1']
    return rr

#datasets=read_csv_file('EXFOR-Datasets.csv')
datasets=read_csv_file('Datasets.csv')
nDatasets=len(datasets)
print('-0-Datasets:'+str(nDatasets))

#reacode='13-AL-27(N,TOT),,SIG'
#reacode='13-AL-27(N,G)13-AL-28,,SIG'
reacode='13-AL-27(N,A)11-NA-24,,SIG'

datasets=filter_datasets(datasets,'ReactionCode',reacode)
nDatasets=len(datasets)
print('-1-Datasets:'+str(nDatasets))
if (nDatasets<=0):
    print("---No data found---")
    sys.exit(2)

xtitle=''; ytitle=''
dss=[];ii=0
for dataset in datasets:
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
    yy=y['y'];		dy=y.get('dy')
    xx1=x1['x1'];	dx1=x1.get('dx1')
    print('\tDataset:'+ds['DatasetID']+' '+str(ds['year1'])+','+ds['author1'])
    ytitle=ds['quantExpan']+' ('+y['units']+')'
    xtitle=x1['expansion']+' ('+x1['units']+')'
    print('\t|||y:',ds['quantExpan'],',',y['units'])
    print('\t||yy:',yy)
    print('\t||dy:',dy)
    print('\t||x1:',x1['expansion'],',',x1['units'])
    print('\t|xx1:',xx1)
    print('\t|dx1:',dx1)
    #pprint(ds)
    ds['y']=yy;  ds['dy']=dy
    ds['x']=xx1; ds['dx']=dx1
    ds['x4lbl']=str(ds['year1'])+' '+ds['author1ini']+ds['author1']
    dss.append(ds)
dss=sorted(dss,key=sort_ya1,reverse=True)

#_________________Preparing EXFOR data for plot_________________
data1=[]; ii=0
for ds in dss:
    tr=Scatter(x=ds['x'],y=ds['y']
	,text=ds['x4lbl']
	,name=str(ii+1)+') '+ds['x4lbl']+' pt:'+str(len(ds['x']))+' #'+ds['DatasetID']
	,marker_symbol=str(ii%33)
	,marker_size=8
	,mode="markers"
	)
    if (ds['dy'] is not None): tr.error_y=dict(type='data',array=ds['dy'],visible=True,thickness=0.9)
    if (ds['dy'] is not None): tr.error_x=dict(type='data',array=ds['dx'],visible=True,thickness=0.9)
    data1.append(tr)
    ii+=1

xtype='linear';ytype='linear'
xtype='log'#;ytype='log'
plotTitle=reacode;

#_________________Plot data from EXFOR_________________
plot1={}
plot1['data']=data1
xaxis=dict(title=xtitle,showline=True,linecolor='black',ticks='outside'
,showgrid=True,gridcolor='#aaaaaa',type=xtype)
yaxis={'title':ytitle,'showline':True,'linecolor':'black'
	,'showgrid':True, 'gridcolor':'#aaaaaa','ticks':'outside','type':ytype
	,'zeroline':True, 'zerolinecolor':'#dddddd'#, 'zerolinewidth':0.1
}
xaxis['mirror']='ticks'
yaxis['mirror']='ticks' 
plot1['layout']=Layout(title='EXFOR cross sections \u03c3(E): '+plotTitle
	+'  #Datasets:'+str(nDatasets)
	+'<br><i>X5json, by V.Zerkin, IAEA-NDS, 2021-2024, ver.2024-02-26 //running:'+ct+'</i>'
	,xaxis=xaxis,yaxis=yaxis
	,plot_bgcolor='white'
	,legend=dict(traceorder="grouped")
)

outhtml='data2'
plotly.offline.plot(plot1,filename=outhtml+'.html')
