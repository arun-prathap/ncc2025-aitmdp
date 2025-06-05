'''
Module Description

Classes:
    LinkWithQueue:Class Description
'''
#import random
import numpy as np

from link.queue import Queue

class LinkWithQueue:
    '''
    Class Description

    Attributes:
        Class Attributes

    Methods:
        Class Methods

    '''

    def __init__(self, queue_max_size, admission_prob, service_prob, fifo):
        '''
        Constructor.

        Parameters


        Raises



        Returns

        None.

        '''
        self.queue = Queue(queue_max_size, fifo)
        if admission_prob < 0 or admission_prob > 1:
            raise ValueError("admission_prob should be in [0,1]")
        if service_prob < 0 or service_prob > 1:
            raise ValueError("service_prob should be in [0,1]")
        self.admission_prob = admission_prob
        self.service_prob = service_prob
        self.rng = np.random.default_rng()

    def process_arrival(self, time, data):
        '''
        Method.

        Parameters



        Raises



        Returns

        None.

        '''
        # distribution can be used
        #if random.random() <= self.admission_prob:
        if self.rng.binomial(1, self.admission_prob):
            try:
                #print("enqueue")
                self.queue.enqueue(time, data)
            except Exception as exception:
                raise exception
        else:
            raise ValueError("incoming packet dropped "+str(time)+" "+str(data))

    def service_queue(self):
        '''
        Method.

        Parameters



        Raises



        Returns

        None.

        '''
        # distribution can be used
        #if random.random() <= self.service_prob:
        if self.rng.binomial(1, self.service_prob):
            try:
                #print("dequeue")
                return self.queue.dequeue()
            except Exception as exception:
                raise exception
        else:
            raise ValueError("queue is not serviced")
