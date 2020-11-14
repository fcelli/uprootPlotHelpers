import uproot, sys

__all__ = ['FileManager']

class FileManager:
  def __init__(self,filename=None,treename=None,columns=None,dropna=False):
    self.filename = filename
    self.treename = treename
    if self.filename is not None:
      self.open(self.filename)
    if self.treename is not None:
      self.settree(treename)
      self.makedf(columns)
      if dropna:
        if self.df[self.df.columns].isna().any().any():
          print('Warning: dropping missing values (NaN) from the dataframe.')
        self.df=self.df[self.df.columns].dropna(axis=0)

  def open(self,filename):
    self.file = uproot.open(filename)
    if self.file==None:
      print('Error: no file found at {}'.format(filename))
      sys.exit()

  def settree(self,treename):
    self.tree = self.file[treename]
    if self.tree==None:
      print('Error: no tree found with name {}'.format(treename))
      sys.exit()

  def makedf(self,columns=None):
    if columns is None:
      self.df = self.tree.pandas.df()
    else:
      self.df = self.tree.pandas.df(columns)
    
  def addmask(self,maskname,exp,varlist):
    '''
    maskname [type = str]      : name of the new column
    exp      [type = str]      : expression to evaluate for generating the new column
    varlist  [type = str list] : list of variable names in exp
    '''
    vdict = {}
    for var in varlist:
       vdict[var] = self.df[var]
    self.df[maskname] = eval(exp,vdict)
    return maskname
