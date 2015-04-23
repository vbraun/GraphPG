# -*- coding: utf-8 -*-
"""
Plot Resource Usage Over Time
"""

import os
import math
import tempfile
import matplotlib
import subprocess
import matplotlib.pyplot as plt


class Graphics(object):

    def __init__(self):
        self.fig, self.cpu = plt.subplots()
        self.cpu.set_xlabel('wall time (s)')
        self.cpu.set_ylabel('CPU (%)', color='red')
        # self.cpu.set_ybound(lower=0.0)
        for tl in self.cpu.get_yticklabels():
            tl.set_color('red')
        self.rss = self.cpu.twinx()
        self.rss.set_ylabel('RSS (MB)', color='blue')
        for tl in self.rss.get_yticklabels():
            tl.set_color('blue')
        #self.rss.set_ybound(lower=0.0)
        #self.rss.set_ylim(bottom=0.0)
        
    def plot_cpu(self, x, y, color='red'):
        self.cpu.fill_between(x, y, color=color, alpha=0.3)
        self.cpu.plot(x, y, color=color)
        max_cpu = max(y)
        max_cpu = max(100.0, 100.0 * math.ceil(max_cpu / 100.0))
        self.cpu.set_ylim([0.0, max_cpu])

    def plot_rss(self, x, y, color='blue'):
        mb = map(lambda b:b/1e6, y)
        self.rss.fill_between(x, mb, color=color, alpha=0.3)
        self.rss.plot(x, mb, color=color)
        self.rss.set_ylim([0.0, max(mb)])

    def show(self):
        plt.grid(True)
        if matplotlib.get_backend() in matplotlib.rcsetup.interactive_bk:
            plt.show()
        else:
            self.open_viewer()

    def open_viewer(self):
        with tempfile.NamedTemporaryFile(suffix='.svg', delete=False) as tmpfile:
            plt.savefig(tmpfile, format='svg')
        subprocess.check_call(['xdg-open', tmpfile.name])

