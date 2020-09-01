from helpers.filetools  import FileManager
from helpers.modeltools import h1DModel
from helpers.plottools  import ContourPlot
import matplotlib.pyplot as plt

def main():
  path    = '/afs/cern.ch/work/f/fcelli/private/ATLAS/HbbJetMiniNtuples/C2Studies/200618/'
  cols    = ['w','Hcand_C2','Hcand_D2','Hcand_tau21']
  reglist = ['srl','srs']
  extlist = ['.pdf','.png']
  hmodels = []
  hmodels.append( h1DModel( var = 'Hcand_C2',
                            nbins   = 50,
                            x_range = (0,0.5),
                            xlabel  = 'Large-R Jet C2',
                            ylabel  = 'Events' ) )

  hmodels.append( h1DModel( var     = 'Hcand_D2',
                            nbins   = 50,
                            x_range = (0,4),
                            xlabel  = 'Large-R Jet D2',
                            ylabel  = 'Events' ) )

  hmodels.append( h1DModel( var     = 'Hcand_tau21',
                            nbins   = 50,
                            x_range = (0,1),
                            xlabel  = 'Large-R Jet $\\tau_{21}$',
                            ylabel  = 'Events' ) )

  for reg in reglist:
    fm_higgs = FileManager( filename = path+'Higgs/Higgs.root',
                            treename = reg+'/outTree',
                            columns  = cols,
                            dropna   = True )
    fm_ttbar = FileManager( filename = path+'Powheg_ttbar/Powheg_ttbar.root',
                            treename = reg+'/outTree',
                            columns  = cols,
                            dropna   = True )
    fm_QCD   = FileManager( filename = path+'Pythia8_dijet/Pythia8_dijet.root',
                            treename = reg+'/outTree',
                            columns  = cols,
                            dropna   = True ) 
    fm_Vqq   = FileManager( filename = path+'Sherpa_Vqq/Sherpa_Vqq.root',
                            treename = reg+'/outTree',
                            columns  = cols,
                            dropna   = True ) 
 
    for xhmod in hmodels:
      idx = hmodels.index(xhmod)
      if idx == len(hmodels)-1: continue
      for yhmod in hmodels[idx+1:]:

        ContourPlot( [ (fm_higgs,{'label':'Higgs','weight':'w','color':'C0'}),
                       (fm_ttbar,{'label':'ttbar','weight':'w','color':'C1'}) ],
                     xhmod     = xhmod,
                     yhmod     = yhmod,
                     nlevels   = 8 )

        for ext in extlist: 
          figname = '{}_Higgs_ttbar_{}_{}{}'.format(reg,xhmod.var,yhmod.var,ext)
          print('Saving figure: '+figname)
          plt.savefig('./'+figname)

        plt.close('all')

        ContourPlot( [ (fm_higgs,{'label':'Higgs','weight':'w','color':'C0'}),
                       (fm_QCD  ,{'label':'QCD'  ,'weight':'w','color':'C2'}) ],
                     xhmod     = xhmod,
                     yhmod     = yhmod, 
                     nlevels   = 8 )

        for ext in extlist:
          figname = '{}_Higgs_QCD_{}_{}{}'.format(reg,xhmod.var,yhmod.var,ext)
          print('Saving figure: '+figname)
          plt.savefig('./'+figname)

        plt.close('all')  

        ContourPlot( [ (fm_higgs,{'label':'Higgs','weight':'w','color':'C0'}),
                       (fm_Vqq  ,{'label':'Vqq'  ,'weight':'w','color':'C3'}) ],
                     xhmod     = xhmod,
                     yhmod     = yhmod, 
                     nlevels   = 8 )

        for ext in extlist:
          figname = '{}_Higgs_Vqq_{}_{}{}'.format(reg,xhmod.var,yhmod.var,ext)
          print('Saving figure: '+figname)
          plt.savefig('./'+figname)

        plt.close('all')

if __name__ == "__main__":
  main()
