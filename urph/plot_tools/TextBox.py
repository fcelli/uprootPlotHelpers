class TextBox:
    def __init__(self, ax, options):
        self.ax = ax
        # Set default options
        self.draw       = options.setdefault('draw'         , False)
        self.position   = options.setdefault('position'     , (0.05,0.95))
        self.fontsize   = options.setdefault('fontsize'     , 14)
        self.experiment = options.setdefault('experiment'   , None)
        self.internal   = options.setdefault('internal'     , False)
        self.simulation = options.setdefault('simulation'   , False)
        self.ecom       = options.setdefault('ecom'         , None)
        self.u_ecom     = options.setdefault('u_ecom'       , 'TeV')
        self.lumi       = options.setdefault('lumi'         , None)
        self.u_lumi     = options.setdefault('u_lumi'       , '$fb^{-1}$')
        self.text       = options.setdefault('text'         , None)
        # Main algorithm
        if self.draw:
            self.__run()

    def __run(self) -> None:
        # Create textbox string
        textstr = ''
        if self.experiment is not None:
        	textstr += (r'$\mathbf{' + self.experiment + '}$')
        	if self.internal:
        		textstr += ' $Internal$'
        textstr += '\n'
        if self.simulation:
            textstr += 'Simulation '
        if self.ecom is not None:
            textstr += (r'$\sqrt{s}='+str(self.ecom)+'$'+self.u_ecom+' ')
        if self.lumi is not None:
            textstr += (str(self.lumi)+self.u_lumi)
        if self.text is not None:
        	textstr += '\n{}'.format(self.text)
        # Draw textbox on plot
        xpos, ypos  = self.position
        self.ax.text(
            xpos,
            ypos,
            textstr,
            transform   = self.ax.transAxes,
            fontsize    = self.fontsize,
            verticalalignment = 'top'
        )




