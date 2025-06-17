'''
Module Description

Classes:
    None
'''

import json
import os

import numpy as np
import pandas as pd

from blocks.mdpsystem_mod import MDPSystemMod

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

MU_DD = np.array([0.55])
LAMBDA_DD = np.array([0.4])
MU_UU = np.array([0.3,0.45])
LAMBDA_UU = np.round(np.arange(0.05,1,0.05), 2)

NO_OF_SIMULATIONS = 1000
NO_OF_STEPS = 10000

def simulate_and_write_data_to_folders():
    for mu_d in MU_DD:
        if mu_d == 1.0:
            break
        print("mu_d = "+str(mu_d))
        for mu_u in MU_UU:
            if mu_u == 1.0:
                break
            if (mu_u+mu_d) > 1:
                break
            print("mu_u = "+str(mu_u))
            for lambda_d in LAMBDA_DD:
                if lambda_d >= mu_d and mu_d != 1.0:
                    break
                print("lambda_d = "+str(lambda_d))
                for lambda_u in LAMBDA_UU:
                    if lambda_u >= mu_u and mu_u != 1.0:
                        break
                    print("lambda_u = "+str(lambda_u))
                    #for mu_mdp in MU_MDP:
                    mu_mdp = np.round(max(0.0,1-mu_u-mu_d),2)
                    if not os.path.isdir('sim/sim8/'+str(mu_d)+'_'+str(lambda_d)+'_'+str(mu_u)+'_'+str(lambda_u)):
                        os.mkdir('sim/sim8/'+str(mu_d)+'_'+str(lambda_d)+'_'+str(mu_u)+'_'+str(lambda_u))
                    queue_dict_u = {'queue_max_size':NO_OF_STEPS+1, 'admission_prob':lambda_u,\
		                          'service_prob':1.0, 'fifo':True}
                    queue_dict_d = {'queue_max_size':NO_OF_STEPS+1, 'admission_prob':lambda_d,\
		                          'service_prob':1.0, 'fifo':True}
                    for i in range(NO_OF_SIMULATIONS):
                        INIT_STATE = np.random.choice(S, p=STATIONARY_STATE_DIST[0])
                        system = MDPSystemMod(NO_OF_STEPS, P[0], R, queue_dict_u, queue_dict_d, [mu_mdp,mu_u,mu_d])
                        system.set_initial_state(INIT_STATE)
                        system.evolve()
                        system.dump_json('sim/sim8/'+str(mu_d)+'_'+str(lambda_d)+\
                                '_'+str(mu_u)+'_'+str(lambda_u)+'/test_'+str(i)+'.json')

def compile_data_from_folders():
    data1 = {}
    data1["mu_d"] = {"lambda_d":{"mu_u":{"lambda_u":"mu_mdp"}}}
    data1["mean"] = {}
    data1["std"] = {}
    #data1["cost"] = {}
    for mu_d in MU_DD:
        #if mu_d == 1.0:
            #break
        data1["mean"][mu_d] = {}
        data1["std"][mu_d] = {}
        for lambda_d in LAMBDA_DD:
            if lambda_d >= mu_d and mu_d != 1.0:
                break
            data1["mean"][mu_d][lambda_d] = {}
            data1["std"][mu_d][lambda_d] = {}
            #data1["cost"][lambda_d] = {}
            for mu_u in MU_UU:            
                #if mu_u == 1.0:
                    #break
                if (mu_u+mu_d) > 1:
                    break
                data1["mean"][mu_d][lambda_d][mu_u] = {}
                data1["std"][mu_d][lambda_d][mu_u] = {}
                for lambda_u in LAMBDA_UU:
                    if lambda_u >= mu_u and mu_u != 1.0:
                        break
                    #data1["mean"][mu_d][lambda_d][mu_u][lambda_u] = {}
                    #data1["std"][mu_d][lambda_d][mu_u][lambda_u] = {}
                    mu_mdp = max(0.0,1-mu_u-mu_d)
                    #for mu_mdp in MU_MDP:                        
                    cost1 = []
                    for i in range(NO_OF_SIMULATIONS):
                        with open('sim/sim8/'+str(mu_d)+'_'+str(lambda_d)+'_'+str(mu_u)+'_'+str(lambda_u)+\
                                      '/test_'+str(i)+'.json') as f:
                            data = json.load(f)
                            cost1.append(data['Model']['Cost'][-1])
                    #data1["cost"][lambda_d][lambda_u] = cost1
                    data1["mean"][mu_d][lambda_d][mu_u][lambda_u] = \
                                                  np.array(cost1).mean()/NO_OF_STEPS
                    data1["std"][mu_d][lambda_d][mu_u][lambda_u] = \
                                                  np.array(cost1).std()/NO_OF_STEPS
    file_name = "sim/sim8_data_055_10000x1000.json"
    with open(file_name, 'w') as file:
        json.dump(data1, file, ensure_ascii=False)
    print(pd.DataFrame(data1["mean"]))

if not os.path.isdir("sim/sim8"):
    os.mkdir("sim/sim8")
    
### Uncomment as required
simulate_and_write_data_to_folders()

### Uncomment as required
compile_data_from_folders()
