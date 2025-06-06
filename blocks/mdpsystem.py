'''
Module Description

Classes:
    MDPSystem:Class Description
'''
import json

from blocks.mdpplantmodel import MDPPlantModel
from blocks.mdpcontroller import MDPController
from blocks.linkwithqueue import LinkWithQueue
from utils.util import json_serialize

        
class MDPSystem:
    '''
    Class Description

    Attributes:
        Class Attributes

    Methods:
        Class Methods

    '''

    def __init__(self, horizon, P, R, queue_uplink_dict, queue_downlink_dict):
        '''
        Constructor.

        Parameters


        Raises



        Returns

        None.

        '''
        #consistency check S,A wrt size of P,R
        self.horizon = horizon
        self.model = MDPPlantModel(horizon, P, R)
        self.controller = MDPController(horizon, P, R)
        self.uplink_queue = LinkWithQueue(queue_uplink_dict['queue_max_size'], \
                                          queue_uplink_dict['admission_prob'], \
                                          queue_uplink_dict['service_prob'], \
                                          queue_uplink_dict['fifo'])
        self.downlink_queue = LinkWithQueue(queue_downlink_dict['queue_max_size'], \
                                            queue_downlink_dict['admission_prob'], \
                                            queue_downlink_dict['service_prob'], \
                                            queue_downlink_dict['fifo'])
        self.time_step = 0
        self.data = {}
        self.data['simulationParams'] = {}
        self.data['simulationParams']['horizon'] = horizon
        self.data['simulationParams']['A'] = R.shape[1]
        self.data['simulationParams']['S'] = P.shape[0]
        self.data['simulationParams']['P'] = P.tolist()
        self.data['simulationParams']['R'] = R.tolist()
        self.data['simulationParams']['queue_uplink_dict'] = queue_uplink_dict
        self.data['simulationParams']['queue_downlink_dict'] = queue_downlink_dict

    def set_initial_state(self, state):
        '''
        Method.

        Parameters



        Raises



        Returns

        None.

        '''
        self.model.state[0] = state

    def step(self):
        '''
        Method.

        Parameters



        Raises



        Returns

        None.

        '''
        #print("time ",str(self.time_step))
        if self.time_step < self.horizon:
            time, state = self.model.give_observation()
            #print(time,state)
            try:#uplink queue
                self.uplink_queue.process_arrival(time, state)                
            except Exception as _:
                pass
            try:    
                time, state = self.uplink_queue.service_queue()
                #print(time,state)
                #print(time,state)
                self.controller.get_observation(time, state)
            except Exception as _:
                pass

            
            try:#downlink queue
                time, action = self.controller.give_control()  
                #print(time,action)              
                self.downlink_queue.process_arrival(time, action)
            except Exception as _:
                pass
            action = None
            time = None
            try:
                time, action = self.downlink_queue.service_queue()
                #print(time,state,action)
            except Exception as _:
                action = None
                time = None
            self.model.get_control(action, time)
            self.model.step()
            self.controller.step()
            self.time_step += 1

    def evolve(self):
        '''
        Method.

        Parameters



        Raises



        Returns

        None.

        '''
        start_step = self.time_step
        for _ in range(start_step, self.horizon):
            self.step()
        self.model.compute_cost()

    def dump_json(self, file_name):
        '''
        Method.

        Parameters



        Raises



        Returns

        None.

        '''
        self.data['Model'] = self.model.dump_json()
        self.data['Controller'] = self.controller.dump_json()
        #print(self.data)
        with open(file_name, 'w') as file:
            json.dump(self.data, file, ensure_ascii=False, cls=json_serialize)
