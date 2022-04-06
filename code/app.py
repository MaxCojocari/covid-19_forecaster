import numpy as np
import pandas as pd
import plotly.graph_objects as go
from sktime.forecasting.arima import AutoARIMA
from datetime import datetime, timedelta, date

import streamlit as st 

ALL = "All Cumulaive Series - No Forecast"
CASES = "Total Cases"
DEATHS = "Total Deaths"
RECOVERIES = "Total Recoveries"


@st.cache(allow_output_mutation=True)
def make_forecast(selection, df, input_fh):
    """Takes a name from the selection and makes a forecast plot."""

    if selection == CASES:

        cumulative_series_name = "cumulative_cases"
        title = "Daily Cases"
        y_label = "Cases"

    if selection == DEATHS:

        cumulative_series_name = "cumulative_deaths"
        title = "Daily Deaths"
        y_label = "Deaths"

    if selection == RECOVERIES:

        cumulative_series_name = "cumulative_recoveries"
        title = "Daily Recoveries"
        y_label = "Recoveries"


    #Setting the forecasting horizon
    fh = np.arange(1, input_fh+1)

    from sktime.forecasting.arima import ARIMA
    forecaster = ARIMA(
        order=(2, 1, 2), seasonal_order=(1, 0, 1, 7), suppress_warnings=True
    )

    forecaster.fit(df)

    alpha = 0.05  
    df_pred, df_pred_ints = forecaster.predict(fh, return_pred_int=True, alpha=alpha)
    
    new_pd = pd.concat([df_pred_ints["upper"], df_pred_ints["lower"][::-1]])

    # Create traces
    fig = go.Figure()
    df = df['2022-01-01':]

    fig.add_trace(go.Scatter(x=df.index.strftime('%Y-%m-%d'), 
                             y=df.values, 
                             line_color='rgb(0, 64, 255)',
                             mode='lines+markers', 
                             name='actual data'))
    fig.add_trace(go.Scatter(x=df_pred.index.strftime('%Y-%m-%d'), 
                             y=df_pred.values, 
                             line_color='rgb(255, 102, 0)',
                             mode='lines+markers', 
                             name='prediction'))
    fig.add_trace(go.Scatter(x=new_pd.index.strftime('%Y-%m-%d'),
                             y=new_pd.values,
                             fill='toself',
                             fillcolor='rgba(255, 102, 0, 0.2)',
                             line_color='rgba(255 , 255, 255, 0)',
                             showlegend=True,
                             name='confidence interval'))
    fig.update_layout(title=title,
                      xaxis_title="Date",
                      yaxis_title=y_label)
    

    return fig

def plot_graph(selected_series, y, input_fh):
    y.index = pd.PeriodIndex(y.index, freq='D')
    plotly_fig = make_forecast(selected_series, y, input_fh)
    st.plotly_chart(plotly_fig)
        




cases = pd.read_csv('/content/drive/MyDrive/PBL_sem2/cases_covid_de.csv',
                        index_col=0, squeeze=True, dtype={1: float})

deaths = pd.read_csv('/content/drive/MyDrive/PBL_sem2/deaths_covid_de.csv',
                        index_col=0, squeeze=True, dtype={1: float})

recovered = pd.read_csv('/content/drive/MyDrive/PBL_sem2/recovered_covid_de.csv',
                        index_col=0, squeeze=True, dtype={1: float})


st.write("# COVID-19 Forecast in Germany")

selected_series = st.selectbox("Select data to forecast:", (ALL, CASES, DEATHS, RECOVERIES))



if selected_series in [CASES, DEATHS, RECOVERIES]:

    today = pd.Timestamp(datetime.today())
    

    x = cases.copy()
    x.index = pd.PeriodIndex(x.index, freq='D')
    data_time = x.index.to_timestamp()
    
    fin_date = datetime.strptime("2022-12-31", "%Y-%m-%d")

    default_date = data_time[-1] + timedelta(days=1)

    end_date = st.date_input(
            "Select end date for forecasting:",
            default_date,
            min_value=default_date,
            max_value=fin_date,
        )

    fh_lengh = pd.Timestamp(end_date) - data_time[-1]
    
    st.write("Forecasting interval: " + str(fh_lengh.days) + " days")
    
    if fh_lengh.days > 0:
        if selected_series == CASES:
            plot_graph(selected_series, cases, fh_lengh.days)
        elif selected_series == DEATHS:
            plot_graph(selected_series, deaths, fh_lengh.days)
        else:
            plot_graph(selected_series, recovered, fh_lengh.days)
        
else:
    start_date = '2022-01-01'

    df_cases = pd.read_csv('/content/drive/MyDrive/PBL_sem2/cases_covid_de.csv')
    select_data_cases = df_cases.loc[df_cases['date'] >= start_date]
    
    df_deaths = pd.read_csv('/content/drive/MyDrive/PBL_sem2/deaths_covid_de.csv')
    select_data_deaths = df_deaths.loc[df_deaths['date'] >= start_date]
    
    df_recovered = pd.read_csv('/content/drive/MyDrive/PBL_sem2/recovered_covid_de.csv')
    select_data_recovered = df_recovered.loc[df_recovered['date'] >= start_date]

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=select_data_cases['date'], y=select_data_cases['cases'],
                        mode='lines+markers',
                        name='daily cases'))
    fig.add_trace(go.Scatter(x=select_data_deaths['date'], y=select_data_deaths['deaths']*100,
                        mode='lines+markers',
                        name='deaths*100'))
    fig.add_trace(go.Scatter(x=select_data_recovered['date'], y=select_data_recovered['recovered'],
                        mode='lines+markers', 
                        name='recovered'))

    fig.update_layout(title='Daily Series',
                    xaxis_title='Date',
                    yaxis_title='Number of people')
    st.plotly_chart(fig)

