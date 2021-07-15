import json
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from plotly.subplots import make_subplots
import plotly


class OwidData:
    R0 = 2.5
    p_raw = 1 - (1 / R0)
    IMUNE = 0.044
    VACCINE_EFFICIENCY = 0.95
    p = (1 - 1 / R0 - IMUNE) / VACCINE_EFFICIENCY
    P = 0.7

    def __init__(self):
        owid_data = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv"
        self.df = pd.read_csv(owid_data)
        self.df.date = pd.to_datetime(self.df.date)
        self.columns_ = [
            "date",
            "location",
            "iso_code",
            "total_vaccinations",
            "population",
        ]

        self.df_pt = self.group_country()

    def group_country(self, country="Portugal"):
        """download data and group by country"""
        self.country = country
        df_pt = self.df[self.columns_].copy()
        df_pt = df_pt[df_pt.location == self.country]
        df_pt = df_pt[df_pt.date > "2021-01-01"]  # first date
        # df_pt.fillna(method="bfill", limit=1, inplace=True)
        df_pt.interpolate(method="linear", inplace=True)
        df_pt["total_vaccinations_ma"] = df_pt.total_vaccinations.rolling(7).mean()
        df_pt["daily_diff"] = df_pt.total_vaccinations.diff()
        df_pt["daily_diff_ma"] = df_pt.daily_diff.rolling(7).mean()
        time_span = df_pt.date.apply(lambda x: (x - df_pt.date.min()).days)  # days
        df_pt["due_date"] = (
            (df_pt.population * self.p) * time_span / (df_pt.total_vaccinations / 2)
        )
        # df_pt.dropna(inplace=True)
        return df_pt

    def last_update(self):
        remaining_pop = "{0:,}".format(
            int(
                self.df_pt.tail(1).population
                - (self.df_pt.tail(1).total_vaccinations / 2)
            )
        )
        remaining_days = "{0:,}".format(int(self.df_pt.tail(1).due_date))
        last_ma = "{0:,}".format(int(self.df_pt.tail(1).daily_diff_ma))
        total_pop = "{0:,}".format(int(self.df_pt.tail(1).population))
        update_date = self.df_pt.tail(1).date.to_string().split(" ")[-1]
        return remaining_pop, remaining_days, last_ma, total_pop, update_date

    def daily_doses(self):
        """graph daily doses injected with 7 days moving average"""
        fig = make_subplots(1, 1, specs=[[{"secondary_y": True}]])
        fig.add_trace(
            go.Line(
                x=self.df_pt["date"],
                y=self.df_pt["daily_diff_ma"],
                name="7 days moving average",
            ),
            row=1,
            col=1,
            secondary_y=True,
        )
        fig.add_trace(
            go.Bar(
                x=self.df_pt["date"],
                y=self.df_pt["daily_diff"],
                opacity=0.4,
                name="daily doses",
            ),
            row=1,
            col=1,
            secondary_y=True,
        )

        fig.update_layout(
            title=f"Daily rythm of COVID-19 vaccination doses administered in {self.country}"
        )
        fig.update_yaxes(title_text="Doses per day", secondary_y=True)
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return fig

    def total_doses(self):
        """graph total doses injected and herd immunity target"""
        fig = make_subplots(1, 1, specs=[[{"secondary_y": True}]])
        fig.add_trace(
            go.Line(
                x=self.df_pt["date"],
                y=self.df_pt["total_vaccinations"],
                name="total doses",
            ),
            row=1,
            col=1,
            secondary_y=True,
        )

        # fig.add_trace(
        #     go.Line(
        #         x=self.df_pt["date"],
        #         y=self.df_pt["population"] * 2,
        #         name="population * 2",
        #     ),
        #     row=1,
        #     col=1,
        #     secondary_y=True,
        # )

        fig.add_trace(
            go.Line(
                x=self.df_pt["date"],
                y=self.df_pt["population"] * self.p * 2,
                name="herd immunity",
                line=dict(color="#8BE639", width=4, dash="dot"),
            ),
            row=1,
            col=1,
            secondary_y=True,
        )

        fig.update_layout(
            title=f"Total COVID-19 vaccination doses administered in {self.country}"
        )
        fig.update_yaxes(title_text="Total doses", secondary_y=True)
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return fig

    def waffle_plot(self):
        z = np.ones((10, 10), dtype=int)

        fully_vax = 16  # 3
        one_dose = 36 - fully_vax  # 4
        herd_immun = 100 - 58  # 1
        remaining = 100 - (herd_immun + fully_vax + one_dose)  # 2

        fv = fully_vax
        od = one_dose
        rm = remaining
        # because Heatmap colorscale logic sucks.
        colorscale = [
            [0, "#CFA9A9"],
            [0.33, "#ED5858"],
            [0.66, "#1F8039"],
            [1, "#2DBD54"],
        ]

        customdata = []
        for x in range(len(z[0, :])):
            for y in range(len(z[:, 0])):
                if fv > 0:
                    z[y, x] = 3
                    fv -= 1
                    customdata.append(f"two doses ({fully_vax}%)")
                elif od > 0:
                    z[y, x] = 4
                    od -= 1
                    customdata.append(f"at least a dose ({one_dose}%)")
                elif rm > 0:
                    z[y, x] = 2
                    rm -= 1
                    customdata.append(f"remaining to vaccinate ({remaining}%)")
                else:
                    customdata.append(f"protected ({herd_immun}%)")
        customdata = np.reshape(customdata, newshape=(10, 10)).T

        fig = go.Figure(
            go.Heatmap(
                x=[1],
                y=[1],
                z=z,
                customdata=customdata,
                xgap=1,
                ygap=1,
                colorscale=colorscale,
                showscale=False,
                hovertemplate="%{customdata}<extra></extra>",
            )
        )
        fig.update_layout(width=600, height=450, yaxis_autorange="reversed")
        return fig
