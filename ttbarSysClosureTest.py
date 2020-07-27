from helpers.filetools  import FileManager
from helpers.modeltools import h1DModel
from helpers.plottools  import Histos1D
import matplotlib.pyplot as plt
import helpers.textboxtools as tb

def ApplySelections(fm):
  cutlist = []
  cutlist.append( fm.addmask('Hcand_pt_l450'    ,'Hcand_pt<450'                 ,['Hcand_pt']) )
  cutlist.append( fm.addmask('Hcand_pt_g450l650','(Hcand_pt>450)&(Hcand_pt<650)',['Hcand_pt']) )
  cutlist.append( fm.addmask('Hcand_pt_g650'    ,'Hcand_pt>650'                 ,['Hcand_pt']) )
  fm.df['category'].astype('category')
  cutlist.append( fm.addmask('bbl'              ,'category==\'bbl\'.encode()'   ,['category']) )
  cutlist.append( fm.addmask('bbs'              ,'category==\'bbs\'.encode()'   ,['category']) )
  cutlist.append( fm.addmask('bxl'              ,'category==\'bxl\'.encode()'   ,['category']) )
  cutlist.append( fm.addmask('bxs'              ,'category==\'bxs\'.encode()'   ,['category']) )
  cutlist.append( fm.addmask('xxl'              ,'category==\'xxl\'.encode()'   ,['category']) )
  cutlist.append( fm.addmask('xxs'              ,'category==\'xxs\'.encode()'   ,['category']) )
  return cutlist

def main():

  basedir = '/afs/cern.ch/work/f/fcelli/private/ATLAS/HbbJetMiniNtuples/recoNtuples'
  tag     = '200727'
  syslist = ['PowHer','MG5Py8']
  reglist = ['srl','srs','vrl','vrs']
  columns = ['w','Hcand_m','Hcand_pt','category']
  extlist = ['.pdf','.png']

  # define textbox
  tb.Experiment('ATLAS')
  tb.Internal(True)
  tb.Simulation(True)
  tb.Ecom(13)
  tb.Luminosity(136.0)
  
  # define histogram models
  hmod_m  = h1DModel( var    = 'Hcand_m',
                      nbins  = 44,
                      xlow   = 60,
                      xhigh  = 280,
                      xlabel = 'Large-R Jet Mass [GeV]',
                      ylabel = 'Events' )

  hmod_pt = h1DModel( var    = 'Hcand_pt',
                      nbins  = 95,
                      xlow   = 250,
                      xhigh  = 1200,
                      xlabel = 'Large-R Jet $p_{T}$ [GeV]',
                      ylabel = 'Events' )

  hmodlist = [hmod_m, hmod_pt]

  for sys in syslist:
    for reg in reglist:

      tb.text = reg.upper()

      fm_PowPy8 = FileManager( filename = '{}/ttbar_allhad_PowPy8_r{}/{}/ttbar_allhad_PowPy8.root'.format(basedir,sys,tag),
                               treename = reg+'/outTree',
                               columns  = columns+['reweight'],
                               dropna   = False )
      fm_PowHer = FileManager( filename = '{}/ttbar_allhad_{}/{}/ttbar_allhad_{}.root'.format(basedir,sys,tag,sys),
                               treename = reg+'/outTree',
                               columns  = columns,
                               dropna   = False )
 
      fm_PowPy8.df['full_weight'] = fm_PowPy8.df.w * fm_PowPy8.df.reweight

      cutlist = ApplySelections(fm_PowPy8)
      ApplySelections(fm_PowHer)
      cutlist = [None]+cutlist

      for hmod in hmodlist:
        for cut in cutlist:
          if cut is not None:
            if hmod.var in cut: continue
            if len(cut)==3 and cut[-1] != reg[-1]: continue
          Histos1D( [(fm_PowPy8,{'weight':'full_weight','label':'reweighted (PowPy8)'}),
                     (fm_PowHer,{'weight':'w'          ,'label':'fullsim (PowHer)'   }) ],
                    hmod,
                    maskname   = cut,
                    ratiorange = [0.5,1.5],
                    ratio      = 0,
                    ratiolabel = 'fs/rw',
                    textbox    = True )

          for ext in extlist:
            figname =''
            if cut == None:
              figname = '{}_{}_{}{}'.format(sys,reg,hmod.var,ext)
            else:
              figname = '{}_{}_{}_{}{}'.format(sys,reg,cut,hmod.var,ext)
            print('Saving figure: '+figname)
            plt.savefig('./'+figname)

        plt.close('all')
         

if __name__ == '__main__':
  main()

