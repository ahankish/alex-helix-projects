import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#import pyRAPL

### https://pyrapl.readthedocs.io/en/latest/  -> pyRAPL documentation

# for cpu socket 1
#pyRAPL.setup(devices=[pyRAPL.Device.PKG], socket_ids=[1])

    #@pyRAPL.measureit
	#def foo():
		# Instructions to be evaluated.

	#foo() # function that measures xyz

# output file with filename 
filename = 'result' + '.csv' # add identifier for which test

csv_output = pyRAPL.outputs.CSVOutput(filename)

# for all available devices on the cpu
pyRAPL.setup()

@pyRAPL.measureit
def add_stress():
    # use stress_ng to stress the cpu and measure

add_stress() # function that measures xyz

# save output 
csv_output.save()
