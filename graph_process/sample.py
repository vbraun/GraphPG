# -*- coding: utf-8 -*-
"""
Sample Metadata for Process Group
"""

import os
import psutil
from graph_process.timer import walltime


class ProcessSample(object):

    def __init__(self, pgid):
        """
        Sampled process metadata

        Typically you run :meth:`collect_data` exactly once for a
        process sample object.

        Args:
            pgid (int): The process group id (NOT: pid) to account for.
        """
        self.pgid = pgid

    def pg_members(self):
        """
        Iterate over the members of the process group.
        """
        own_pid = os.getpid()
        for process in psutil.process_iter():
            if own_pid != process.pid and self.pgid == os.getpgid(process.pid):
                yield process
                
    def _accumulate_data(self, process):
        """
        Add process data to the sample

        Args:
            process (psutil.Process): the process whose metadata
            should be added to the sample.
        """
        self.rss += process.memory_info().rss
        self.cpu += process.cpu_percent()
        self.processes.append(' '.join(process.cmdline()))
                
    def collect_data(self):
        """
        Collect data for the process group.

        Data from all processes of the process group will be added up
        to get the resource usage of the process group.
        """
        self.time = walltime.time()
        self.rss = 0
        self.cpu = 0.0
        self.processes = []
        for process in self.pg_members():
            try:
                self._accumulate_data(process)
            except psutil.NoSuchProcess:
                pass

    def __str__(self):
        return '{0}s {1}% {2}bytes {3}'.format(
            self.time, self.cpu, self.rss, ', '.join(self.processes))
