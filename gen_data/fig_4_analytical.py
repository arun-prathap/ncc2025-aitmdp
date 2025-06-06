'''
Module Description

Classes:
    None
'''

import numpy as np
import pandas as pd
import json
import random

from utils.util import create_matrix_from_eig_value

SEED = 123
random.seed(SEED)
np.random.seed(SEED)
np.random.default_rng(SEED)

SECOND_EIG_VALUE_OF_TPM = 0.85

S = 6
A = 3

P = create_matrix_from_eig_value(S, SECOND_EIG_VALUE_OF_TPM) 
print(P)
eig_val, eig_vec = np.linalg.eig(P.T)
STATIONARY_STATE_DIST = np.array(eig_vec[:, np.where(np.abs(eig_val - 1.) < 1e-8)[0][0]].flat)
STATIONARY_STATE_DIST = STATIONARY_STATE_DIST / np.sum(STATIONARY_STATE_DIST)
STATIONARY_STATE_DIST = STATIONARY_STATE_DIST.real
print(STATIONARY_STATE_DIST)
P = np.array([P])
STATIONARY_STATE_DIST = np.array([STATIONARY_STATE_DIST])

R = np.array([
    [50, 0, 0],
    [0, 0, 50],
    [0, 50, 0],
    [0, 50, 0],
    [0, 0, 50],
    [50, 0, 0]])

if R.shape[0] != S or R.shape[1] != A:
    raise ValueError("R shape should be SxA")

LAMBDA_UU = np.round(np.arange(0.05,1,0.05), 2)

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

no_of_steps = 1000

astar = np.argmax(R, axis=1)
print(astar)

dict_rewards = {}
dict_rewards["mu_d"] = {"lambda_d":{"mu_u":"lambda_u"}}
dict_rewards["rewards"] = {}

def find_analytical(mu_dd,lambda_dd,mu_uu,lambda_uu):
    for mu_d in mu_dd:
        if mu_d == 1.0:
            break
        print("mu_d = "+str(mu_d))
        if mu_d not in dict_rewards["rewards"]:
            dict_rewards["rewards"][mu_d] = {}
        for lambda_d in lambda_dd:
            if lambda_d >= mu_d and mu_d != 1.0:
                break
            print("lambda_d = "+str(lambda_d))
            if lambda_d not in dict_rewards["rewards"][mu_d]:
                dict_rewards["rewards"][mu_d][lambda_d] = {}
            for mu_u in mu_uu:
                if mu_u == 1.0:
                    break
                if (mu_u+mu_d) > 1:
                    break
                print("mu_u = "+str(mu_u))
                if mu_u not in dict_rewards["rewards"][mu_d][lambda_d]:
                    dict_rewards["rewards"][mu_d][lambda_d][mu_u] = {}        
                for lambda_u in lambda_uu:
                    if lambda_u >= mu_u and mu_u != 1.0:
                        break
                    print("lambda_u = "+str(lambda_u))
                    avg_reward = 0
                    #P_temp = np.eye(6)#P[0]#
                    #P_temp = P                
                    for delta_u in range(no_of_steps):                    
                        #lambda_u_temp = compute_pmf_of_aoi(lambda_u, mu_u, delta_u)
                        #if lambda_u_temp <= 1e-8:
                        #    break
                        #P_temp1 = P_temp
                        #P_temp1 = np.eye(6)                    
                        for delta_d in range(no_of_steps):
                            if delta_u==0 and delta_d==0:
                                continue
                            pmf_temp = analytical_prob(delta_u,delta_d,lambda_u,lambda_d,mu_u,mu_d)                        
                            if pmf_temp <= 1e-8:
                                break
                            P_temp1 = np.linalg.matrix_power(P[0], delta_u + delta_d)
                            P_temp = np.linalg.matrix_power(P[0], delta_u)
                            s_ML = np.argmax(P_temp, axis=-1)
                            temp = 0
                            for index,state in enumerate(s_ML):
                                temp += (STATIONARY_STATE_DIST[0]@P_temp[:,state])*(P_temp1[index,:]@R.T[astar[state],:])
                                ## here (STATIONARY_STATE_DIST@P_temp[:,state]) = STATIONARY_STATE_DIST[index] may not be true for a general stochastic matrix
                            avg_reward += pmf_temp*temp
                            #print(temp)  
                            #P_temp1 = P_temp1@P[0]
                        #P_temp = P_temp@P[0]
                    dict_rewards["rewards"][mu_d][lambda_d][mu_u][lambda_u] = avg_reward


find_analytical([0.45],[0.35],[0.45],LAMBDA_UU)
find_analytical([0.45],[0.4],[0.5],LAMBDA_UU)
find_analytical([0.55],[0.4],[0.45],LAMBDA_UU)

print(pd.DataFrame(dict_rewards["rewards"]))

file_name="sim/sim10_data3_085.json"    
with open(file_name, 'w') as file:
    json.dump(dict_rewards, file, ensure_ascii=False)
