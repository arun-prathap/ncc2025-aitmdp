from utils.plot_from_dicts import plotfigure
import json

dict_plot1 = {}
dict_plot1["no_of_plots"] = 4
dict_plot1["file_name"] = "img/fig_8a.pdf"
dict_plot1["str_label_common"] = 'TPM - '
dict_plot1["x_label"] = 'Admission Probability of uplink ($\lambda_u$)'
dict_plot1["y_label"] = 'Expected Rewards'


with open('jsons/sim12_data3_055_s6.json') as f:
    DATA1 = json.load(f)
    
dict_plot1["0"] = {}
dict_plot1["0"]["data"] = DATA1["1"]["rewards"]['0.45']['0.25']['0.45']
dict_plot1["0"]["str_label_specific"] = '$1$'
dict_plot1["0"]["plot_args"] = 'square'

dict_plot1["1"] = {}
dict_plot1["1"]["data"] = DATA1["7"]["rewards"]['0.45']['0.25']['0.45']
dict_plot1["1"]["str_label_specific"] = '$7$'
dict_plot1["1"]["plot_args"] = 'square'

dict_plot1["2"] = {}
dict_plot1["2"]["data"] = DATA1["8"]["rewards"]['0.45']['0.25']['0.45']
dict_plot1["2"]["str_label_specific"] = '$8$'
dict_plot1["2"]["plot_args"] = 'square'

dict_plot1["3"] = {}
dict_plot1["3"]["data"] = DATA1["12"]["rewards"]['0.45']['0.25']['0.45']
dict_plot1["3"]["str_label_specific"] = '$12$'
dict_plot1["3"]["plot_args"] = 'square'

plotfigure(dict_plot1)
