from PySide6.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from collections import defaultdict
from datetime import datetime
import matplotlib.dates as mdates

class ChartWidget(QWidget):
    """
    A QWidget that displays two types of charts: a pie chart showing spending by category 
    and a line chart showing daily spending trends.

    Attributes:
        layout (QVBoxLayout): The layout that holds the chart canvas.
        figure (matplotlib.figure.Figure): The matplotlib figure containing the subplots.
        ax_pie (matplotlib.axes.Axes): The axes for the pie chart.
        ax_line (matplotlib.axes.Axes): The axes for the line chart.
        canvas (FigureCanvas): The canvas that renders the figure.
    """

    def __init__(self, parent = None):
        """
        Initializes the widget, creating the layout and the charts.

        Args:
            parent (QWidget, optional): The parent widget. Defaults to None.
        """
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.figure, (self.ax_pie, self.ax_line) = plt.subplots(1, 2, figsize=(8, 4))
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)

    def update_chart(self, expenses):
        """
        Updates both the pie chart and the line chart based on the provided list of expense objects.

        Args:
            expenses (list): A list of expense objects. Each expense should have a 'category', 
                             'amount', and 'date' (either a datetime object or a date object).
        """
        self.ax_pie.clear()
        self.ax_line.clear()
    
        if not expenses:
            self.canvas.draw()
            return
        
        # Pie chart: sum by category
        category_totals = defaultdict(float)
        for e in expenses:
            category_totals[e.category] += e.amount
        labels = list(category_totals.keys())
        sizes = list(category_totals.values())
        self.ax_pie.pie(sizes, labels=labels, autopct="%1.1f%%")
        self.ax_pie.set_title("Spending by Category")

        # Line chart: daily spending trend
        daily_totals = defaultdict(float)
        for e in expenses:
            day = e.date.date() if isinstance(e.date, datetime) else e.date
            daily_totals[day] += e.amount
        days = sorted(daily_totals.keys())
        values = [daily_totals[d] for d in days]
        self.ax_line.plot(days, values, marker="o")
        self.ax_line.set_title("Spending Trend")
        self.ax_line.set_xlabel("Date")
        self.ax_line.set_ylabel("Amount")

        # Format the x-axis to display dates as mm-dd
        self.ax_line.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
        plt.xticks(rotation=45)

        self.figure.tight_layout()
        self.canvas.draw()
