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
import copy
import QSTK.qstkstudy.EventProfiler as ep

# Get the data from the data store
storename = "Yahoo" # get data from our daily prices source
# Available field names: open, close, high, low, close, actual_close, volume
closefield = "actual_close"

def fivebucks(symbols, startday,endday, verbose=False,threshold=5.0):

    # Reading the Data for the list of Symbols.    
    timeofday=dt.timedelta(hours=16)
    timestamps = du.getNYSEdays(startday,endday,timeofday)
    dataobj = da.DataAccess(storename)
    if verbose:
            print __name__ + " reading data"
    # Reading the Data
    close = dataobj.get_data(timestamps, symbols, closefield)
    
    # Completing the Data - Removing the NaN values from the Matrix
    close = (close.fillna(method='ffill')).fillna(method='backfill')

    
    # Calculating Daily Returns for the Market
    #tsu.returnize0(close.values)
    
    
    events=copy.deepcopy(close)
    events*=np.NAN
    for sym in symbols:
        for i in range(1,len(timestamps)):
            if close[sym].ix[i-1]>=threshold and close[sym].ix[i]<threshold:
                events[sym].ix[i]=1
    
          
    return events,{'close':close}

def q1():
    sym2008 = np.loadtxt('C:\Anaconda\Lib\site-packages\QSTK\QSData\Yahoo\Lists\sp5002008.txt',dtype='S10',comments='#')
    sym2012 = np.loadtxt('C:\Anaconda\Lib\site-packages\QSTK\QSData\Yahoo\Lists\sp5002012.txt',dtype='S10',comments='#')

    # You might get a message about some files being missing, don't worry about it.

    #symbols =['BFRE','ATCS','RSERF','GDNEF','LAST','ATTUF','JBFCF','CYVA','SPF','XPO','EHECF','TEMO','AOLS','CSNT','REMI','GLRP','AIFLY','BEE','DJRT','CHSTF','AICAF']
    startday = dt.datetime(2008,1,1)
    endday = dt.datetime(2009,12,31)
    events2008,close2008 = fivebucks(sym2008,startday,endday,verbose=True)
    events2012,close2012 = fivebucks(sym2012,startday,endday,verbose=True)

    eventprof2008 = ep.eventprofiler(events2008,close2008,20,20,"fivebucks2008stocks.pdf",False,True)
    eventprof2012 = ep.eventprofiler(events2012,close2012,20,20,"fivebucks2012stocks.pdf",False,True)

def q2():
    sym2008 = np.loadtxt('C:\Anaconda\Lib\site-packages\QSTK\QSData\Yahoo\Lists\sp5002008.txt',dtype='S10',comments='#')
    startday = dt.datetime(2008,1,1)
    endday = dt.datetime(2009,12,31)
    events2008,close2008 = fivebucks(sym2008,startday,endday,True,10.0)
    eventprof2008 = ep.eventprofiler(events2008,close2008,20,20,"tenbucks2008stocks.pdf",False,True)

def q3():
    sym2012 = np.loadtxt('C:\Anaconda\Lib\site-packages\QSTK\QSData\Yahoo\Lists\sp5002012.txt',dtype='S10',comments='#')
    startday = dt.datetime(2008,1,1)
    endday = dt.datetime(2009,12,31)
    events2012,close2012 = fivebucks(sym2012,startday,endday,True,9.0)
    eventprof2012 = ep.eventprofiler(events2012,close2012,20,20,"ninebucks2012stocks.pdf",False,True)
        