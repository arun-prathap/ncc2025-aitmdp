'''
Module Description

Classes:
    Queue:Class Description
'''

class Queue:
    '''
    Class Description

    Attributes:
        Class Attributes

    Methods:
        Class Methods

    '''

    def __init__(self, queue_max_size, fifo):
        '''
        Constructor.

        Parameters


        Raises



        Returns

        None.

        '''
        self.top = 0 #queue - fifo
        if not fifo:#stack - lifo
            self.top = -1
        self.queue_max_size = queue_max_size
        #As of Python version 3.7, dictionaries are ordered.
        #In Python 3.6 and earlier, dictionaries are unordered.
        self.data_dict = dict({})

    def enqueue(self, time, data):
        '''
        Method.

        Parameters



        Raises



        Returns

        None.

        '''
        if len(self.data_dict) < self.queue_max_size:
            if any(self.data_dict):
                if time <= max(self.data_dict.keys()):
                    raise ValueError("time index should be strict monotonic")
            self.data_dict[time] = data
        else:
            if self.top==0:
                raise ValueError("queue is full")
            else:
                time1 = list(self.data_dict.keys())[0]
                data1 = self.data_dict.pop(time1)
                self.data_dict[time] = data 

    def is_empty(self):
        '''
        Method.

        Parameters



        Raises



        Returns

        None.

        '''
        return len(self.data_dict) == 0

    def dequeue(self):
        '''
        Method.

        Parameters



        Raises



        Returns

        None.

        '''
        if not self.is_empty():
            time = list(self.data_dict.keys())[self.top]
            #data = self.data_dict[time]
            data = self.data_dict.pop(time)
            return time, data
        raise ValueError("queue is empty")

    def printqueue(self):
        '''
        Method.

        Parameters



        Raises



        Returns

        None.

        '''
        print(self.data_dict)
