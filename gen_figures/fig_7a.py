from utils.plot_from_dicts import plotfigure
import json

dict_plot1 = {}
dict_plot1["no_of_plots"] = 6
dict_plot1["file_name"] = "img/fig_7a.pdf"
dict_plot1["str_label_common"] = '$\mu_u = $'
dict_plot1["x_label"] = 'Admission Probability of uplink ($\lambda_u$)'
dict_plot1["y_label"] = 'Expected Reward'


with open('jsons/sim3_data3_085.json') as f:
    DATA1 = json.load(f)

with open('jsons/sim3_data_055_0.45_10000x1000.json') as f:
    DATA2 = json.load(f)

with open('jsons/sim8_data_055_10000x1000.json') as f:
    DATA3 = json.load(f)
    
with open('jsons/sim3_data_055_0.3_10000x1000.json') as f:
    DATA4 = json.load(f)    
            
dict_plot1["0"] = {}
dict_plot1["0"]["data"] = DATA1["rewards"]['0.55']['0.4']['0.45']
dict_plot1["0"]["str_label_specific"] = '$0.45$, Analytical - Relaxed'
dict_plot1["0"]["plot_args"] = 'round'

dict_plot1["1"] = {}
dict_plot1["1"]["data"] = DATA2["mean"]['0.55']['0.4']['0.45']
dict_plot1["1"]["str_label_specific"] = '$\mu_u = 0.45$, Simulation - Relaxed'
dict_plot1["1"]["plot_args"] = 'square'

dict_plot1["2"] = {}
dict_plot1["2"]["data"] = DATA3["mean"]['0.55']['0.4']['0.45']
dict_plot1["2"]["str_label_specific"] = '$\mu_u = 0.45$, Simulation - Actual'
dict_plot1["2"]["plot_args"] = 'square'

dict_plot1["3"] = {}
dict_plot1["3"]["data"] = DATA1["rewards"]['0.55']['0.4']['0.3']
dict_plot1["3"]["str_label_specific"] = '$0.3$, Analytical - Relaxed'
dict_plot1["3"]["plot_args"] = 'round'

dict_plot1["4"] = {}
dict_plot1["4"]["data"] = DATA4["mean"]['0.55']['0.4']['0.3']
dict_plot1["4"]["str_label_specific"] = '$\mu_u = 0.3$, Simulation - Relaxed'
dict_plot1["4"]["plot_args"] = 'square'

dict_plot1["5"] = {}
dict_plot1["5"]["data"] = DATA3["mean"]['0.55']['0.4']['0.3']
dict_plot1["5"]["str_label_specific"] = '$\mu_u = 0.3$, Simulation - Actual'
dict_plot1["5"]["plot_args"] = 'square'

plotfigure(dict_plot1)
