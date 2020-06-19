import uproot
import numpy as np
import matplotlib.pyplot as plt
import sys

class h1DModel:
  def __init__( self,
                var,
                nbins,
                xlow,
                xhigh,
                weight = '',
                xlabel = '',
                ylabel = 'Events' ):
    if xlow >= xhigh:
      print('Error: xlow is greater than xhigh.')
      sys.exit()
    self.var    = var
    self.nbins  = nbins
    self.xlow   = xlow
    self.xhigh  = xhigh
    self.weight = weight
    self.xlabel = xlabel
    self.ylabel = ylabel

class fileService:
  def __init__(self,filepathname,treename,label):
    self.filepathname = filepathname
    self.file         = uproot.open(filepathname)
    if self.file==None:
      print('Error: no file found at {}'.format(filepathname))
      sys.exit()
    self.tree = self.file[treename]
    if self.tree==None:
      print('Error: no tree found with name {}'.format(treename))
      sys.exit()
    self.branches = self.tree.arrays(namedecode='utf-8')
    self.label    = label

def SimplePlot( fileServiceList,
                hmodel,
                figsize  = (8,6),
                style    = 'white',  
                text     = '',
                histtype = 'step',
                norm     = False ):
  if len(fileServiceList)==0:
    print('Error: no files specified.')
    sys.exit()
  # prepare figure and plot style
  fig,ax = plotStyle(figsize,style)
  plt.xticks( np.arange(hmodel.xlow,hmodel.xhigh+float(hmodel.xhigh-hmodel.xlow)/10,step = float(hmodel.xhigh-hmodel.xlow)/10) )
  # axis labels
  plt.xlabel(hmodel.xlabel,fontsize=14)
  if norm == False:
    plt.ylabel(hmodel.ylabel,fontsize=14)
  else:
    plt.ylabel('Normalised',fontsize=14)
  # add ATLAS label
  ax.text(0.05, 0.95, text, transform=ax.transAxes, fontsize=14, verticalalignment='top')
  # loop over data
  for fs in fileServiceList:
    if hmodel.var not in fs.branches:
      print('Error: variable {} not found in file {}.'.format(hmodel.var,fs.filepathname))
      sys.exit()
    # create histograms
    if hmodel.weight=='':
      n,bins,patches = plt.hist( fs.branches[hmodel.var],
                                 bins     = hmodel.nbins,
                                 range    = (hmodel.xlow,hmodel.xhigh),
                                 histtype = histtype,
                                 label    = fs.label,
                                 density  = norm
                               )
    else:
      if hmodel.weight not in fs.branches:
        print('Error: weight {} not found in file {}.'.format(hmodel.weight,fs.filepathname))
        sys.exit()
      n,bins,patches = plt.hist( fs.branches[hmodel.var],
                                 weights  = fs.branches[hmodel.weight],
                                 bins     = hmodel.nbins,
                                 range    = (hmodel.xlow,hmodel.xhigh),
                                 histtype = histtype,
                                 label    = fs.label,
                                 density  = norm
                               )
  # set limits on axes
  ax.set_ylim([0,None])
  ax.set_xlim([hmodel.xlow,hmodel.xhigh])
  # show legend
  plt.legend()
  return fig,ax

def plotStyle(figsize=(8,6),style='white'):
  fig, ax = plt.subplots(figsize=figsize)
  # background and grid lines
  if style == 'white':
    ax = plt.axes(facecolor='w')
    plt.grid(color='#E6E6E6', linestyle='solid')
  if style == 'dark':
    ax = plt.axes(facecolor='#E6E6E6')
    plt.grid(color='w', linestyle='solid')
  ax.set_axisbelow(True)
  # show axis spines and set axis color
  for spine in ax.spines.values():
    spine.set_visible(True)
    spine.set_color('#E6E6E6')
  # hide top and right ticks
  ax.xaxis.tick_bottom()
  ax.yaxis.tick_left()
  # lighten ticks and labels
  ax.tick_params(colors='gray', direction='out')
  for tick in ax.get_xticklabels():
    tick.set_color('gray')
  for tick in ax.get_yticklabels():
    tick.set_color('gray')
  return fig, ax

def AtlasLabel(internal=False,sim=False,com_energy=13,lumi=136.0,more=''):
  out = '$\\mathbf{ATLAS}$'
  if internal:
    out+=' Internal'
  out+='\n'
  if sim:
    out+='Simulation, $\sqrt{s} = '+str(com_energy)+'$ TeV, '+str(lumi)+' $fb^{-1}$'
  if more != '':
    out+='\n'+more
  return out
