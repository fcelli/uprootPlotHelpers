from abc import ABC, abstractmethod
import matplotlib.pyplot as plt
from urph.textboxtools import TextBox

class PlotInterface(ABC, object):
    """
    PlotInterface is an abstract class defining the interface for all other plot classes.
    Methods marked with the @abstractmethod decorator must be overridden in derived classes.
    """

    def __new__(cls, inputs, **kwargs):
        instance = object.__new__(cls)
        instance._inputs    = inputs
        instance._options   = {}
        instance._fig       = None
        instance._ax        = None
        instance._axratio   = None
        instance._add_default_options(
            base = instance._options,
            new  = {
                # Show and Save
                'show'      : True,
                'saveas'    : None,
                # Textbox
                'textbox'       : False,
                'experiment'    : None,
                'internal'      : False,
                'simulation'    : False,
                'ecom'          : None,
                'u_ecom'        : 'TeV',
                'lumi'          : None,
                'u_lumi'        : '$fb^{-1}$',
                'tb_addtext'    : None,
                'tb_pos'        : (0.05,0.95),
                'tb_fontsize'   : 14
                }
        )
        instance._options.update(kwargs)
        return instance
        
    def _add_default_options(self, base : dict, new : dict) -> None:
        for key in new:
            if key not in base:
                base.update({key:new[key]})

    @abstractmethod
    def _check_args(self) -> None:
        pass

    @abstractmethod
    def _set_default_opts(self) -> None:
        pass

    @abstractmethod
    def _create_figure(self) -> None:
        pass

    @abstractmethod
    def _draw(self) -> None:
        pass

    def _hook(self):
        """Overwrite this function in derived classes if additional operations are needed.
        """
        pass

    def _run(self) -> None:
        """Main algorithm.
        """
        self._check_args()
        self._set_default_opts()
        self._create_figure()
        self._draw()
        self._hook()
        if self._options['textbox']:
            self._draw_textbox()
        if self._options['saveas'] is not None:
            self._save_as(self._options['saveas'])
        if self._options['show']:
            self._show()

    def _draw_textbox(self) -> None:
        tb      = TextBox(self._options)
        textstr = tb.default()
        xpos, ypos  = self._options['tb_pos']
        self._ax.text(
            xpos,
            ypos,
            textstr,
            transform   = self._ax.transAxes,
            fontsize    = self._options['tb_fontsize'],
            verticalalignment = 'top'
        )
        
    def _save_as(self,name) -> None:
        self._fig.savefig(name)

    def _show(self) -> None:
        plt.show()