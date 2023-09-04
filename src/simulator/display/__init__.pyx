from .components import GameVisualizer


def get_impl(visualize: bool = True):
    """ Get Proper Visualizer Implementation """
    if visualize:
        if GameVisualizer.is_pyodide:
            from .web.components import JSVisualizer
            return JSVisualizer
        else:
            from .desktop.components import PyArcadeVisualizer
            return PyArcadeVisualizer
    else:
        return GameVisualizer
