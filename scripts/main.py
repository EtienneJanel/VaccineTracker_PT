import json
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly


class OwidData():
    R0 = 2.5
    p_raw = 1 - (1/R0)
    IMUNE = 0.044
    VACCINE_EFFICIENCY = 0.95
    p = (1 - 1/R0 - IMUNE) / VACCINE_EFFICIENCY

    def __init__(self):
        owid_data = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv"
        self.df = pd.read_csv(owid_data)
        self.df.date = pd.to_datetime(self.df.date)
        self.columns_ = ['date','location','iso_code','total_vaccinations','population']

        self.df_pt = self.group_country()


    def group_country(self, country="Portugal"):
        self.country = country
        df_pt = self.df[self.columns_].copy()
        df_pt = df_pt[df_pt.location == self.country]
        df_pt = df_pt[df_pt.date > '2021-01-01'] # first date
        df_pt['total_vaccinations_ma'] = df_pt.total_vaccinations.rolling(7).mean()
        df_pt['daily_diff'] = df_pt.total_vaccinations.diff()
        df_pt['daily_diff_ma'] = df_pt.daily_diff.rolling(7).mean()
        time_span = df_pt.date.apply(lambda x: (x - df_pt.date.min()).days) #days
        df_pt['due_date'] = (df_pt.population * self.p) * time_span / (df_pt.total_vaccinations / 2)
        return df_pt

    def daily_doses(self):
        fig = make_subplots(1,1,specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Line(x=self.df_pt["date"], y=self.df_pt["daily_diff_ma"],
                            name="7 days moving average"),
                    row = 1, col = 1,secondary_y=True)
        fig.add_trace(go.Bar(x=self.df_pt["date"], y=self.df_pt["daily_diff"],
                            opacity=0.4, name='daily doses'),
                    row = 1, col = 1,secondary_y=True)

        fig.update_layout(title=f'Daily rythm of COVID-19 vaccination doses administered in {self.country}')
        fig.update_yaxes(title_text="Doses per day", secondary_y=True)
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return graphJSON

    def total_doses(self):
        fig = make_subplots(1,1,specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Line(x=self.df_pt["date"], y=self.df_pt["total_vaccinations"],
                            name="total vaccinations"),
                    row = 1, col = 1,secondary_y=True)

        fig.add_trace(go.Line(x=self.df_pt["date"], y=self.df_pt["population"],
                            name="population"),
                    row = 1, col = 1,secondary_y=True)

        fig.add_trace(go.Line(x=self.df_pt["date"], y=self.df_pt["population"]*self.p,
                            name="herd immunity"),
                    row = 1, col = 1,secondary_y=True)

        fig.update_layout(title=f'Total COVID-19 vaccination doses administered in {self.country}')
        fig.update_yaxes(title_text="Total doses", secondary_y=True)
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return graphJSON
