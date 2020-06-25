import sys

figsize        = (8,6)
theme          = 'white'
facecolor      = 'w'
gridcolor      = '#E6E6E6'
gridlinestyle  = 'solid'
axiscolor      = 'grey'
tickcolor      = 'black'
ticklabelcolor = 'black'
 
def SetFigSize(x,y):
  global figsize
  figsize = (x,y)

def SetTheme(t):
  if t not in ['white','dark']:
    print('Error: theme not available.')
    sys.exit()
  global theme
  theme = t
  if theme == 'white':
    SetFaceColor('w')
    SetGridColor('#E6E6E6')

  elif theme == 'dark':
    SetFaceColor('#E6E6E6')
    SetGridColor('w')

def SetFaceColor(fc):
  global facecolor
  facecolor = fc

def SetGridColor(gc):
  global gridcolor
  gridcolor = gc

def SetGridLineStyle(gls):
  global gridlinestyle
  gridlinestyle = gls

def SetAxisColor(ac):
  global axiscolor
  axiscolor = ac

def SetTickColor(tc):
  global tickcolor
  tickcolor = tc

def SetTickLabelColor(tlc):
  global ticklabelcolor
  ticklabelcolor = tlc

def StyleHistos1D(ax,axratio=None):
  global theme,facecolor,linestyle,gridcolor,gridlinestyle,axiscolor,tickcolor,ticklabelcolor
  # set plot style
  ax.set_facecolor(facecolor)
  ax.grid(color=gridcolor, linestyle=gridlinestyle)
  ax.set_axisbelow(True)
  for spine in ax.spines.values():
    spine.set_visible(True)
    spine.set_color(axiscolor)
  ax.xaxis.tick_bottom()
  ax.yaxis.tick_left()
  ax.tick_params(colors=tickcolor,direction='out')
  for tick in ax.get_xticklabels():
    tick.set_color(ticklabelcolor)
  for tick in ax.get_yticklabels():
    tick.set_color(ticklabelcolor)
  # set ratio plot style
  if axratio is not None:
    axratio.set_facecolor(facecolor)
    axratio.yaxis.grid(color=gridcolor,linestyle='dashed')
    axratio.set_axisbelow(True)
    for spine in axratio.spines.values():
      spine.set_visible(True)
      spine.set_color(axiscolor)
    axratio.xaxis.tick_bottom()
    axratio.yaxis.tick_left()
    axratio.tick_params(colors=tickcolor,direction='out')
    for tick in axratio.get_xticklabels():
      tick.set_color(ticklabelcolor)
    for tick in axratio.get_yticklabels():
      tick.set_color(ticklabelcolor)

def StyleContourPlot(ax):
  global theme,facecolor,linestyle,gridcolor,gridlinestyle,axiscolor,tickcolor,ticklabelcolor
  ax.set_facecolor(facecolor)
  #ax.grid(color=gridcolor, linestyle=gridlinestyle)
  ax.set_axisbelow(True)
  for spine in ax.spines.values():
    spine.set_visible(True)
    spine.set_color(axiscolor)
  ax.xaxis.tick_bottom()
  ax.yaxis.tick_left()
  ax.tick_params(colors=tickcolor,direction='out')
  for tick in ax.get_xticklabels():
    tick.set_color(ticklabelcolor)
  for tick in ax.get_yticklabels():
    tick.set_color(ticklabelcolor)
