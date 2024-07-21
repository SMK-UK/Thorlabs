"""
Read and configure PM100 power meters from Thorlabs.

Author: Sean Keenan
GitHub: SMK-UK
Created: 11/02/2024

Based on
https://pypi.org/project/ThorlabsPM100/

# use ' pip install ThorlabsPM100 ' to install the libraries.

"""

import pyvisa as visa
from ThorlabsPM100 import ThorlabsPM100
from numpy import array
import time
import random
import sys

# setup the class
class PM100():

    def __init__(self, verbose=True):
        
        # find correct device if not specified
        self.rm = visa.ResourceManager()
        self.devices = self.rm.list_resources()
        # ensure default unit is Watts
        self.unit = 'W'
        # toggle print out
        self.verbose = verbose

    def close(self):
        '''
        Close the connection to the device
        '''
        try:
            self.inst.close()

            if self.verbose:
                print(f'Connection to device {self.device} ended')
        except Exception:
            print(f'No device connected!')

    def initialise(self, device=None):

        try:
            # check for available devices 
            if device is not None:
                self.device = device
            # select if only 1 device available
            elif len(self.devices) == 1:
                self.device = self.devices[0]
            # user select from list if more than one
            elif len(self.devices) > 1:
                print(f'Found the following devices: \n {self.devices}')
                time.sleep(0.2)
                self.device = input('Please enter the correct device from the list above')
            # cannot find device
            else:
                sys.exit('Could not find device')

            # set desired device to power_meter
            self.inst = self.rm.open_resource(self.device, timeout=2500)
            self.power_meter = ThorlabsPM100(inst=self.inst)

            if self.verbose:
                print(f'Connection to device {self.device} succesful!')
        
        except Exception as e:
            print(f'Connection to device unsuccesful {e}')

    def average(self):
        '''
        Take and averaged measurement

        <n_samples>:
            number of samples to average (default 100)
        <sample_rate>:
            sampling rate of the meter (samples per read)
        '''
        # set sample rate and then create array of sampled data
        data = array([self.power_meter.read/self.conversion for _ in range(self.n_averages)])

        if self.verbose:
            print(f"Average value : {round(data.mean(), 2)} {self.unit}")
            print(f"Standard Deviation : {round(data.std(), 2)} {self.unit}")

        return data
    
    def auto_range(self, state=True):
        '''
        Set the meter to auto-range ON / OFF

        <state>:
            Boolean - True == ON, False == OFF

        '''
        if state:
            self.power_meter.sense.power.dc.range.auto = 'ON'
            print('Auto-Range ON')
        else:
            self.power_meter.sense.power.dc.range.auto = 'OFF'
            print('Auto-Range OFF')
    
    """
    TO DO - finish configuration settings getter
    def get_configuration(self):
        '''
        Get the current measurement configuration
        '''
        return self.configuration
    """
    
    def get_max_power(self):
        '''
        Get the detector maximum power
        '''
        return self.power_meter.sense.power.dc.range.upper

    def measure(self, type='single', sample_rate=10, n_averages=10):
        '''
        Take a power measurement

        <wavelength>:
            set measurement wavelength
        <type>:
            measurement type to conduct - 'single' or 'average'
        <n_samples>:
            number of samples per measurement (default 10)
        <n_averages>:
            number of averages for average measurement (default 10)

        '''
        self.set_samples(sample_rate)
        self.n_averages = n_averages
        # set meter to take power reading
        self.power_meter.configure.scalar.power()
        # take desired reading
        if type == 'average':
            data = self.average()
        else:
            data = self.power_meter.read/self.conversion
            print(f"Power reading: {round(data, 2)}{self.unit}")

        return data
    
    def set_bandwidth(self, state='high'):
        '''
        Set bandwidth of the detector
        
        <state>:
            Set 'low' or 'high' bandwidth
        '''
        # create dict of bandwidth values
        bandwidth = {'low': 1, 'high': 0,}
        # check correct input
        if state not in bandwidth:
            print(f"Invalid state '{state}'. Please enter either 'low' or 'high'")
            return
        try:
            #set the bandwidth on the device
            self.power_meter.input.pdiode.filter.lpass.state = bandwidth[state]

            print(f'bandwidth set to {state}')
        except Exception as e:
            print(f'An error occurred: {e}')

    def set_samples(self, n_samples=1):
        '''
        Set the sample rate

        <n_samples>:
            number of samples per read (default 1)
        '''
        # set sample rate
        self.power_meter.sense.average.count = n_samples

    def set_units(self, unit=None):
        '''
        Set the default units on the meter

        <units>:
            Takes string of desired unit types

            'nW', 'uW', 'mW', 'W', 'DBM'
        '''
        # change unit if neccesary
        if unit:
            self.unit = unit
        # check for correct unit type entry
        unit_types ={'nW': 1E-9,
                     'uW': 1E-6,
                     'mW': 1E-3,
                     'W': 1,
                     'dBm': 1,}
        
        if self.unit not in unit_types:
            self.unit = input(f'Please enter correct unit type from list: {unit_types}')
        # set meter measurement unit type (W or DBM)
        if 'dBm' in [self.unit]:
            self.unit_to_measure = 'DBM'
        else:
            self.unit_to_measure = 'W'
        try:
            # set units for meter
            self.power_meter.sense.power.dc.unit = self.unit_to_measure
            self.conversion = unit_types[self.unit]
            if self.verbose:
                print(f'Units set to {self.unit}')
        except Exception as e:
            print(f'Error changing unit type: {e}')

    def set_wavelength(self, wavelength):
        '''
        Set desired wavelength of the meter

        <wavelength>:
            set wavelength to measure data in nm
        '''
        # set wavelength of the power meter
        self.power_meter.sense.correction.wavelength = wavelength