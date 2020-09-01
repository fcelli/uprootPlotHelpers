from helpers.filetools  import FileManager
from helpers.modeltools import h1DModel
from helpers.plottools  import Histos1D
import matplotlib.pyplot as plt

def ApplyCuts(fm):
  cutlist = []
  cutlist.append( fm.addmask('m_l100'     ,'Hcand_m<100'                  ,['Hcand_m'])  )
  cutlist.append( fm.addmask('m_g100l150' ,'(Hcand_m>100)&(Hcand_m<150)'  ,['Hcand_m'])  )
  cutlist.append( fm.addmask('m_g150'     ,'Hcand_m>150'                  ,['Hcand_m'])  )
  cutlist.append( fm.addmask('pt_l450'    ,'Hcand_pt<450'                 ,['Hcand_pt']) )
  cutlist.append( fm.addmask('pt_g450l650','(Hcand_pt>450)&(Hcand_pt<650)',['Hcand_pt']) )
  cutlist.append( fm.addmask('pt_g650'    ,'Hcand_pt>650'                 ,['Hcand_pt']) )
  return cutlist

def main():
  path    = '/afs/cern.ch/work/f/fcelli/private/ATLAS/HbbJetMiniNtuples/C2Studies/200618/'
  cols    = ['w','Hcand_m','Hcand_pt','Hcand_C2','Hcand_D2','Hcand_tau21','Hcand_tau32']
  reglist = ['srl','srs'] 
  extlist = ['.pdf','.png']
  hmodels = []
  hmodels.append( h1DModel( var = 'Hcand_C2',
                            nbins   = 50,
                            x_range = (0,0.5),
                            xlabel  = 'Large-R Jet C2',
                            ylabel  = 'Events (Normalised)' ) )

  hmodels.append( h1DModel( var     = 'Hcand_D2',
                            nbins   = 50,
                            x_range = (0,4),
                            xlabel  = 'Large-R Jet D2',
                            ylabel  = 'Events (Normalised)' ) )

  hmodels.append( h1DModel( var     = 'Hcand_tau21',
                            nbins   = 50,
                            x_range = (0,1),
                            xlabel  = 'Large-R Jet $\\tau_{21}$',
                            ylabel  = 'Events (Normalised)' ) )

  hmodels.append( h1DModel( var     = 'Hcand_tau32',
                            nbins   = 50,
                            x_range = (0,1),
                            xlabel  = 'Large-R Jet $\\tau_{32}$',
                            ylabel  = 'Events (Normalised)' ) )

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

    cutlist = ApplyCuts(fm_higgs)
    ApplyCuts(fm_ttbar)
    ApplyCuts(fm_QCD)
    ApplyCuts(fm_Vqq)
    cutlist = [None] + cutlist
 
    for cut in cutlist:
      for hmod in hmodels:

        Histos1D( [ (fm_higgs,{'label':'Higgs','weight':'w'}),
                    (fm_ttbar,{'label':'ttbar','weight':'w'}),
                    (fm_QCD  ,{'label':'QCD'  ,'weight':'w'}),
                    (fm_Vqq  ,{'label':'Vqq'  ,'weight':'w'}) ],
                  model     = hmod,
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
