import copy
import matplotlib.pyplot as plt
import numpy as np
import sys
from helpers import styletools

def Histos1D(tuplelist,hmod,mask=None,**kwargs):
  '''
  tuplelist format: [(FileManager,{opt1:val1, opt2:val2, ...})]
  '''
  tuplelist,kwargs = ParseArgs(tuplelist,kwargs)

  fig = None
  ax  = None
  axratio = None 
  if len(tuplelist)>1 and kwargs['makeratio']:
    fig, (ax, axratio) = plt.subplots( 2,
                                       figsize     = styletools.figsize,
                                       sharex      = True,
                                       gridspec_kw = { 'hspace'       : 0,
                                                       'height_ratios': [4,1] } ) 
  else:
    fig, ax = plt.subplots(figsize=styletools.figsize)

  styletools.StyleHistos1D(ax,axratio)

  nlist       = []
  binslist    = [] 
  for fmopt in tuplelist:
    data   = fmopt[0].df[hmod.var]
    weight = None
    if hmod.weight is not None:
      weight = fmopt[0].df[hmod.weight]
    if mask is not None:
      data = data[mask]
      if weight is not None:
        weight = weight[mask]
    n,bins,_ = ax.hist( data,
                        weights  = weight,
                        bins     = hmod.nbins,
                        range    = (hmod.xlow,hmod.xhigh),
                        color    = fmopt[1]['color'],
                        histtype = fmopt[1]['opt'],
                        label    = fmopt[1]['label'],
                        density  = kwargs['norm'] )
    nlist.append(n)
    binslist.append(bins)

  plt.xlabel(hmod.xlabel,fontsize=14)
  ax.set_ylabel(hmod.ylabel,fontsize=14)
  if kwargs['xrange'] == [None,None]:
    ax.set_xlim([hmod.xlow,hmod.xhigh])
  else:
    ax.set_xlim(kwargs['xrange'])
  ax.set_ylim(kwargs['yrange'])
  ax.legend()

  ratiodata = {}
  if len(tuplelist)>1 and kwargs['makeratio']:
    for i in range(0,len(tuplelist)):
      if i == kwargs['ratio']: continue
      ratiodata[i] = np.array(nlist[i])/np.array(nlist[kwargs['ratio']])
    
    for idx in ratiodata:
      axratio.hist( binslist[idx][:-1],
                    binslist[idx],
                    weights  = ratiodata[idx],
                    color    = tuplelist[idx][1]['color'],
                    histtype = 'step' )
    if kwargs['xrange'] == [None,None]: 
      axratio.set_xlim([hmod.xlow,hmod.xhigh])
    else:
      axratio.set_xlim(kwargs['xrange'])
    axratio.set_ylim([kwargs['ratiorange'][0],kwargs['ratiorange'][1]])
    ylow, yhigh = axratio.get_ylim()
    tick_step = float(yhigh-ylow)/kwargs['rationydiv']
    axratio.yaxis.set_ticks(np.arange(ylow, yhigh, tick_step))
    axratio.set_ylabel(kwargs['ratiolabel'],fontsize=12)

def ScatterPlot(tuplelist,xhmod,yhmod,marker='.',s=1,alpha=1,maskname=None,**kwargs):
  tuplelist,kwargs = ParseArgs(tuplelist,kwargs)
  fig, ax = plt.subplots(figsize=styletools.figsize)  
  for fmopt in tuplelist:
    xdata = fmopt[0].df[xhmod.var]
    ydata = fmopt[0].df[yhmod.var]
    if maskname is not None:
      xdata = xdata[maskname]
      ydata = ydata[maskname]
    ax.scatter( x      = xdata,
                y      = ydata,
                marker = marker,
                s      = s,
                c      = fmopt[1]['color'],
                label  = fmopt[1]['label'],
                alpha  = alpha )
  plt.xlabel(xhmod.xlabel,fontsize=14)
  plt.ylabel(yhmod.xlabel,fontsize=14)
  ax.set_xlim([xhmod.xlow,xhmod.xhigh])
  ax.set_ylim([yhmod.xlow,yhmod.xhigh])
  plt.legend() 

