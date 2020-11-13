__all__ = ['h1DModel']

class h1DModel:
  def __init__( self,
                var,
                nbins,
                x_range,
                xlabel = '',
                ylabel = '' ):
    if not isinstance(var,str):       raise TypeError('Argument var must be a string.')
    if not isinstance(nbins,int):     raise TypeError('Argument nbins must be an integer.')
    if not isinstance(x_range,tuple): raise TypeError('Argument x_range must be a tuple.')
    if not isinstance(xlabel,str):    raise TypeError('Argument xlabel must be a string.')
    if not isinstance(ylabel,str):    raise TypeError('Argument ylabel must be a string.')
    if nbins<=0:                 raise ValueError('Argument nbins must be positive.')
    if len(x_range)!=2:          raise ValueError('Argument x_range must have size 2.')
    if x_range[0] >= x_range[1]: raise ValueError('Argument x_range must be in ascending order.')
    self.var     = var
    self.nbins   = nbins
    self.x_range = x_range
    self.step    = float(x_range[1]-x_range[0])/nbins
    self.xlabel  = xlabel
    self.ylabel  = ylabel
