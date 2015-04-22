# -*- coding: utf-8 -*-
"""
Execute Command and Record Resource Usage over Time
"""

import os
import time
import subprocess

from graph_process.sample import ProcessSample


class Recorder(object):

    def __init__(self, argv, resolution=1.0):
        """
        Process data recorder
        
        This class records process information during the execution of
        a command.

        Args:
            argv (list of sting): The command to execute.
            resolution (float): delay between samples in seconds

        Examples:

            >>> rec = Recorder(['sleep', '1'], resolution=0.1)
            >>> rec.run()
            >>> rec.samples[0].processes
            ['sleep 1']
            >>> last = rec.samples[-1]
            >>> last.time > 1.0
            True
        """
        self.argv = argv
        self.samples = []
        self.resolution = resolution

    def __repr__(self):
        result = []
        for x in self.samples:
            result.append(str(x))
        return '\n'.join(result)
        
    def run(self):
        """
        Perform the data collection run.

        This method is usually only called once during the recorder's
        lifetime, though you can call it multiple times (results are
        appended).
        """
        proc = subprocess.Popen(self.argv)
        pgid = os.getpgid(proc.pid)
        while True:
            proc.poll()
            if proc.returncode is not None:
                return
            time.sleep(self.resolution)
            s = ProcessSample(pgid)
            s.collect_data()
            # print('\n---- collected {0}'.format(s))
            self.samples.append(s)
            
    def cpu(self):
        """
        Return the CPU samples
        """
        return [s.cpu for s in self.samples]

    def rss(self):
        """
        Return the RSS samples
        """
        return [s.rss for s in self.samples]

    def nproc(self):
        """
        Return the number of processes
        """
        return [len(s.processes) for s in self.samples]
    
    def plot(self):
        timestamps = [s.time for s in self.samples]
        from graph_process.plot import Graphics
        g = Graphics()
        g.plot_cpu(timestamps, self.cpu())
        g.plot_rss(timestamps, self.rss())
        g.show()
