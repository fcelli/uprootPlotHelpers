experiment = None
internal   = True
sim        = True
ecom       = None
lumi       = None
text       = None
pos        = (0.05,0.95)
fontsize   = 14

def Experiment(exp):
  global experiment
  experiment = exp

def Internal(is_internal):
  global internal
  internal = is_internal

def Simulation(is_sim):
  global sim
  sim = is_sim

def Ecom(e):
  global ecom
  ecom = e

def Luminosity(l):
  global lumi
  lumi = l

def Text(t):
  global text
  text = t

def Position(x,y):
  global pos
  pos = (x,y)

def FontSize(f):
  global fontsize
  fontsize = f

def MakeTextBox(): 
  textbox = ''
  if experiment is not None:
    textbox += ('$\mathbf{'+str(experiment)+'}$')
    if internal:
      textbox += ' $Internal$'
    textbox += '\n'
  if sim:
    textbox += 'Simulation '
  if ecom is not None:
    textbox += ('$\sqrt{s}='+str(ecom)+'$TeV ')
  if lumi is not None:
    textbox += (str(lumi)+'$fb^{-1}$')
  if text is not None:
    textbox += '\n{}'.format(text)
  return textbox




