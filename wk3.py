#!/usr/bin/env python

import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da
import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import pdb
import itertools

def getq(symbols=['GOOG','AAPL','GLD','XOM'],range=[dt.datetime(2011,1,1),dt.datetime(2011,12,31)]):
    """ retrieve adjusted close for symbols for given time range"""
    clstm=dt.timedelta(hours=16)
    tmstmp=du.getNYSEdays(range[0],range[1],clstm)
    yhoo=da.DataAccess('Yahoo',cachestalltime=0)
    #kys=['open', 'high', 'low', 'close', 'volume', 'actual_close']
    kys=['close']
    dat=yhoo.get_data(tmstmp,symbols,kys)
    ddat=dict(zip(kys, dat))  # dict indexed by data key, e.g. close, etc
    ret=ddat['close'].copy()
    ret=ret.fillna(method='ffill')
    ret=ret.fillna(method='bfill')
    ret=ret.values
    tsu.returnize0(ret)
    normpr=ddat['close'].copy()
    normpr=normpr/normpr.ix[0,:]
    return normpr,ret
    
def alloc(symbols=['GOOG','AAPL','GLD','XOM'],start=(2011,1,1),end=(2011,12,31),allocation=None):
    nsym=len(symbols)
    if allocation is None:
        allocation=np.ones((nsym,1))/float(nsym)
    else:
        allocation=np.array(allocation).reshape((-1,1))
    rng=[dt.datetime(*start),dt.datetime(*end)]  #could be more robust...
    normpr,ret=getq(symbols,rng)
    portnormpr=normpr.dot(allocation)
    portret=ret.dot(allocation)
    vol=np.std(portret)
    mnret=np.mean(portret)
    vol=np.std(portret)
    sharpe=np.sqrt(252)*mnret/vol  #annualized from daily returns
    cumret=portnormpr.values[-1][0]
    return {'meanreturn':mnret,'volatility':vol,'sharpe':sharpe,'cumulativeReturn':cumret}

def allochelper(normpr,ret,allocation):
    allocation=np.array(allocation).reshape((-1,1))
    portnormpr=normpr.dot(allocation)
    portret=ret.dot(allocation)
    vol=np.std(portret)
    mnret=np.mean(portret)
    vol=np.std(portret)
    sharpe=np.sqrt(252)*mnret/vol  #annualized from daily returns
    cumret=portnormpr.values[-1][0]
    return {'meanreturn':mnret,'volatility':vol,'sharpe':sharpe,'cumulativeReturn':cumret}
    
    
def dumboptimizer(symbols,start,end):
    nsym=len(symbols)
    rng=[dt.datetime(*start),dt.datetime(*end)]  #could be more robust...
    normpr,ret=getq(symbols,rng)
    fracts=np.arange(11)/10.0
    fractlist=[fracts]*nsym
    generator=(el for el in itertools.product(*fractlist) if abs(sum(el)-1)<.01)  #latter condition nod to float equality limitations
    maxsharpe=-float('inf')
    out=[]
    for al in generator:
        tmp=allochelper(normpr,ret,list(al))
        if tmp['sharpe']>maxsharpe:
            maxsharpe=tmp['sharpe']
            out=[al,tmp.copy()]
    return out
        