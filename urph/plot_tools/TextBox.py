class TextBox:
    def __init__(self, options):
    	self.experiment = options['experiment']
    	self.internal   = options['internal']
    	self.simulation = options['simulation']
    	self.ecom       = options['ecom']
    	self.u_ecom     = options['u_ecom']
    	self.lumi       = options['lumi']
    	self.u_lumi     = options['u_lumi']
    	self.text       = options['tb_addtext']
    
    def default(self) -> str:
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
        return textstr




