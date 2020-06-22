import sys

class h1DModel:
  def __init__( self,
                var,
                nbins,
                xlow,
                xhigh,
                weight = None,
                xlabel = '',
                ylabel = '' ):
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
