# This file contain Matplot library for Object Oriented Interface

from matplotlib.backends.backend_agg import FigureCanvas
from matplotlib.figure import Figure


class Chart():
    def __init__(self, data = None):
        if data is None:
            return

        fig = Figure()
        FigureCanvas(fig)

        labels = []
        sizes = []
        for row in data:
            labels.append(row[0])
            sizes.append(row[1])

        # labels = ['Cats','Dogs']
        # sizes = [4,3]

        ax = fig.add_subplot(111)
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        fig.savefig('static/chart')
    #
    # def get_canvas(self):
    #     """
    #     Get canvas
    #     """
    #     return FigureCanvas(self.fig)