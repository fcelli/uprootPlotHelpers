import matplotlib.pyplot as plt
from .PlotInterface import PlotInterface

class Hist1D(PlotInterface):
    """
    Class for plotting 1D histograms.
    """

    def __init__(self, inputs, **kwargs):
        """
        Arguments:
            - inputs: tuple (or list of tuples) of type (FileManager, {'opt1':'val1','opt2':'val2'})
        """

        self._inputs = inputs
        self._kwargs = kwargs

        self._fig = None
        self._ax = None
        self._axratio = None

        self._run()
        self._save_as(self._kwargs['saveas'])
        self._show(self._kwargs['show'])

    def _check_args(self) -> None:
        """
        Check arguments type
        """
        if isinstance(self._inputs,list):
            if len(self._inputs) == 0: raise TypeError('Argument \'inputs\' is empty.')
            elif any([not isinstance(i,tuple) for i in self._inputs]): raise TypeError('Elements of argument \'inputs\' must be tuples.')
        else:
            if not isinstance(self._inputs,tuple): raise TypeError('Argument \'inputs\' must be a tuple (or list of tuples).')


    def _set_default_opts(self) -> None:
        """
        Function for setting default histogram options.
        """
        def add_default_opt(opt_dict : dict, name : str, value):
            if name not in opt_dict: opt_dict.update({name:value})

        # Set general default options
        add_default_opt(self._kwargs, 'var'         , None)
        add_default_opt(self._kwargs, 'weight'      , None)
        add_default_opt(self._kwargs, 'nbins'       , 10)
        add_default_opt(self._kwargs, 'xrange'      , (0,10))
        add_default_opt(self._kwargs, 'yrange'      , (None,None))
        add_default_opt(self._kwargs, 'xlabel'      , '')
        add_default_opt(self._kwargs, 'ylabel'      , '')
        add_default_opt(self._kwargs, 'mask'        , None)
        add_default_opt(self._kwargs, 'norm'        , False)
        add_default_opt(self._kwargs, 'logy'        , False)
        add_default_opt(self._kwargs, 'ratio'       , 0)
        add_default_opt(self._kwargs, 'makeratio'   , True)
        add_default_opt(self._kwargs, 'ratiorange'  , (None,None))
        add_default_opt(self._kwargs, 'ratiolabel'  , '')
        add_default_opt(self._kwargs, 'rationydiv'  , 4)
        add_default_opt(self._kwargs, 'heightratios', [3,1])
        add_default_opt(self._kwargs, 'textbox'     , False)
        add_default_opt(self._kwargs, 'saveas'      , None)
        add_default_opt(self._kwargs, 'show'        , True)

        # Set input-specific default options
        for ipt in self._inputs:
            add_default_opt(ipt[1], 'opt'   , 'step')
            add_default_opt(ipt[1], 'label' , '')
            add_default_opt(ipt[1], 'color' , 'C'+str(self._inputs.index(ipt)))
            add_default_opt(ipt[1], 'var'   , self._kwargs['var'])
            add_default_opt(ipt[1], 'weight', self._kwargs['weight'])
            add_default_opt(ipt[1], 'nbins' , self._kwargs['nbins'])
            add_default_opt(ipt[1], 'mask'  , self._kwargs['mask'])

    def _create_figure(self) -> None:
        """
        Creates the canvas where the plots will be drawn.
        """
        #import styletools #FIXME !!!
        from urph import styletools
        #TODO make a function to handle style and textbox options

        if len(self._inputs)>1 and self._kwargs['makeratio']: #FIXME or if we are plotting more than one variable from the same sample!
            self._fig, (self._ax, self._axratio) = plt.subplots(
                2,
                figsize     = styletools.figsize,
                sharex      = True,
                gridspec_kw = { 'hspace'       : 0,
                                'height_ratios': self._kwargs['heightratios'] } ) 
        else:
            self._fig, self._ax = plt.subplots(figsize=styletools.figsize)

        #TODO this has to go in a separate function
        styletools.StyleHistos1D(self._ax,self._axratio)

    def _draw(self) -> None:
        """
        Draws plots on the canvas
        """
        def _create_hist(ipt, var): #-> tuple(list, list):
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
                range    = self._kwargs['xrange'],
                color    = ipt[1]['color'],
                histtype = ipt[1]['opt'],
                label    = ipt[1]['label'],
                density  = self._kwargs['norm']
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
        if self._kwargs['logy']: self._ax.set_yscale('log')

        # Axes labels
        plt.xlabel(self._kwargs['xlabel'],fontsize=14)
        self._ax.set_ylabel(self._kwargs['ylabel'],fontsize=14)

        # Axes limits
        self._ax.set_xlim(self._kwargs['xrange'])
        self._ax.set_ylim(self._kwargs['yrange'])

        # Draw legend
        self._ax.legend()

    def _hook(self):
        """
        Draws ratio plots
        """
        #FIXME needed? If so, move to the top
        import warnings
        import numpy as np
        #---------
        ratiodata  = {}
        if len(self._inputs)>1 and self._kwargs['makeratio']:
            for i in range(0,len(self._inputs)):
                if i == self._kwargs['ratio']: continue
                with warnings.catch_warnings():
                    warnings.filterwarnings('ignore', 'divide by zero encountered in true_divide', RuntimeWarning)
                    warnings.filterwarnings('ignore', 'invalid value encountered in true_divide' , RuntimeWarning) 
                    ratiodata[i] = np.array(self._bin_contents[i])/np.array(self._bin_contents[self._kwargs['ratio']]) 
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
            self._axratio.set_xlim(self._kwargs['xrange'])
            self._axratio.set_ylim(self._kwargs['ratiorange'])
            # Set y axis ticks
            ylow, yhigh = self._axratio.get_ylim()
            tick_step = float(yhigh-ylow)/self._kwargs['rationydiv']
            self._axratio.yaxis.set_ticks(np.arange(ylow, yhigh, tick_step))
            # Set y axis label
            self._axratio.set_ylabel(self._kwargs['ratiolabel'],fontsize=12)

    @property
    def fig(self):
        return self._fig

    @property
    def ax(self):
        return self._ax

    @property
    def axratio(self):
        return self._axratio

    @property
    def bin_contents(self):
        return self._bin_contents
    
    @property
    def bin_edges(self):
        return self._bin_edges