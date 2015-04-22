# -*- coding: utf-8 -*-
"""
Timer for Elapsed Seconds


This module defines ``walltime`` which counts elapsed seconds since
the program was started.
"""

import time


class Timer(object):

    def __init__(self):
        """
        Timer

        This object counts elapsed time since it has been
        instantiated.
        """
        self.start = time.time()

    def time(self):
        """
        Return the current timer value

        Returns:
            float: The elapsed seconds since the timer was instantiated.
        """
        return time.time() - self.start


walltime = Timer()
