'''
Module Description

Classes:
    MDPPlantModel:Class Description
'''
import numpy as np

class MDPPlantModel:
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
        self.params['A'] = R.shape[1]
        self.params['S'] = P.shape[0]
        self.params['P'] = P
        self.params['R'] = R
        self.params['horizon'] = horizon
        # to add sanity check for dimensions here or downstream
        self.state = np.zeros(horizon, dtype=int)
        self.action = np.zeros(horizon, dtype=int)
        self.action_times = np.zeros(horizon, dtype=int)
        self.time_step = 0
        self.action_init = False
        self.params['J'] = np.zeros(horizon)

    def get_control(self, action, time=None):
        '''
        Method.

        Parameters



        Raises



        Returns

        None.

        '''
        #print(action)
        if action is not None:
            if not self.action_init:
                self.action_init = True
            if self.time_step < (self.params['horizon']):
                self.action[self.time_step] = action
            if time is not None:
                self.action_times[self.time_step] = time
        else:
            if self.time_step > 0 and self.time_step < (self.params['horizon']):
                #if self.action_init:
                self.action[self.time_step] = self.action[self.time_step - 1]
                self.action_times[self.time_step] = self.action_times[self.time_step - 1]
            else:
                self.action[self.time_step] = np.random.choice(self.params['A'])

    def step(self):
        '''
        Method.

        Parameters



        Raises



        Returns

        None.

        '''
        self.time_step += 1
        if self.time_step < self.params['horizon']:
            self.state[self.time_step] =\
                np.random.choice(self.params['S'], p=self.params['P'][self.state[self.time_step-1]])

    def give_observation(self):
        '''
        Method.

        Parameters



        Raises



        Returns

        None.

        '''
        return self.time_step, self.state[self.time_step]

    def compute_cost(self):
        '''
        Method.

        Parameters



        Raises



        Returns

        None.

        '''
        self.params['J'] = np.zeros(self.params['horizon'])
        self.params['J'][0] = self.params['R'][self.state[0], self.action[0]]
        for i in range(1, self.params['horizon']):
            self.params['J'][i] = self.params['J'][i-1] \
                                    + self.params['R'][self.state[i], self.action[i]]
        return self.params['J']

    def dump_json(self):
        '''
        Method.

        Parameters



        Raises



        Returns

        None.

        '''
        temp_dict = {}
        temp_dict['State'] = self.state.tolist()
        temp_dict['Action'] = self.action.tolist()
        temp_dict['Action_times'] = self.action_times.tolist()
        temp_dict['Cost'] = self.params['J'].tolist()
        return temp_dict
