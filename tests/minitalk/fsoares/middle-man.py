#!/usr/bin/env python
import signal
import sys

def handler(signum, frame):
    print('Signal handler called with signal', signum)
    raise OSError("Couldn't open device!")

for i in [x for x in dir(signal) if x.startswith("SIG")]:
  try:
    signum = getattr(signal,i)
    signal.signal(signum, handler)
  except (OSError, RuntimeError) as m:
    print ("Skipping {}".format(i))