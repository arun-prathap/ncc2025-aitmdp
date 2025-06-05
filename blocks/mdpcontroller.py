'''
Module Description

Classes:
    MDPController:Class Description
'''

import numpy as np

class MDPController:
    '''
    Class Description

    Attributes:
        Class Attributes

    Methods:
        Class Methods

    '''

    def __init__(self, horizon, P, R):
        '''
        Constructor.

        Parameters


        Raises



        Returns

        None.

        '''
        self.params = {}
        self.params["horizon"] = horizon
        #self.NoOfActions = A
        #self.NoOfStates = S
        self.params["transition_prob_matrix"] = P
        self.params["reward_matrix"] = R
        # sanity check for dimensions
        self.observations = {}
        self.observation_times = []
        self.aoi={}
        self.state_estimate = np.zeros(horizon, dtype=int)
        self.action = np.zeros(horizon, dtype=int)

        self.time_step = 0

        self.observed = False

    def get_observation(self, time, state):
        '''
        Method.

        Parameters



        Raises



        Returns

        None.

        '''
        if not self.observed:
            self.observed = True
        self.observations[time] = state
        #print(type(time),type(state))
        self.observation_times.append(self.time_step)
        #print(self.observations)

    def step(self):
        '''
        Method.

        Parameters



        Raises



        Returns

        None.

        '''
        
        self.time_step += 1

    def give_control(self):
        '''
        Method.

        Parameters



        Raises



        Returns

        None.

        '''
        if not self.observed:
            index = self.time_step
            self.aoi[index] = self.aoi.get(index, 0) + 1
            #print("index",str(index))
        if self.observed and self.time_step <= self.params["horizon"]:#argmax
            last_observation_time = list(self.observations.keys())[-1]
            index = self.time_step - last_observation_time
            self.aoi[index] = self.aoi.get(index, 0) + 1
            #print("index",str(index))
            tpm_now = np.linalg.matrix_power(self.params["transition_prob_matrix"], \
                                                  self.time_step - last_observation_time)            
            self.state_estimate[self.time_step] = \
                np.argmax(tpm_now[self.observations[last_observation_time], :])
            self.action[self.time_step] =\
                np.argmax(self.params["reward_matrix"][self.state_estimate[self.time_step], :])
            return self.time_step, self.action[self.time_step]
        return None

    def dump_json(self):
        '''
        Method.

        Parameters



        Raises



        Returns

        None.

        '''
        temp_dict = {}
        temp_dict['State_Estimate'] = self.state_estimate.tolist()
        temp_dict['Action'] = self.action.tolist()
        temp_dict['Observations'] = self.observations
        temp_dict['Observation_dest_times'] = self.observation_times
        temp_dict['aoi'] = self.aoi
        return temp_dict
