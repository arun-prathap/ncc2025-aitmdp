'''
Module Description

Classes:
    None
'''
import os
import numpy as np
import json


MU_DD = [0.55]
LAMBDA_DD = [0.4]
MU_UU = [0.3,0.45]
LAMBDA_UU = np.round(np.arange(0.05,1,0.05),2)

pmf_of_aoi={}

def compute_pmf_of_aoi(lambda_, mu_, delta_):
    if lambda_ not in pmf_of_aoi:
        pmf_of_aoi[lambda_] = {}
    if mu_ not in pmf_of_aoi[lambda_]:
        pmf_of_aoi[lambda_][mu_] = {}
    if delta_ not in pmf_of_aoi[lambda_][mu_]:
        term_1 = ((mu_ - lambda_)*(((1 - mu_)/(1 - lambda_))**(delta_ + 1)))/(1 - mu_)
        term_2 = (((1 - lambda_)**(delta_ + 1)) * lambda_ * mu_)/(mu_ - lambda_)
        term_3 = lambda_ * mu_ * ((1 - mu_)**delta_)*(2 + delta_)
        term_4 = (((1 - mu_)**(delta_))*(((1 + mu_) * (lambda_**2))-(lambda_ * mu_ * (1 + 2 * mu_))+(mu_ ** 2)))/(lambda_ - mu_)    
        pmf_of_aoi[lambda_][mu_][delta_] = (term_1 + term_2 - term_3 + term_4)
    return pmf_of_aoi[lambda_][mu_][delta_]

def dump_aoi_ana_info_to_file():
    # variable change to avoid changing inside loop
    mu_uu = MU_DD
    lambda_uu = LAMBDA_DD
    mu_dd = MU_UU
    lambda_dd = LAMBDA_UU
    
    #no_of_steps = NO_OF_STEPS
    no_of_steps = 10000

    dict_aoi = {}
    dict_aoi["mu_d"] = {}
    dict_aoi["mu_d"]["lambda_d"] = {}
    dict_aoi["mu_d"]["lambda_d"]["mu_u"] = "lambda_u"
    dict_aoi["pmf"] = {}
    dict_aoi["avg_aol"] = {}
    for mu_u in mu_uu:
        print("mu_u = "+str(mu_u))
        if mu_u == 1.0:
            break
        dict_aoi["pmf"][mu_u] = {}
        dict_aoi["avg_aol"][mu_u] = {}
        for lambda_u in lambda_uu:
            if lambda_u >= mu_u and mu_u != 1.0:
                break        
            print("lambda_u="+str(lambda_u))            
            dict_aoi["pmf"][mu_u][lambda_u] = {}
            dict_aoi["avg_aol"][mu_u][lambda_u] = {}
            for mu_d in mu_dd:
                print("mu_d = "+str(mu_d))
                if mu_d == 1.0:
                    break
                dict_aoi["pmf"][mu_u][lambda_u][mu_d] = {}
                dict_aoi["avg_aol"][mu_u][lambda_u][mu_d] = {}
                for lambda_d in lambda_dd:
                    if lambda_d >= mu_d and mu_d != 1.0:
                        break        
                    print("lambda_d="+str(lambda_d))            
                    dict_aoi["pmf"][mu_u][lambda_u][mu_d][lambda_d] = {}
            
                    avg_aol = 0
                    #dict_aoi["pmf"][mu_u][lambda_u]["aoi"] = {}
                    for delta_u in range(no_of_steps):
                        #print("delta_u="+str(delta_u))
                        pmf_of_aoi_u = compute_pmf_of_aoi(lambda_u, mu_u, delta_u)
                        if pmf_of_aoi_u <= 1e-8:
                                break
                        for delta_d in range(no_of_steps):                           
                            #print("delta_d="+str(delta_d))
                            pmf_of_aoi_d = compute_pmf_of_aoi(lambda_d, mu_d, delta_d)
                            if pmf_of_aoi_d <= 1e-8:
                                break
                            if pmf_of_aoi_u*pmf_of_aoi_d <= 1e-8:
                                break
                            dict_aoi["pmf"][mu_u][lambda_u][mu_d][lambda_d][delta_u+delta_d] = dict_aoi["pmf"][mu_u][lambda_u][mu_d][lambda_d].get(delta_u+delta_d,0)+ pmf_of_aoi_u*pmf_of_aoi_d
                            #print(pmf_of_aoi_u,pmf_of_aoi_d,pmf_of_aoi_u*pmf_of_aoi_d,dict_aoi["pmf"][mu_u][lambda_u][mu_d][lambda_d][delta_u+delta_d])
                    for key in dict_aoi["pmf"][mu_u][lambda_u][mu_d][lambda_d]:
                        avg_aol = avg_aol + key * dict_aoi["pmf"][mu_u][lambda_u][mu_d][lambda_d][key]
                    dict_aoi["avg_aol"][mu_u][lambda_u][mu_d][lambda_d] = avg_aol
                    #print(pd.DataFrame(dict_aoi["pmf"][mu_u][lambda_u]))
                    print(mu_u, ' ', lambda_u, ' ', mu_d, ' ', lambda_d, ' ',avg_aol)
    #print(pd.DataFrame(dict_aoi["pmf"]))

    del dict_aoi["pmf"] # to make data less than 100 MB
    
    file_name="sim/sim3_data4.json"    
    with open(file_name, 'w') as file:
        json.dump(dict_aoi, file, ensure_ascii=False)

dump_aoi_ana_info_to_file()
