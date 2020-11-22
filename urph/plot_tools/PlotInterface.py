from abc import ABC, abstractmethod
import matplotlib.pyplot as plt
from .TextBox import TextBox
from .PlotStyle import PlotStyle

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
        instance._add_default_options(
            base = instance._options,
            new  = {
                # Show and Save
                'figsize'   : (8,6),
                'show'      : True,
                'saveas'    : None,
                'textbox'   : {},
                'style'     : {}
                }
        )
        instance._options.update(kwargs)
        return instance
    
    def _add_default_options(self, base : dict, new : dict) -> None:
        for key in new:
            if key not in base:
                base.update({key:new[key]})

    def _run(self) -> None:
        """Main algorithm.
        """
        self._check_args()
        self._set_default_opts()
        self._create_figure()
        self._set_style()
        self._draw()
        self._hook()
        self._draw_textbox()
        self._save_as(self._options['saveas'])
        self._show()

    @abstractmethod
    def _check_args(self) -> None:
        pass

    @abstractmethod
    def _set_default_opts(self) -> None:
        pass

    @abstractmethod
    def _create_figure(self) -> None:
        pass

    def _set_style(self) -> None:
        """Set default plot style
        """
        PlotStyle(self._ax, self._options['style'])

    @abstractmethod
    def _draw(self) -> None:
        pass

    def _hook(self):
        """Overwrite this function in derived classes if additional operations are needed.
        """
        pass

    def _draw_textbox(self) -> None:
        TextBox(self._ax, self._options['textbox'])
        
    def _save_as(self,name) -> None:
        if self._options['saveas'] is not None:
            self._fig.savefig(name)

    def _show(self) -> None:
        if self._options['show']:
            plt.show()
            
    @property
    def fig(self):
        return self._fig

    @property
    def ax(self):
        return self._ax