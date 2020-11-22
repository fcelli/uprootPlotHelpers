import matplotlib.pyplot as plt
from .PlotInterface import PlotInterface
from .PlotStyle import PlotStyle

class Hist1D(PlotInterface):
    """
    Class for plotting 1D histograms.
    """

    def __init__(self, inputs, **kwargs):
        """Instantiates a Hist1D object.

        Args:
            inputs ( [(FileManager, {'opt1':'val1','opt2':'val2'})] ): tuple (or list of tuples) describing input datasets and options.
        """
        self._axratio = None
        self._run()

    def _check_args(self) -> None:
        """Checks arguments type
        """
        if isinstance(self._inputs,list):
            if len(self._inputs) == 0: raise TypeError('Argument \'inputs\' is empty.')
            elif any([not isinstance(i,tuple) for i in self._inputs]): raise TypeError('Elements of argument \'inputs\' must be tuples.')
        else:
            if not isinstance(self._inputs,tuple): raise TypeError('Argument \'inputs\' must be a tuple (or list of tuples).')


    def _set_default_opts(self) -> None:
        """Sets default histogram options.
        """
        
        # Set general default options
        self._add_default_options(
            base   = self._options,
            new    = {
                # Histogram options
                'var'           : None,
                'weight'        : None,
                'nbins'         : 10,
                'xrange'        : (0,10),
                'yrange'        : (None,None),
                'xlabel'        : '',
                'ylabel'        : '',
                'mask'          : None,
                'norm'          : False,
                'logy'          : False,
                # Ratio plot
                'heightratios'  : (3,1),
                'ratio'         : 0,
                'makeratio'     : True,
                'ratiorange'    : (None,None),
                'ratiolabel'    : '',
                'rationydiv'    : 4,
                'ratiostyle'    : {}
            }
        )

        # Set input-specific default options
        for ipt in self._inputs:
            self._add_default_options(
                base   = ipt[1],
                new    = {
                    'opt'      : 'step',
                    'label'    : '',
                    'color'    : 'C'+str(self._inputs.index(ipt)),
                    'var'      : self._options['var'],
                    'weight'   : self._options['weight'],
                    'nbins'    : self._options['nbins'],
                    'mask'     : self._options['mask']
                }
            )

    def _create_figure(self) -> None:
        """Creates the canvas where the plots will be drawn.
        """

        if len(self._inputs)>1 and self._options['makeratio']:
            self._fig, (self._ax, self._axratio) = plt.subplots(
                2,
                figsize     = self._options['figsize'],
                sharex      = True,
                gridspec_kw = { 'hspace'       : 0,
                                'height_ratios': self._options['heightratios'] } ) 
        else:
            self._fig, self._ax = plt.subplots(figsize = self._options['figsize'])

    def _draw(self) -> None:
        """Draws plots on the canvas
        """
        def _create_hist(ipt, var):
            # Define data
            data = ipt[0].df[var]
            # Define weight
            weight = None
            if ipt[1]['weight'] is not None:
                weight = ipt[0].df[ipt[1]['weight']]
            # Define mask
            mask = None
            if ipt[1]['mask'] is not None:
                # A mask is applied
                mask = [True]*len(data)
                if isinstance(ipt[1]['mask'],list):
                    for m in ipt[1]['mask']:
                        mask = mask & ipt[0].df[m]
                else:
                    mask = mask & ipt[0].df[ipt[1]['mask']]
            
            # Apply mask to data and weight
            if mask is not None:
                data    = data[mask]
                weight  = weight[mask]

            # Create histogram
            n,bins,_ = self._ax.hist( 
                data,
                weights  = weight,
                bins     = ipt[1]['nbins'],
                range    = self._options['xrange'],
                color    = ipt[1]['color'],
                histtype = ipt[1]['opt'],
                label    = ipt[1]['label'],
                density  = self._options['norm']
            )
            return (n, bins)
        
        self._bin_contents  = []
        self._bin_edges     = []
        if isinstance(self._inputs,list):
            # Multiple inputs
            for ipt in self._inputs:
                n, bins = _create_hist(ipt, ipt[1]['var'])
                self._bin_contents.append(n)
                self._bin_edges.append(bins)
        else:
            # Single input
            n, bins = _create_hist(self._inputs, self._inputs[1]['var'])
            self._bin_contents.append(n)
            self._bin_edges.append(bins)

        # Log scale
        if self._options['logy']: self._ax.set_yscale('log')

        # Axes labels
        self._ax.set_xlabel(self._options['xlabel'])
        self._ax.set_ylabel(self._options['ylabel'])

        # Axes limits
        self._ax.set_xlim(self._options['xrange'])
        self._ax.set_ylim(self._options['yrange'])

        # Draw legend
        self._ax.legend()

    def _hook(self):
        """Draws ratio plots
        """
        #FIXME needed? If so, move to the top
        import warnings
        import numpy as np
        #---------
        ratiodata  = {}
        if len(self._inputs)>1 and self._options['makeratio']:
            for i in range(0,len(self._inputs)):
                if i == self._options['ratio']: continue
                with warnings.catch_warnings():
                    warnings.filterwarnings('ignore', 'divide by zero encountered in true_divide', RuntimeWarning)
                    warnings.filterwarnings('ignore', 'invalid value encountered in true_divide' , RuntimeWarning) 
                    ratiodata[i] = np.array(self._bin_contents[i])/np.array(self._bin_contents[self._options['ratio']]) 
            for idx in ratiodata:
                maskfinite = [ (not np.isnan(x)) and (x!=np.inf) for x in ratiodata[idx] ] # determine finite ratio values
                self._axratio.hist(
                    x        = self._bin_edges[idx][:-1][maskfinite],   # initialize with 1 entry per finite bin
                    bins     = self._bin_edges[idx],                    # use same binning as original histos
                    weights  = ratiodata[idx][maskfinite],              # weight the only entry per bin by the ratio values
                    color    = self._inputs[idx][1]['color'],
                    histtype = 'step'
                )
            # Set axes limits
            self._axratio.set_xlim(self._options['xrange'])
            self._axratio.set_ylim(self._options['ratiorange'])
            # Set axes labels
            self._axratio.set_xlabel(self._options['xlabel'])
            self._axratio.set_ylabel(self._options['ratiolabel'])
            # Set y axis ticks
            ylow, yhigh = self._axratio.get_ylim()
            tick_step = float(yhigh-ylow)/self._options['rationydiv']
            self._axratio.yaxis.set_ticks(np.arange(ylow, yhigh, tick_step))

    def _set_style(self):
        super()._set_style()
        # Set style of ratio plot
        self._options['ratiostyle'].setdefault('gridlinestyle'  ,'dashed')
        self._options['ratiostyle'].setdefault('ylabelfontsize' ,12)
        PlotStyle(self._axratio, self._options['ratiostyle'])
        
    @property
    def axratio(self):
        return self._axratio

    @property
    def bin_contents(self):
        return self._bin_contents
    
    @property
    def bin_edges(self):
        return self._bin_edges