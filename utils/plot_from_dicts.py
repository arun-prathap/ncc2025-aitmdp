import os

import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import scienceplots
plt.style.use(['science','ieee'])

matplotlib.use('TkAgg')

def plotfigure(dict_array, operator=None):
    
    fig, subplot = plt.subplots()
    
    for i in range(dict_array["no_of_plots"]):
        data_dict = dict_array[str(i)]
        
        DF3 = pd.Series(data_dict["data"])
        print(DF3)

        xindex = np.array(DF3.index.to_list(), dtype=np.float32)        
        df_array1 = np.array(DF3.T)
        
        x = xindex
        y = df_array1
        
        if operator is not None:
            if operator == '-np.log':
                y = -np.log(y)
            else:
                raise Exception("Unknown Operator")
        
        if i <= 3:
            if data_dict["plot_args"] == "square":
                subplot.plot(x, y, label=dict_array["str_label_common"]+str(data_dict["str_label_specific"]),marker="s", ms=1)
            elif data_dict["plot_args"] == "round":
                subplot.plot(x, y, label=dict_array["str_label_common"]+str(data_dict["str_label_specific"]),marker="o", markerfacecolor="None",ms=3)
            else:
                raise Exception("Only square and round plot args supported")

        elif i == 4:
            if data_dict["plot_args"] == "square":
                subplot.plot(x, y, label=dict_array["str_label_common"]+str(data_dict["str_label_specific"]),linestyle=(5, (10, 3)),color='c',marker="s", ms=1)
            elif data_dict["plot_args"] == "round":
                subplot.plot(x, y, label=dict_array["str_label_common"]+str(data_dict["str_label_specific"]),linestyle=(5, (10, 3)),color='c',marker="o", markerfacecolor="None",ms=3)
            else:
                raise Exception("Only square and round plot args supported")
                
        elif i == 5:
            if data_dict["plot_args"] == "square":
                subplot.plot(x, y, label=dict_array["str_label_common"]+str(data_dict["str_label_specific"]), linestyle=(0, (3, 1,1,1)),color='m',marker="s", ms=1)
            elif data_dict["plot_args"] == "round":
                subplot.plot(x, y, label=dict_array["str_label_common"]+str(data_dict["str_label_specific"]), linestyle=(0, (3, 1,1,1)),color='m',marker="o", markerfacecolor="None",ms=3)
            else:
                raise Exception("Only square and round plot args supported")
                
        else:
            raise Exception("Only 6 plots supported")

    subplot.set_xlabel(dict_array["x_label"])
    subplot.set_ylabel(dict_array["y_label"])
    subplot.legend()
    plt.grid()

    plt.savefig(dict_array["file_name"], format="pdf")
