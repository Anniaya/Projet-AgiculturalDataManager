from bokeh.layouts import column
from bokeh.models import ColumnDataSource, Select, DateRangeSlider, HoverTool
from bokeh.plotting import figure, curdoc
import pandas as pd

class MockDataManager:
    def __init__(self):
        self.monitoring_data = pd.DataFrame({
            'date': pd.date_range(start="2025-01-01", periods=10, freq="D"),
            'yield_value': [10, 12, 15, 13, 16, 18, 20, 19, 21, 23],
        })
        self.yield_history = pd.DataFrame({
            'date': pd.date_range(start="2020-01-01", periods=10, freq="Y"),
            'yield_value': [8, 9, 11, 10, 12, 14, 16, 15, 17, 19],
        })

    def get_parcelle_options(self):
        return ['Parcelle_1', 'Parcelle_2']

    def get_date_range(self):
        return self.monitoring_data['date'].min(), self.monitoring_data['date'].max()

class AgriculturalDashboard:
    def __init__(self, data_manager):
        self.data_manager = data_manager
        self.source = ColumnDataSource(data=dict(date=[], yield_value=[]))
        self.create_yield_history_plot()

    def create_yield_history_plot(self):
        self.plot = figure(title="Historique des Rendements", x_axis_type="datetime", height=400)
        self.plot.line(source=self.source, x="date", y="yield_value", line_width=2)
        curdoc().add_root(column(self.plot))

mock_manager = MockDataManager()
dashboard = AgriculturalDashboard(mock_manager)
