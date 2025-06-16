'''
Module Description

Classes:
    None
'''
#the publication uses simulation data for this plot, if you want to replicate that use the code in fig_7a_sim_relaxed replacing the TPMs from this code.

import numpy as np
import pandas as pd
import os
import json

import random

import mdptoolbox.example

S = 6
A = 3
NO_OF_MDPS = 20

np.random.seed(0)
P, R_Rand = mdptoolbox.example.rand(S, NO_OF_MDPS)
STATIONARY_STATE_DIST = np.zeros((NO_OF_MDPS,S))
for i in range(NO_OF_MDPS):
    eig_val, eig_vec = np.linalg.eig(P[i].T)
    stationary = np.array(eig_vec[:, np.where(np.abs(eig_val - 1.) < 1e-8)[0][0]].flat)
    stationary = stationary / np.sum(stationary)
    stationary = stationary.real
    STATIONARY_STATE_DIST[i] = stationary
    print(stationary)

R = np.array([
    [50, 0, 0],
    [0, 0, 50],
    [0, 50, 0],
    [0, 50, 0],
    [0, 0, 50],
    [50, 0, 0]])

if R.shape[0] != S or R.shape[1] != A:
    raise ValueError("R shape should be SxA")

MU_DD = np.array([0.55])
LAMBDA_DD = np.array([0.4])
MU_UU = np.array([0.3,0.35,0.4,0.45])
LAMBDA_UU = np.round(np.arange(0.05,1,0.05), 2)

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

def compute_analytical_rewards():
    lambda_dd = LAMBDA_DD
    #lambda_dd=[0.001,0.05,1.0]## TEST
    lambda_uu = LAMBDA_UU
    mu_dd = MU_DD
    mu_uu = MU_UU

    #no_of_steps = NO_OF_STEPS
    no_of_steps = 100000

    astar = np.argmax(R, axis=1)
    print(astar)

    dict_rewards = {}
    dict_rewards["MDP"] = {"mu_d":{"lambda_d":{"mu_u":"lambda_u"}}}
    for i in range(NO_OF_MDPS):
        if i not in [1]:#[0]:
            continue
        print(P[i])
        print(STATIONARY_STATE_DIST[i])
        dict_rewards[i] = {}
        dict_rewards[i]["P"] = P[i].tolist()
        dict_rewards[i]["rewards"] = {}
        for mu_d in mu_dd:
            if mu_d == 1.0:
                break
            print("mu_d = "+str(mu_d))
            dict_rewards[i]["rewards"][mu_d] = {}
            for lambda_d in lambda_dd:
                if lambda_d >= mu_d and mu_d != 1.0:
                    break
                print("lambda_d = "+str(lambda_d))
                dict_rewards[i]["rewards"][mu_d][lambda_d] = {}
                for mu_u in mu_uu:
                    if mu_u == 1.0:
                        break
                    print("mu_u = "+str(mu_u))
                    dict_rewards[i]["rewards"][mu_d][lambda_d][mu_u] = {}
     
                    for lambda_u in lambda_uu:
                        if lambda_u >= mu_u and mu_u != 1.0:
                            break
                        print("lambda_u = "+str(lambda_u))
                        avg_reward = 0
                        #P_temp = np.eye(6)
                        #P_temp = P                
                        for delta_u in range(no_of_steps):
                            lambda_u_temp = compute_pmf_of_aoi(lambda_u, mu_u, delta_u)
                            if lambda_u_temp <= 1e-8:
                                break
                            #P_temp1 = P_temp
                            #P_temp1 = np.eye(6)                    
                            for delta_d in range(no_of_steps):
                                lambda_d_temp = compute_pmf_of_aoi(lambda_d, mu_d, delta_d)
                                if lambda_d_temp*lambda_u_temp <= 1e-8:
                                    break
                                P_temp1 = np.linalg.matrix_power(P[i], delta_u + delta_d)
                                P_temp = np.linalg.matrix_power(P[i], delta_u)
                                s_ML = np.argmax(P_temp, axis=-1)
                                #if delta_u<10 and delta_d<10:
                                    #print(delta_u,delta_d,s_ML)
                                    #print(P_temp)
                                    #print(P_temp1)
                                temp = 0
                                for index,state in enumerate(s_ML):
                                    #temp += (STATIONARY_STATE_DIST@P_temp[:,state])*(P_temp1[index,:]@R.T[astar[state],:])
                                    ## here (STATIONARY_STATE_DIST@P_temp[:,state]) = STATIONARY_STATE_DIST[index] may not be true for a general stochastic matrix
                                    temp += STATIONARY_STATE_DIST[i][index]*(P_temp1[index,:]@R.T[astar[state],:])
                                avg_reward += lambda_d_temp*lambda_u_temp*temp 
                                #P_temp1 = P_temp1@P
                            #P_temp = P_temp@P
                        dict_rewards[i]["rewards"][mu_d][lambda_d][mu_u][lambda_u] = avg_reward

        print(pd.DataFrame(dict_rewards[i]["rewards"]))

    
    file_name="sim/sim12_data_055_10000x100.json"    
    with open(file_name, 'w') as file:
        json.dump(dict_rewards, file, ensure_ascii=False)

## UNCOMMENT AS REQUIRED
compute_analytical_rewards()
