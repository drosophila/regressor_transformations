import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

df = pd.read_csv("data/source/state.x77.csv", header = 0)
cols = df.columns.tolist()
y_col  = cols[4]
x_col = cols[0:4] + cols[5:]
avail_tsfm = ["native", "x^2", "x^3", "log(x)", "e^x", "sq.rt"]

layout_obj =\
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
                          }), #from here
                  html.Div([
                    html.Div([dcc.Graph(id = "residvsfttd")],style = {"width"  : '45%','display': 'inline-block','position': 'relative'}),
                    html.Div([],style = {"width"  : '10%','display': 'inline-block','position': 'relative'}),
                    html.Div([dcc.Graph(id = "residsonly"),],style = {"width"  : '45%','display': 'inline-block','position': 'relative'}),
                    ]),
                  #to here
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
                          }),
                  html.Div([
                    html.Div([dcc.Graph(id = "residvsfttd_n")],style = {"width"  : '45%','display': 'inline-block','position': 'relative'}),
                    html.Div([],style = {"width"  : '10%','display': 'inline-block','position': 'relative'}),
                    html.Div([dcc.Graph(id = "residsonly_n"),],style = {"width"  : '45%','display': 'inline-block','position': 'relative'}),
                    ]),
                ], style = {"width"  : '48%','display': 'inline-block','position': 'relative'})
              ]), #branch2 end

    html.Div(id = "diags",
             style={"marginLeft": 20,"marginTop": 25,"marginBottom": 0,"fontSize": 14, "font-family":"Roboto Mono"}),
    #dcc.Graph(id = "residvsfttd"),
    #dcc.Graph(id = "residsonly"),
    html.Div(id = "space",
            style={"marginTop": 25,"marginBottom": 150,"fontSize": 20, "font-family":"Roboto Mono"})

])