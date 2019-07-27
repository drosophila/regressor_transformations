import pandas as pd
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf
import os

df = pd.read_csv("data/source/state.x77.csv", header = 0)
cols = df.columns.tolist()
y_col  = cols[4]
x_col = cols[0:4] + cols[5:]
avail_tsfm = ["native", "x^2", "x^3", "log(x)", "e^x", "sq.rt"]


import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import dash_table as dt
from utils import signif, formula_builder, df_to_table
from layouts import layout_obj

layout = layout_obj

app = dash.Dash()
app.layout = layout


@app.callback(
    Output("formula","children"),
    [Input("select_inputs",   "values"),
     Input("murder_radio",    "value"),
     Input("population_radio","value"),
     Input("income_radio",    "value"),
     Input("illiteracy_radio","value"),
     Input("life_exp_radio",  "value"),
     Input("hs_grad_radio",   "value"),
     Input("frost_radio",     "value"),
     Input("area_radio",      "value")]
     )
def update_formula(*sdv):
  sdv[0].insert(0, "Murder")
  _, disp, _ = formula_builder(sdv)

  return "Regression formula: {}".format(disp)

@app.callback(
    Output("statsmodels","children"),
    [Input("select_inputs",   "values"),
     Input("murder_radio",    "value"),
     Input("population_radio","value"),
     Input("income_radio",    "value"),
     Input("illiteracy_radio","value"),
     Input("life_exp_radio",  "value"),
     Input("hs_grad_radio",   "value"),
     Input("frost_radio",     "value"),
     Input("area_radio",      "value")]
     )
def update_formula(*sdv):
  sdv[0].insert(0, "Murder")
  frmla, _,_ = formula_builder(sdv)

  return "Statsmodels formula: {}".format(frmla)


@app.callback(
    Output("html_table_1","children"),
    [Input("select_inputs",   "values"),
     Input("murder_radio",    "value"),
     Input("population_radio","value"),
     Input("income_radio",    "value"),
     Input("illiteracy_radio","value"),
     Input("life_exp_radio",  "value"),
     Input("hs_grad_radio",   "value"),
     Input("frost_radio",     "value"),
     Input("area_radio",      "value")]
     )
def html_table_update(*sdv):
  sdv[0].insert(0, "Murder")
  formula_ ,_,_ = formula_builder(sdv)
  lmod = smf.ols(formula = formula_, data = df)
  results = lmod.fit()
  coef_df = signif(results.summary().tables).reset_index(drop = False)
  return df_to_table(coef_df)

@app.callback(
    Output("html_table_2","children"),
    [Input("select_inputs",   "values"),
     Input("murder_radio",    "value"),
     Input("population_radio","value"),
     Input("income_radio",    "value"),
     Input("illiteracy_radio","value"),
     Input("life_exp_radio",  "value"),
     Input("hs_grad_radio",   "value"),
     Input("frost_radio",     "value"),
     Input("area_radio",      "value")]
     )
def html_table_update(*sdv):
  sdv[0].insert(0, "Murder")
  _,_, formula_ = formula_builder(sdv)
  lmod = smf.ols(formula = formula_, data = df)
  results = lmod.fit()
  coef_df = signif(results.summary().tables).reset_index(drop = False)
  return df_to_table(coef_df)


@app.callback(
    Output("residvsfttd","figure"),
    [Input("select_inputs",   "values"),
     Input("murder_radio",    "value"),
     Input("population_radio","value"),
     Input("income_radio",    "value"),
     Input("illiteracy_radio","value"),
     Input("life_exp_radio",  "value"),
     Input("hs_grad_radio",   "value"),
     Input("frost_radio",     "value"),
     Input("area_radio",      "value")]
     )
def residvsfttd(*sdv):
  sdv[0].insert(0, "Murder")
  formula_ ,_,_ = formula_builder(sdv)
  lmod = smf.ols(formula = formula_, data = df)
  results = lmod.fit()
  resids = results.resid
  ftd    = results.fittedvalues
  residvsfttd =  go.Scatter({ "y": resids,
                              "x": ftd,
                              "mode": "markers",
                              #"line": {"color": "#8c8c8c", "dash": "dash", "width": 1},
                              #"name": "Residuals vs fitted-values",
                              "hoverinfo": "skip"})

  plot_layout = {'title': "Residuals vs fitted-values",
                 'xaxis': {"title": "fitted-values"},
                 'yaxis': {"title": "residuals"},
                 'height': '400',
                 'width' : '400'
                 }

  return {"data": [residvsfttd], "layout": plot_layout}

