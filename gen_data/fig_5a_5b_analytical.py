'''
Module Description

Classes:
    None
'''

import numpy as np
import pandas as pd
import os
import json

NO_OF_MDPS = 1

MU_DD = [0.45]
LAMBDA_DD = [0.05, 0.2, 0.3, 0.4]
MU_UU = [0.55]
LAMBDA_UU = np.round(np.arange(0.05,1,0.05),2)


pmf_of_aoi={}

def analytical_prob(au, ad, lu, ld, mu, md):
    lub = 1 - lu
    ldb = 1 - ld
    mub = 1 - mu
    mdb = 1 - md
    t0 = np.sum([mu * (mub**(g - 1)) * lu * (lub**(au - g)) for g in range(1, au + 1)])
    t1 = ld * (md * mdb**ad * t0)
    t3 = np.sum([mu * (mub**(g)) * lu * (lub**(au - g)) for g in range(0, au + 1)])
    t4 = 0
    if ad > 0:
        t4 = np.sum([md * (mdb**(ad - g)) * ld * (ldb**(g)) for g in range(1, ad + 1)])
    return t1 + t3*t4

def compute_analytical_rewards(P, R,STATIONARY_STATE_DIST, file_name):
    lambda_dd = LAMBDA_DD
    #lambda_dd=[0.001,0.05,1.0]## TEST
    lambda_uu = LAMBDA_UU
    mu_dd = MU_DD
    mu_uu = MU_UU

    #no_of_steps = NO_OF_STEPS
    no_of_steps = 1000

    astar = np.argmax(R, axis=1)
    print(astar)

    dict_rewards = {}
    dict_rewards["MDP"] = {"mu_d":{"lambda_d":{"mu_u":"lambda_u"}}}
    for i in range(NO_OF_MDPS):
        if i != 0:
            continue
        print(P[i])
        print(STATIONARY_STATE_DIST[i])
        dict_rewards[i] = {}
        dict_rewards[i]["P"] = P[i].tolist()
        dict_rewards[i]["rewards"] = {}
        dict_rewards[i]["state_err"] = {}
        for mu_d in mu_dd:
            if mu_d == 1.0:
                break
            print("mu_d = "+str(mu_d))
            dict_rewards[i]["rewards"][mu_d] = {}
            dict_rewards[i]["state_err"][mu_d] = {}
            for lambda_d in lambda_dd:
                if lambda_d >= mu_d and mu_d != 1.0:
                    break
                print("lambda_d = "+str(lambda_d))
                dict_rewards[i]["rewards"][mu_d][lambda_d] = {}
                dict_rewards[i]["state_err"][mu_d][lambda_d] = {}
                for mu_u in mu_uu:
                    if mu_u == 1.0:
                        break
                    print("mu_u = "+str(mu_u))
                    dict_rewards[i]["rewards"][mu_d][lambda_d][mu_u] = {}
                    dict_rewards[i]["state_err"][mu_d][lambda_d][mu_u] = {}                
                    for lambda_u in lambda_uu:
                        if lambda_u >= mu_u and mu_u != 1.0:
                            break
                        print("lambda_u = "+str(lambda_u))
                        avg_reward = 0
                        state_err = 0
                        #P_temp = np.eye(6)
                        #P_temp = P                
                        for delta_u in range(no_of_steps):
                            #lambda_u_temp = compute_pmf_of_aoi(lambda_u, mu_u, delta_u)
                            #if lambda_u_temp <= 1e-8:
                                #break
                            #P_temp1 = P_temp
                            #P_temp1 = np.eye(6)                    
                            for delta_d in range(no_of_steps):
                                #lambda_d_temp = compute_pmf_of_aoi(lambda_d, mu_d, delta_d)
                                #if lambda_d_temp*lambda_u_temp <= 1e-8:
                                    #break
                                if delta_u==0 and delta_d==0:
                                    continue
                                pmf_temp = analytical_prob(delta_u,delta_d,lambda_u,lambda_d,mu_u,mu_d)                        
                                if pmf_temp <= 1e-8:
                                    break
                                P_temp1 = np.linalg.matrix_power(P[i], delta_u + delta_d)
                                P_temp = np.linalg.matrix_power(P[i], delta_u)
                                s_ML = np.argmax(P_temp, axis=-1)
                                #if delta_u<10 and delta_d<10:
                                    #print(delta_u,delta_d,s_ML)
                                    #print(P_temp)
                                    #print(P_temp1)
                                temp = 0
                                temp_state_err = 0
                                for index,state in enumerate(s_ML):
                                    #temp += (STATIONARY_STATE_DIST@P_temp[:,state])*(P_temp1[index,:]@R.T[astar[state],:])
                                    ## here (STATIONARY_STATE_DIST@P_temp[:,state]) = STATIONARY_STATE_DIST[index] may not be true for a general stochastic matrix
                                    temp += STATIONARY_STATE_DIST[i][index]*(P_temp1[index,:]@R.T[astar[state],:])
                                    temp_state_err += STATIONARY_STATE_DIST[i][index]*P_temp1[index,state]
                                avg_reward += pmf_temp*temp 
                                state_err +=  pmf_temp*temp_state_err   
                                #P_temp1 = P_temp1@P
                            #P_temp = P_temp@P
                        dict_rewards[i]["rewards"][mu_d][lambda_d][mu_u][lambda_u] = avg_reward
                        dict_rewards[i]["state_err"][mu_d][lambda_d][mu_u][lambda_u] = 1 - state_err

        print(pd.DataFrame(dict_rewards[i]["rewards"]))

    #file_name=SIM_NAME+"_data3.json"    
    #file_name=SIM_NAME+"_data4_055_s_s6_tpm1.json"    
    with open(file_name, 'w') as file:
        json.dump(dict_rewards, file, ensure_ascii=False)

R = np.array([
    [50, 0],
    [0, 50]])

## UNCOMMENT AS REQUIRED
P = np.array([[0.1,0.9],[0.9,0.1]])
#print(P)
eig_val, eig_vec = np.linalg.eig(P.T)
STATIONARY_STATE_DIST = np.array(eig_vec[:, np.where(np.abs(eig_val - 1.) < 1e-8)[0][0]].flat)
STATIONARY_STATE_DIST = STATIONARY_STATE_DIST / np.sum(STATIONARY_STATE_DIST)
STATIONARY_STATE_DIST = STATIONARY_STATE_DIST.real
#print(STATIONARY_STATE_DIST)
P = np.array([P])
STATIONARY_STATE_DIST = np.array([STATIONARY_STATE_DIST])

compute_analytical_rewards(P, R, STATIONARY_STATE_DIST, 'sim/sim12_data4_EX1_LCFS.json')

## UNCOMMENT AS REQUIRED
P = np.array([[0.1,0.9],[0.8,0.2]])
print(P)
eig_val, eig_vec = np.linalg.eig(P.T)
STATIONARY_STATE_DIST = np.array(eig_vec[:, np.where(np.abs(eig_val - 1.) < 1e-8)[0][0]].flat)
STATIONARY_STATE_DIST = STATIONARY_STATE_DIST / np.sum(STATIONARY_STATE_DIST)
STATIONARY_STATE_DIST = STATIONARY_STATE_DIST.real
print(STATIONARY_STATE_DIST)
P = np.array([P])
STATIONARY_STATE_DIST = np.array([STATIONARY_STATE_DIST])

compute_analytical_rewards(P, R, STATIONARY_STATE_DIST, 'sim/sim12_data4_EX2_LCFS.json')
