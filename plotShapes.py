import uproot
import uproothelpers as uh
import matplotlib.pyplot as plt
import numpy as np

fileBaseDir = '/afs/cern.ch/work/f/fcelli/private/ATLAS/HbbJetMiniNtuples/C2Studies/200618/'
regList = ['srl','srs']
varList = ['Hcand_C2','Hcand_D2','Hcand_tau32','Hcand_tau21']

h1DModels = []
# C2 model
h1DModels.append( uh.h1DModel( var    = 'Hcand_C2',
                               nbins  = 50,
                               xlow   = 0,
                               xhigh  = 0.5,
                               weight = 'w',
                               xlabel = 'Large-R Jet C2',
                               ylabel = 'Events'
                             ) )
# D2 model
h1DModels.append( uh.h1DModel( var    = 'Hcand_D2',
                               nbins  = 50,
                               xlow   = 0,
                               xhigh  = 4,
                               weight = 'w',
                               xlabel = 'Large-R Jet D2',
                               ylabel = 'Events'
                             ) )
# tau21 model
h1DModels.append( uh.h1DModel( var    = 'Hcand_tau21',
                               nbins  = 50,
                               xlow   = 0,
                               xhigh  = 1,
                               weight = 'w',
                               xlabel = 'Large-R Jet $\\tau_{21}$',
                               ylabel = 'Events'
                             ) )
# tau32 model
h1DModels.append( uh.h1DModel( var    = 'Hcand_tau32',
                               nbins  = 50,
                               xlow   = 0,
                               xhigh  = 1,
                               weight = 'w',
                               xlabel = 'Large-R Jet $\\tau_{32}$',
                               ylabel = 'Events'
                             ) )

for hmodel in h1DModels:
  for reg in regList:
    fileServiceList = []
    fileServiceList.append( uh.fileService( filepathname = fileBaseDir+'Higgs/Higgs.root',
                                            treename     = reg+'/outTree',
                                            label       = 'Higgs'
                                          ) )
    fileServiceList.append( uh.fileService( filepathname = fileBaseDir+'Powheg_ttbar/Powheg_ttbar.root',
                                            treename     = reg+'/outTree',
                                            label       = 'ttbar'
                                          ) )
    fileServiceList.append( uh.fileService( filepathname = fileBaseDir+'Pythia8_dijet/Pythia8_dijet.root',
                                            treename     = reg+'/outTree',
                                            label        = 'QCD'
                                          ) )
    fileServiceList.append( uh.fileService( filepathname = fileBaseDir+'Sherpa_Vqq/Sherpa_Vqq.root',
                                            treename     = reg+'/outTree',
                                            label        = 'Vqq'
                                          ) )

    text = uh.AtlasLabel( internal   = True,
                          sim        = True,
                          com_energy = 13,
                          lumi       = 136.0,
                          more       = reg.upper()
                        ) 

    fig,ax = uh.SimplePlot( fileServiceList,
                            hmodel,
                            figsize  = (8,6),
                            style    = 'white', 
                            text     = text,
                            histtype = 'step',
                            norm     = True
                          )

    extList = ['.png','.pdf']
    for ext in extList:
      figName = '{}_{}{}'.format(reg,hmodel.var,ext)
      print('Writing '+figName)
      plt.savefig('./'+figName)
