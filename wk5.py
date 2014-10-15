#!/usr/bin/env python

import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da

import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import sys
import pdb

def runwk5(budget=10000,orderfn='orders.csv',outfn='portfoliovalue.csv'):
    
    budget=int(budget)
    orderm=pd.read_csv(orderfn,index_col=False,names=['year','month','day','symbol','action','shares'])
    outfh=open(outfn,'w')
    pdb.set_trace()
    syms=list(set(orderm['symbol']))
    
    orderm['date']=[dt.datetime(*x[:3]) for x in orderm.iterrows()]
    startd=min(orderm['date'])
    stopd=max(orderm['date']+1)
    closet=du.timedelta(hours=16)
    days=du.getNYSEdays(startd,stopd,closet)

    yhoo=da.DataAccess('Yahoo')
    ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
    data = yhoo.get_data(days, syms, ls_keys)
    datadict = dict(zip(ls_keys, data))

    columns=syms+['cash']
    unitdf=pd.DataFrame(index=days,columns=columns)
    valuedf=pd.DataFrame(index=days,columns=columns)