from helpers.filetools  import FileManager
from helpers.modeltools import h1DModel
from helpers.plottools  import Histos1D
import matplotlib.pyplot as plt

def ApplyCuts(fm):
  fm.addmask('m_l100'     ,'Hcand_m<100'                  ,['Hcand_m'])
  fm.addmask('m_g100l150' ,'(Hcand_m>100)&(Hcand_m<150)'  ,['Hcand_m'])
  fm.addmask('m_g150'     ,'Hcand_m>150'                  ,['Hcand_m'])
  fm.addmask('pt_l450'    ,'Hcand_pt<450'                 ,['Hcand_pt'])
  fm.addmask('pt_g450l650','(Hcand_pt>450)&(Hcand_pt<650)',['Hcand_pt'])
  fm.addmask('pt_g650'    ,'Hcand_pt>650'                 ,['Hcand_pt'])

def main():
  path    = '/afs/cern.ch/work/f/fcelli/private/ATLAS/HbbJetMiniNtuples/C2Studies/200618/'
  cols    = ['w','Hcand_m','Hcand_pt','Hcand_C2','Hcand_D2','Hcand_tau21','Hcand_tau32']
  reglist = ['srl','srs']
  cutlist = [None,'m_l100','m_g100l150','m_g150','pt_l450','pt_g450l650','pt_g650']
  extlist = ['.pdf','.png']
  hmodels = []
  hmodels.append( h1DModel( var = 'Hcand_C2',
                            nbins  = 50,
                            xlow   = 0,
                            xhigh  = 0.5,
                            weight = 'w',
                            xlabel = 'Large-R Jet C2',
                            ylabel = 'Events (Normalised)' ) )

  hmodels.append( h1DModel( var    = 'Hcand_D2',
                            nbins  = 50,
                            xlow   = 0,
                            xhigh  = 4,
                            weight = 'w',
                            xlabel = 'Large-R Jet D2',
                            ylabel = 'Events (Normalised)' ) )

  hmodels.append( h1DModel( var    = 'Hcand_tau21',
                            nbins  = 50,
                            xlow   = 0,
                            xhigh  = 1,
                            weight = 'w',
                            xlabel = 'Large-R Jet $\\tau_{21}$',
                            ylabel = 'Events (Normalised)' ) )

  hmodels.append( h1DModel( var    = 'Hcand_tau32',
                            nbins  = 50,
                            xlow   = 0,
                            xhigh  = 1,
                            weight = 'w',
                            xlabel = 'Large-R Jet $\\tau_{32}$',
                            ylabel = 'Events (Normalised)' ) )

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

    ApplyCuts(fm_higgs)
    ApplyCuts(fm_ttbar)
    ApplyCuts(fm_QCD)
    ApplyCuts(fm_Vqq)
 
    for cut in cutlist:
      for hmod in hmodels:

        Histos1D( [ (fm_higgs,{'label':'Higgs'}),
                    (fm_ttbar,{'label':'ttbar'}),
                    (fm_QCD  ,{'label':'QCD'  }),
                    (fm_Vqq  ,{'label':'Vqq'  }) ],
                  hmod      = hmod,
                  norm      = True,
                  maskname  = cut,
                  makeratio = False )

        for ext in extlist:
          figname =''
          if cut == None:
            figname = '{}_{}{}'.format(reg,hmod.var,ext)
          else:
            figname = '{}_{}_{}{}'.format(reg,cut,hmod.var,ext)
          print('Saving figure: '+figname)
          plt.savefig('./'+figname)

        plt.close('all')

if __name__ == "__main__":
  main()
