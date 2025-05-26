from utils.plot_from_dicts import plotfigure
import json

dict_plot1 = {}
dict_plot1["no_of_plots"] = 4
dict_plot1["file_name"] = "img/fig_3.pdf"
dict_plot1["str_label_common"] = '$\mu_u = $'
dict_plot1["x_label"] = 'Admission Probability of uplink ($\lambda_u$)'
dict_plot1["y_label"] = '$\overline{AoL}$'


with open('jsons/sim12_aaoi_data_sim_ana_lcfs_fcfs.json') as f:
    DATA1 = json.load(f)
    
dict_plot1["0"] = {}
dict_plot1["0"]["data"] = DATA1["lcfs1_ana"]['0.3']
dict_plot1["0"]["str_label_specific"] = '$0.3$ - Analytical'
dict_plot1["0"]["plot_args"] = 'round'

dict_plot1["1"] = {}
dict_plot1["1"]["data"] = DATA1["lcfs1_sim"]['0.3']
dict_plot1["1"]["str_label_specific"] = '$0.3$ - Simulation'
dict_plot1["1"]["plot_args"] = 'square'

dict_plot1["2"] = {}
dict_plot1["2"]["data"] = DATA1["lcfs1_ana"]['0.45']
dict_plot1["2"]["str_label_specific"] = '$0.45$ - Analytical'
dict_plot1["2"]["plot_args"] = 'round'

dict_plot1["3"] = {}
dict_plot1["3"]["data"] = DATA1["lcfs1_sim"]['0.45']
dict_plot1["3"]["str_label_specific"] = '$0.45$ - Simulation'
dict_plot1["3"]["plot_args"] = 'square'

plotfigure(dict_plot1)
