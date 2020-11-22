class PlotStyle:
    def __init__(self, ax, options : dict):
        self.ax = ax
        # Face
        self.facecolor          = options.setdefault('facecolor'        , 'w')
        # Grid
        self.gridcolor          = options.setdefault('gridcolor'        , '#E6E6E6')
        self.gridlinestyle      = options.setdefault('gridlinestyle'    , 'solid')
        self.hidegrid           = options.setdefault('hidegrid'         , False)
        # Axes
        self.axiscolor          = options.setdefault('axiscolor'        , 'grey')
        self.hidespines         = options.setdefault('hidespines'       , [])
        self.xlabelfontsize     = options.setdefault('xlabelfontsize'   , 14)
        self.ylabelfontsize     = options.setdefault('ylabelfontsize'   , 14)
        # Ticks
        self.tickcolor          = options.setdefault('tickcolor'        , 'black')
        self.ticklabelcolor     = options.setdefault('ticklabelcolor'   , 'black')
        self.tickdirection      = options.setdefault('tickdirection'    , 'out')
        self.xticksposition     = options.setdefault('xticksposition'   , 'bottom')
        self.yticksposition     = options.setdefault('yticksposition'   , 'left')
        
        # Run algorithm
        if self.ax is not None:
            self.__run()
        
    def __run(self) -> None:
        self.__set_face()
        self.__set_grid()
        self.__set_axes()
        self.__set_ticks()
        
    def __set_face(self) -> None:
        self.ax.set_facecolor(self.facecolor)
        
    def __set_grid(self) -> None:
        if not self.hidegrid:
            self.ax.grid(
                color       = self.gridcolor,
                linestyle   = self.gridlinestyle
            )
    
    def __set_axes(self) -> None:
        for key in ['left', 'right', 'top', 'bottom']:
            if key in self.hidespines:
                self.ax.spines[key].set_visible(False)
            else:
                self.ax.spines[key].set_visible(True)
                self.ax.spines[key].set_color(self.axiscolor)
            self.ax.xaxis.label.set_size(self.xlabelfontsize)
            self.ax.yaxis.label.set_size(self.ylabelfontsize)
    
    def __set_ticks(self) -> None:
        if self.xticksposition == 'bottom':
            self.ax.xaxis.tick_bottom()
        elif self.xticksposition == 'top':
            self.ax.xaxis.tick_top()
        if self.yticksposition == 'left':
            self.ax.yaxis.tick_left()
        elif self.yticksposition == 'right':
            self.ax.yaxis.tick_right()
            
        self.ax.tick_params(
            colors      = self.tickcolor,
            direction   = self.tickdirection
        )
        
        for tick in self.ax.get_xticklabels():
            tick.set_color(self.ticklabelcolor)
        for tick in self.ax.get_yticklabels():
            tick.set_color(self.ticklabelcolor)