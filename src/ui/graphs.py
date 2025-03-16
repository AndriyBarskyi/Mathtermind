import pyqtgraph as pg
import numpy as np

class MyGraph:
    def __init__(self, plot_widget):
        self.plot = plot_widget  

    def plot_bar_chart(self, data, labels):
        colors = [(221, 226, 246)] * len(data)
        x_positions = np.arange(len(data))
        for x, height, color in zip(x_positions, data, colors):
            bar = pg.BarGraphItem(
                x=[x], height=[height], width=0.8, brush=pg.mkBrush(color)
            )
            self.plot.addItem(bar)
        self.plot.setBackground("w") 
        self.plot.showGrid(x=True, y=True, alpha=0.3)
        self.plot.setXRange(-0.5, len(data) - 0.5)
        self.plot.setYRange(0, max(data) + 5)
        self.plot.getAxis("bottom").setTicks([list(zip(x_positions, labels))])