import copy

def plot1D(fmlist,hmod,mask=None,**kwargs):
  '''
  fmlist format: [(FileManager,{opt1:val1, opt2:val2})]
  '''
  newfmlist = []
  for fm in fmlist:
    extrainfo = copy.copy(kwargs)
    if type(fm) == tuple:
      extrainfo.update(fm[1])      
    newfmlist.append((fm[0],extrainfo))
  
  fmlist = newfmlist
  for fm in fmlist:
    if 'opt' not in fm[1]: fm[1]['opt']='hist'

  #if 'ratio' not in kwargs: kwargs['ratio']=None
  print(fmlist)