def ContourPlot(tuplelist,xhmod,yhmod,nlevels=10,alpha=1,maskname=None,**kwargs):
  '''
  tuplelist format: [(FileManager,{opt1:val1, opt2:val2, ...})]
  '''
  # parse arguments
  tuplelist,kwargs = ParseArgs(tuplelist,kwargs) 
  fig, ax = plt.subplots(figsize=styletools.figsize) 
  lelms  = []
  labels = [] 
  for fmopt in tuplelist:
    # define x and y data
    xdata = fmopt[0].df[xhmod.var]
    ydata = fmopt[0].df[yhmod.var]  
    if len(xdata) != len(ydata):
      print('Error: xdata and ydata must have the same dimension.')
      sys.exit()
    # define weights
    if xhmod.weight != yhmod.weight:
      print('Error: xhmod and yhmod must have the same weight.')
      sys.exit()
    weight = []
    if xhmod.weight is not None:
      weight = fmopt[0].df[xhmod.weight]
    else:
      weight = np.ones(len(xdata))
    # apply additional mask (if specified)
    if maskname is not None:
      xdata = xdata[maskname]
      ydata = ydata[maskname]
      weight = weight[maskname]
    # create 2D histogram
    counts,_,_ = np.histogram2d( x       = xdata,
                                 y       = ydata,
                                 weights = weight,
                                 bins    = [xhmod.nbins,yhmod.nbins],
                                 range   = [[xhmod.xlow,xhmod.xhigh],[yhmod.xlow,yhmod.xhigh]],
                                 density = kwargs['norm'] )
    # create contour lines from h2d counts
    m = np.amax(counts)
    step = m/nlevels
    levels = np.arange(0.0, m, step) + step
    idx = tuplelist.index(fmopt)
    
    c = plt.contour( counts.transpose(),
                     levels = levels,
                     colors = fmopt[1]['color'], 
                     extent = [xhmod.xlow,xhmod.xhigh,yhmod.xlow,yhmod.xhigh],
                     alpha  = alpha ) 
    # handle legend entries
    lelm,_ = c.legend_elements()
    lelms.append( lelm[0] )
    labels.append( fmopt[1]['label'] )

  plt.xlabel(xhmod.xlabel,fontsize=14)
  plt.ylabel(yhmod.xlabel,fontsize=14)
  ax.set_xlim([xhmod.xlow,xhmod.xhigh])
  ax.set_ylim([yhmod.xlow,yhmod.xhigh])
  ax.legend(lelms, labels) 

def ParseArgs(tuplelist,kwargs):
  tuplelist_new = []
  for fmopt in tuplelist:
    extrainfo = copy.copy(kwargs)
    if type(fmopt) == tuple:
      extrainfo.update(fmopt[1])
    tuplelist_new.append((fmopt[0],extrainfo))
  tuplelist = tuplelist_new
  for fmopt in tuplelist:
    if 'opt'   not in fmopt[1]: fmopt[1]['opt']   = 'step'
    if 'label' not in fmopt[1]: fmopt[1]['label'] = ''
    if 'color' not in fmopt[1]: fmopt[1]['color'] = 'C'+str(tuplelist.index(fmopt))
  if 'norm'       not in kwargs: kwargs['norm']       = False
  if 'xrange'     not in kwargs: kwargs['xrange']     = [None,None]
  if 'yrange'     not in kwargs: kwargs['yrange']     = [None,None]
  if 'ratio'      not in kwargs: kwargs['ratio']      = 0
  if 'makeratio'  not in kwargs: kwargs['makeratio']  = True
  if 'ratiorange' not in kwargs: kwargs['ratiorange'] = [None,None]
  if 'ratiolabel' not in kwargs: kwargs['ratiolabel'] = ''
  if 'rationydiv' not in kwargs: kwargs['rationydiv'] = 4
  if 'text'       not in kwargs: kwargs['text']       = ''
  return tuplelist,kwargs
