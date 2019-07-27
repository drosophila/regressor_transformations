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


layout =\
  html.Div([ #master
    html.H2(children = "Regression",
        style={"marginTop": 25,"marginBottom": 10, "font-family":"Roboto Mono"}),
    html.Div(id = 'formula',
             style={"marginTop": 25,"marginBottom": 10,"fontSize": 14, "font-family":"Roboto Mono"}),
    html.Div(id = 'statsmodels',
             style={"marginTop": 15,"marginBottom": 10,"fontSize": 14, "font-family":"Roboto Mono"}),
    html.Div(id = "inputs",
             children = "Select inputs or intercept only model",
             style={"marginTop": 25,"marginBottom": 10,"fontSize": 20, "font-family":"Roboto Mono"}),
    html.Div([ #branch1
                  html.Div([
                      html.Div(id = "output",
                              children = "Murder",
                              style={"marginLeft": 20,"marginTop": 25,"marginBottom": 0,"fontSize": 14, "font-family":"Roboto Mono"}
                              ),
                      dcc.Checklist(id = "select_inputs",
                                   options = [{"label": i,"value": i} for i in x_col],
                                   values = ["Population"],
                                   style={"marginTop": 0,"marginBottom": 10,"fontSize": 14, "font-family":"Roboto Mono"},
                                   labelStyle = {"display": "list-item", "textAligh": "left"}
                                   )

                      ], style = {"width"  : '10%','display': 'inline-block','position': 'relative'}),


                  html.Div([], style = {"width"  : '3%','display': 'inline-block','position': 'relative'}),

                  html.Div([
                      dcc.RadioItems(id = "murder_radio",
                                    options = [{"label": i,"value": i} for i in avail_tsfm],
                                    labelStyle = {"display": "inline-block"},
                                    style={"marginTop": 1,"marginBottom": 1,"fontSize": 12, "font-family":"Roboto Mono"},
                                    value = "native"
                                    ),
                      dcc.RadioItems(id = "population_radio",
                                    options = [{"label": i,"value": i} for i in avail_tsfm],
                                    labelStyle = {"display": "inline-block"},
                                    style={"marginTop": 1,"marginBottom": 1,"fontSize": 12, "font-family":"Roboto Mono"},
                                    value = "native",
                                    ),
                      dcc.RadioItems(id = "income_radio",
                                    options = [{"label": i,"value": i} for i in avail_tsfm],
                                    labelStyle = {"display": "inline-block"},
                                    style={"marginTop": 1,"marginBottom": 1,"fontSize": 12, "font-family":"Roboto Mono"},
                                    value = "native"
                                    ),
                      dcc.RadioItems(id = "illiteracy_radio",
                                    options = [{"label": i,"value": i} for i in avail_tsfm],
                                    labelStyle = {"display": "inline-block"},
                                    style={"marginTop": 1,"marginBottom": 1,"fontSize": 12, "font-family":"Roboto Mono"},
                                    value = "native"
                                    ),
                      dcc.RadioItems(id = "life_exp_radio",
                                    options = [{"label": i,"value": i} for i in avail_tsfm],
                                    labelStyle = {"display": "inline-block"},
                                    style={"marginTop": 1,"marginBottom": 1,"fontSize": 12, "font-family":"Roboto Mono"},
                                    value = "native"
                                    ),
                      dcc.RadioItems(id = "hs_grad_radio",
                                    options = [{"label": i,"value": i} for i in avail_tsfm],
                                    labelStyle = {"display": "inline-block"},
                                    style={"marginTop": 1,"marginBottom": 1,"fontSize": 12, "font-family":"Roboto Mono"},
                                    value = "native"
                                    ),
                      dcc.RadioItems(id = "frost_radio",
                                    options = [{"label": i,"value": i} for i in avail_tsfm],
                                    labelStyle = {"display": "inline-block"},
                                    style={"marginTop": 1,"marginBottom": 1,"fontSize": 12, "font-family":"Roboto Mono"},
                                    value = "native"
                                    ),
                      dcc.RadioItems(id = "area_radio",
                                    options = [{"label": i,"value": i} for i in avail_tsfm],
                                    labelStyle = {"display": "inline-block"},
                                    style={"marginTop": 1,"marginBottom": 1,"fontSize": 12, "font-family":"Roboto Mono"},
                                    value = "native"
                                    ),
                      ], style = {"width"  : '50%','display': 'inline-block','position': 'relative'}),
              ]), #branch1 end
      html.Div([#branch2
                html.Div([
                  html.Div(id = "html_table_1",
                          style={
                          "maxHeight": "500px",
                          "overflowY": "scroll",
                          "padding": "8",
                          "marginTop": "5",
                          "backgroundColor":"white",
                          "border": "1px solid #C8D4E3",
                          "borderRadius": "3px",
                          "font-family": "Arial Narrow",
                          })

                ], style = {"width"  : '48%','display': 'inline-block','position': 'relative'}),

                html.Div([], style = {"width"  : '4%','display': 'inline-block','position': 'relative'}),

                html.Div([
                  html.Div(id = "html_table_2",
                          style={
                          "maxHeight": "500px",
                          "overflowY": "scroll",
                          "padding": "8",
                          "marginTop": "5",
                          "backgroundColor":"white",
                          "border": "1px solid #C8D4E3",
                          "borderRadius": "3px",
                          "font-family": "Arial Narrow",
                          })

                ], style = {"width"  : '48%','display': 'inline-block','position': 'relative'})
              ]), #branch2 end

    html.Div(id = "diags",
             style={"marginLeft": 20,"marginTop": 25,"marginBottom": 0,"fontSize": 14, "font-family":"Roboto Mono"}),
    dcc.Graph(id = "residvsfttd"),
    dcc.Graph(id = "residsonly"),
    html.Div(id = "space",
            style={"marginTop": 25,"marginBottom": 150,"fontSize": 20, "font-family":"Roboto Mono"})

])


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
                 'height': '600',
                 'width' : '600'
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
  x_axis = np.linspace(0, len(resids), num = len(resids))
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
                 'height': '600',
                 'width' : '600'
                 }

  return {"data": [residsonly, norms], "layout": plot_layout}

app.run_server(debug = True)