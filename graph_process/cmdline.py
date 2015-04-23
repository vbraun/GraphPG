

import sys

from graph_process.recorder import Recorder


def run():
    rec = Recorder(sys.argv[1:])
    rec.run()
    print(rec)
    rec.plot()
