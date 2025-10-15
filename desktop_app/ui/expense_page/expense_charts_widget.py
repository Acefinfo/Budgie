from PySide6.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from collections import defaultdict
from datetime import datetime


# Widget showing Pie chart (category) + Line chart (trend)
class ChartWidget(QWidget):

    def __init__(self, parent = None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)

        # Create figure with 2 subplots
        self.figure, (self.ax_pie, self.ax_line) = plt.subplots(1, 2, figsize=(8, 4))
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)


    # Update charts with a list of expense object 
    def update_charts(self,expenses):
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

        self.figure.tight_layout()
        self.canvas.draw()



    