@app.callback(
    Output("residsonly","figure"),
    [Input("select_inputs",   "values"),
     Input("murder_radio",    "value"),
     Input("population_radio","value"),
     Input("income_radio",    "value"),
     Input("illiteracy_radio","value"),
     Input("life_exp_radio",  "value"),
     Input("hs_grad_radio",   "value"),
     Input("frost_radio",     "value"),
     Input("area_radio",      "value")]
     )
def residsonly(*sdv):
  sdv[0].insert(0, "Murder")
  formula_ ,_,_ = formula_builder(sdv)
  lmod = smf.ols(formula = formula_, data = df)
  results = lmod.fit()
  resids = results.resid
  norm = np.random.normal(np.mean(resids), np.std(resids), len(resids))
  #x_axis = np.linspace(0, len(resids), num = len(resids))
  x_axis = np.arange(0,len(resids))
  residsonly =  go.Scatter({ "y": resids,
                              "x": x_axis,
                              "mode": "markers",
                              "marker": {"color": "#ff0000"},
                              "hoverinfo": "skip"})
  norms =  go.Scatter({       "y": norm,
                              "x": x_axis,
                              "mode": "markers",
                              "marker": {"color": "#ffb3ff"},
                              "hoverinfo": "skip"})
  plot_layout = {'title': "Residuals",
                 'xaxis': {"title": "observations"},
                 'yaxis': {"title": "residuals"},
                 'height': '400',
                 'width' : '400'
                 }

  return {"data": [residsonly, norms], "layout": plot_layout}

@app.callback(
    Output("residvsfttd_n","figure"),
    [Input("select_inputs",   "values"),
     Input("murder_radio",    "value"),
     Input("population_radio","value"),
     Input("income_radio",    "value"),
     Input("illiteracy_radio","value"),
     Input("life_exp_radio",  "value"),
     Input("hs_grad_radio",   "value"),
     Input("frost_radio",     "value"),
     Input("area_radio",      "value")]
     )
#_,_, formula_ = formula_builder(sdv)
#  lmod = smf.ols(formula = formula_, data = df)
#  results = lmod.fit()
#  coef_df = signif(results.summary().tables).reset_index(drop = False)
def residvsfttd(*sdv):
  sdv[0].insert(0, "Murder")
  _,_, formula_ = formula_builder(sdv)
  lmod = smf.ols(formula = formula_, data = df)
  results = lmod.fit()
  resids = results.resid
  ftd    = results.fittedvalues
  residvsfttd =  go.Scatter({ "y": resids,
                              "x": ftd,
                              "mode": "markers",
                              #"line": {"color": "#8c8c8c", "dash": "dash", "width": 1},
                              #"name": "Residuals vs fitted-values",
                              "hoverinfo": "skip"})

  plot_layout = {'title': "Residuals vs fitted-values",
                 'xaxis': {"title": "fitted-values"},
                 'yaxis': {"title": "residuals"},
                 'height': '400',
                 'width' : '400'
                 }

  return {"data": [residvsfttd], "layout": plot_layout}

@app.callback(
    Output("residsonly_n","figure"),
    [Input("select_inputs",   "values"),
     Input("murder_radio",    "value"),
     Input("population_radio","value"),
     Input("income_radio",    "value"),
     Input("illiteracy_radio","value"),
     Input("life_exp_radio",  "value"),
     Input("hs_grad_radio",   "value"),
     Input("frost_radio",     "value"),
     Input("area_radio",      "value")]
     )
def residsonly(*sdv):
  sdv[0].insert(0, "Murder")
  _,_, formula_ = formula_builder(sdv)
  lmod = smf.ols(formula = formula_, data = df)
  results = lmod.fit()
  resids = results.resid
  norm = np.random.normal(np.mean(resids), np.std(resids), len(resids))
  #x_axis = np.linspace(0, len(resids), num = len(resids))
  x_axis = np.arange(0,len(resids))
  residsonly =  go.Scatter({ "y": resids,
                              "x": x_axis,
                              "mode": "markers",
                              "marker": {"color": "#ff0000"},
                              "hoverinfo": "skip"})
  norms =  go.Scatter({       "y": norm,
                              "x": x_axis,
                              "mode": "markers",
                              "marker": {"color": "#ffb3ff"},
                              "hoverinfo": "skip"})
  plot_layout = {'title': "Residuals",
                 'xaxis': {"title": "observations"},
                 'yaxis': {"title": "residuals"},
                 'height': '400',
                 'width' : '400'
                 }

  return {"data": [residsonly, norms], "layout": plot_layout}

if __name__ == "__main__":
    app.run_server(debug = True)