import copy, warnings
import matplotlib.pyplot as plt
import numpy as np
from helpers import styletools
from helpers import textboxtools
from helpers import modeltools

def Histos1D(tuplelist,model,maskname=None,**kwargs):
  '''
  tuplelist format: [(FileManager,{opt1:val1, opt2:val2, ...})]
  '''

  nbins   = None
  x_range = None
  xlabel  = None
  ylabel  = None
  if not isinstance(model,list):
    if not isinstance(model,modeltools.h1DModel):
      raise TypeError('Argument model must be instance of modeltools.h1DModel.')
    nbins   = model.nbins
    x_range = model.x_range
    xlabel  = model.xlabel
    ylabel  = model.ylabel
  else:
    if len(model)==0: raise TypeError('Argument model must be list of modeltools.h1DModel.')
    if len(model)!=len(tuplelist): raise ValueError('Arguments tuplelist and model have different size.') 
    for hmod in model:
      if not isinstance(hmod, modeltools.h1DModel): raise TypeError('Argument model must be list of modeltools.h1DModel.')
      if (hmod.nbins!=model[0].nbins) or (hmod.x_range!=model[0].x_range):
        raise ValueError('Models in the list must share the same nbins and x_range.')
    nbins   = model[0].nbins
    x_range = model[0].x_range
    xlabel  = model[0].xlabel
    ylabel  = model[0].ylabel

  tuplelist,kwargs = ParseArgs(tuplelist,kwargs)

  fig = None
  ax  = None
  axratio = None 
  if len(tuplelist)>1 and kwargs['makeratio']:
    fig, (ax, axratio) = plt.subplots( 2,
                                       figsize     = styletools.figsize,
                                       sharex      = True,
                                       gridspec_kw = { 'hspace'       : 0,
                                                       'height_ratios': kwargs['heightratios'] } ) 
  else:
    fig, ax = plt.subplots(figsize=styletools.figsize)

  styletools.StyleHistos1D(ax,axratio)

  nlist       = []
  binslist    = []
  for fmopt in tuplelist:
    var = None
    idx = tuplelist.index(fmopt)
    if not isinstance(model,list): var = model.var
    else: var = model[idx].var
    data   = fmopt[0].df[var]
    weight = fmopt[1]['weight']
    if weight is not None:
      weight = fmopt[0].df[weight]
    if maskname is not None:
      data = data[fmopt[0].df[maskname]]
      if weight is not None:
        weight = weight[fmopt[0].df[maskname]]
    n,bins,_ = ax.hist( data,
                        weights  = weight,
                        bins     = nbins,
                        range    = x_range,
                        color    = fmopt[1]['color'],
                        histtype = fmopt[1]['opt'],
                        label    = fmopt[1]['label'],
                        density  = kwargs['norm'] )
    nlist.append(n)
    binslist.append(bins)

  if kwargs['logy']: ax.set_yscale('log')
  plt.xlabel(xlabel,fontsize=14)
  ax.set_ylabel(ylabel,fontsize=14)
  if kwargs['xrange'] == [None,None]:
    ax.set_xlim(x_range)
  else:
    ax.set_xlim(kwargs['xrange'])
  ax.set_ylim(kwargs['yrange']) 
  ax.legend()

  # make text box
  if kwargs['textbox']:
    textstr   = textboxtools.MakeTextBox()
    xpos,ypos = textboxtools.pos
    ax.text(xpos, ypos, textstr, transform=ax.transAxes, fontsize=textboxtools.fontsize,
        verticalalignment='top') 

  # make ratio plot
  ratiodata  = {}
  if len(tuplelist)>1 and kwargs['makeratio']:
    for i in range(0,len(tuplelist)):
      if i == kwargs['ratio']: continue
      with warnings.catch_warnings():
        warnings.filterwarnings('ignore', 'divide by zero encountered in true_divide', RuntimeWarning)
        warnings.filterwarnings('ignore', 'invalid value encountered in true_divide' , RuntimeWarning) 
        ratiodata[i] = np.array(nlist[i])/np.array(nlist[kwargs['ratio']]) 
    for idx in ratiodata:
      maskfinite = [ (not np.isnan(x)) and (x!=np.inf) for x in ratiodata[idx] ] # determine finite ratio values   
      axratio.hist( x        = binslist[idx][:-1][maskfinite], # initialize with 1 entry per finite bin
                    bins     = binslist[idx],                  # use same binning as original histos
                    weights  = ratiodata[idx][maskfinite],     # weight the only entry per bin by the ratio values
                    color    = tuplelist[idx][1]['color'],
                    histtype = 'step' )
    if kwargs['xrange'] == [None,None]: 
      axratio.set_xlim(x_range)
    else:
      axratio.set_xlim(kwargs['xrange'])
    axratio.set_ylim([kwargs['ratiorange'][0],kwargs['ratiorange'][1]])
    ylow, yhigh = axratio.get_ylim()
    tick_step = float(yhigh-ylow)/kwargs['rationydiv']
    axratio.yaxis.set_ticks(np.arange(ylow, yhigh, tick_step))
    axratio.set_ylabel(kwargs['ratiolabel'],fontsize=12)

  # save plot
  if kwargs['saveas'] is not None:
    for ext in kwargs['ext']:
      figname = '{}{}'.format(kwargs['saveas'],ext)
      print('Saving figure: '+figname)
      plt.savefig(figname)

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
  ax.set_xlim(xhmod.x_range)
  ax.set_ylim(yhmod.x_range)
  plt.legend() 

