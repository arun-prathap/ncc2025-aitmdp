from utils.plot_from_dicts import plotfigure
import json

dict_plot1 = {}
dict_plot1["no_of_plots"] = 4
dict_plot1["file_name"] = "img/fig_8b.pdf"
dict_plot1["str_label_common"] = '$\mu_u = $'
dict_plot1["x_label"] = 'Admission Probability of uplink ($\lambda_u$)'
dict_plot1["y_label"] = 'Expected Rewards'


with open('jsons/sim12_data_055_10000x100.json') as f:
    DATA1 = json.load(f)
    
dict_plot1["0"] = {}
dict_plot1["0"]["data"] = DATA1["mean"]['0.55']['0.4']['0.3']
dict_plot1["0"]["str_label_specific"] = '$0.3$'
dict_plot1["0"]["plot_args"] = 'square'

dict_plot1["1"] = {}
dict_plot1["1"]["data"] = DATA1["mean"]['0.55']['0.4']['0.35']
dict_plot1["1"]["str_label_specific"] = '$0.35$'
dict_plot1["1"]["plot_args"] = 'square'

dict_plot1["2"] = {}
dict_plot1["2"]["data"] = DATA1["mean"]['0.55']['0.4']['0.4']
dict_plot1["2"]["str_label_specific"] = '$0.4$'
dict_plot1["2"]["plot_args"] = 'square'

dict_plot1["3"] = {}
dict_plot1["3"]["data"] = DATA1["mean"]['0.55']['0.4']['0.45']
dict_plot1["3"]["str_label_specific"] = '$0.45$'
dict_plot1["3"]["plot_args"] = 'square'

plotfigure(dict_plot1)
