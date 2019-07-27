import pandas as pd
import numpy as np
import dash_html_components as html

def signif(fit_result_table):
    coef_table = pd.DataFrame(fit_result_table[1].data,  columns =  ['variable','coef','std err','z','P>|z|','[0.025','0.975]']).\
                                                                    set_index('variable')
    # first row is columns names, drop it
    coef_table = coef_table.drop([''], axis = 0)
    coef_table['P>|z|'] = [np.round(i,4) for i in coef_table['P>|z|'].astype(np.float32)]
        # define a significance column similar to R
    coef_table[' '] = ['ooo' if i<0.001 else 'oo' if i>0.001 and i<=.01\
                  else 'o'  if i>.01 and i <=.05\
                  else '.'  if i>.05 and i <=.1 else ' ' for i in coef_table.iloc[:,3]]

    return(coef_table)


def formula_builder(*all_vars):

  trnsfrm_dict =  {"native":"{}", "x^2":"pow({},2)", "x^3":"pow({},3)", "log(x)":"np.log({})", "e^x":"np.exp({})", "sq.rt":"np.sqrt({})"}
  dsply_dict    = {"native":"{}", "x^2":"{}^2",      "x^3":"{}^3",      "log(x)":"ln({})",     "e^x":"e^{}",       "sq.rt":"sq.rt({})"}
  inp   = all_vars[0][0].copy()
  dsp   = all_vars[0][0].copy()
  rqust = list(all_vars[0][1:])
  rqust_format = [trnsfrm_dict.get(i) for i in rqust]
  disp_format  = [dsply_dict.get(i)   for i in rqust]
  bare  = ["Murder"]

  if "Murder" in inp:
    mur_ind = inp.index("Murder")
    inp[mur_ind] = rqust_format[0].format("Murder")
    dsp[mur_ind] =  disp_format[0].format("Murder")


  if "Population" in inp:
    pop_ind = inp.index("Population")
    inp[pop_ind] = rqust_format[1].format("Population")
    dsp[pop_ind] =  disp_format[1].format("Population")
    bare.insert(pop_ind, "Population")

  if "Income" in inp:
    in_ind = inp.index("Income")
    inp[in_ind] = rqust_format[2].format("Income")
    dsp[in_ind] =  disp_format[2].format("Income")
    bare.insert(in_ind, "Income")

  if "Illiteracy" in inp:
    il_ind = inp.index("Illiteracy")
    inp[il_ind] = rqust_format[3].format("Illiteracy")
    dsp[il_ind] =  disp_format[3].format("Illiteracy")
    bare.insert(il_ind, "Illiteracy")

  if "Life_Exp" in inp:
    lf_ind = inp.index("Life_Exp")
    inp[lf_ind] = rqust_format[4].format("Life_Exp")
    dsp[lf_ind] =  disp_format[4].format("Life_Exp")
    bare.insert(lf_ind, "Life_Exp")

  if "HS_Grad" in inp:
    hs_ind = inp.index("HS_Grad")
    inp[hs_ind] = rqust_format[5].format("HS_Grad")
    dsp[hs_ind] =  disp_format[5].format("HS_Grad")
    bare.insert(hs_ind, "HS_Grad")

  if "Frost" in inp:
    fr_ind = inp.index("Frost")
    inp[fr_ind] = rqust_format[6].format("Frost")
    dsp[fr_ind] =  disp_format[6].format("Frost")
    bare.insert(fr_ind, "Frost")

  if "Area" in inp:
    ar_ind = inp.index("Area")
    inp[ar_ind] = rqust_format[7].format("Area")
    dsp[ar_ind] =  disp_format[7].format("Area")
    bare.insert(ar_ind, "Area")

  if len(inp) > 1:
    frmla = inp[0] + ' ~ ' "1 + " + ' + '.join(inp[1:])
    dspf  = dsp[0] + ' ~ ' "1 + " + ' + '.join(dsp[1:])
    br    = bare[0]+ ' ~ ' "1 + " + ' + '.join(bare[1:])
  else:
    frmla = inp[0] + ' ~ ' "1 "
    dspf  = dsp[0] + ' ~ ' "1 "
    br    = bare[0]+ ' ~ ' "1 "

  return(frmla, dspf, br)

def df_to_table(df):
    return html.Table(
                      [html.Tr([html.Th(col) for col in df.columns])] +
                      [html.Tr(
                              [html.Td(df.iloc[i][col]) for col in df.columns]
                              )
                              for i in range(len(df))], style = {"fontSize": 15, "font-family":"Roboto Mono"}
                    )