def ContourPlot(tuplelist,xhmod,yhmod,nlevels=10,alpha=1,maskname=None,**kwargs):
  '''
  tuplelist format: [(FileManager,{opt1:val1, opt2:val2, ...})]
  '''
  # parse arguments
  tuplelist,kwargs = ParseArgs(tuplelist,kwargs) 
  fig, ax = plt.subplots(figsize=styletools.figsize)
  styletools.StyleContourPlot(ax) 
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
    weight = fmopt[1]['weight']
    if weight is not None:
      weight = fmopt[0].df[weight]
    else:
      weight = np.ones(len(xdata))
    # apply additional mask (if specified)
    if maskname is not None:
      xdata  = xdata[maskname]
      ydata  = ydata[maskname]
      if weight is not None:
        weight = weight[maskname]
    # create 2D histogram
    counts,_,_ = np.histogram2d( x       = xdata,
                                 y       = ydata,
                                 weights = weight,
                                 bins    = [xhmod.nbins,yhmod.nbins],
                                 range   = [xhmod.x_range,yhmod.x_range],
                                 density = kwargs['norm'] )
    # create contour lines from h2d counts
    m = np.amax(counts)
    step = m/nlevels
    levels = np.arange(0.0, m, step) + step
    idx = tuplelist.index(fmopt)
    
    c = plt.contour( counts.transpose(),
                     levels = levels,
                     colors = fmopt[1]['color'], 
                     extent = [xhmod.x_range[0],xhmod.x_range[1],yhmod.x_range[0],yhmod.x_range[1]],
                     alpha  = alpha ) 
    # handle legend entries
    lelm,_ = c.legend_elements()
    lelms.append( lelm[0] )
    labels.append( fmopt[1]['label'] )

  plt.xlabel(xhmod.xlabel,fontsize=14)
  plt.ylabel(yhmod.xlabel,fontsize=14)
  ax.set_xlim(xhmod.x_range)
  ax.set_ylim(yhmod.x_range)
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
    if 'opt'    not in fmopt[1]: fmopt[1]['opt']    = 'step'
    if 'label'  not in fmopt[1]: fmopt[1]['label']  = ''
    if 'color'  not in fmopt[1]: fmopt[1]['color']  = 'C'+str(tuplelist.index(fmopt))
    if 'weight' not in fmopt[1]: fmopt[1]['weight'] = None
  if 'norm'         not in kwargs: kwargs['norm']         = False
  if 'xrange'       not in kwargs: kwargs['xrange']       = [None,None]
  if 'yrange'       not in kwargs: kwargs['yrange']       = [None,None]
  if 'logy'         not in kwargs: kwargs['logy']         = False
  if 'ratio'        not in kwargs: kwargs['ratio']        = 0
  if 'makeratio'    not in kwargs: kwargs['makeratio']    = True
  if 'ratiorange'   not in kwargs: kwargs['ratiorange']   = [None,None]
  if 'ratiolabel'   not in kwargs: kwargs['ratiolabel']   = ''
  if 'rationydiv'   not in kwargs: kwargs['rationydiv']   = 4
  if 'heightratios' not in kwargs: kwargs['heightratios'] = [3,1]
  if 'textbox'      not in kwargs: kwargs['textbox']      = False
  if 'saveas'       not in kwargs: kwargs['saveas']       = None
  if 'ext'          not in kwargs: kwargs['ext']          = ['.pdf','.png']
  return tuplelist,kwargs
