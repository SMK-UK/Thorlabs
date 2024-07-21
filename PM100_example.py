"""
Example script for controlling a Thorlabs PM100 power meter

Author: Sean Keenan
GitHub: SMK-UK
Date: 13/02/2024

"""

# import the relevant class
from PM100 import PM100

# initialise the device
PM = PM100()
# user enter device ID or leave blank for search
PM.initialise(device='enter deivce ID here')
# set units for device
PM.set_units('mW')
# change the bandwidth of the device
PM.set_bandwidth('high')
# set device to auto range
PM.auto_range(state=True)
# take a power reading for a give wavelength
PM.set_wavelength(606)
single_read = PM.measure(type='single', sample_rate=5)
# take an average reading at same wavelength
average_read = PM.measure(type='average', sample_rate=5, n_averages=100)
# close device when finished
PM.close()