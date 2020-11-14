from abc import ABC, abstractmethod
import matplotlib.pyplot as plt

class PlotInterface(ABC):
    """
    PlotInterface defines the interface for all other plot classes.
    """

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
        """
        Overwrite this function in derived classes if additional operations are needed.
        """
        pass

    def _run(self) -> None:
        self._check_args()
        self._set_default_opts()
        self._create_figure()
        self._draw()
        self._hook()

    def _save_as(self,name) -> None:
        if name is not None:
            plt.savefig(name)

    def _show(self,flag) -> None:
        if flag:
            plt.show()