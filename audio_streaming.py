## This file contains code relating to recording and reading of audio streams.
## And a basic audio stream classes

## ToDo : Implement a dynamic audio stream

from abc import ABCMeta, abstractmethod

import numpy as np
import matplotlib.pyplot as plt

class _IAudio_stream():
	"""Interface class for an audio stream"""
	__metaclass__ = ABCMeta
	
	@abstractmethod
	def plot_stream(self): pass
	
	@abstractmethod
	def return_mono_amplitude_array(self): pass

class Audio_stream_const(_IAudio_stream):
	"""A class to represent a fixed stream of audio data.
		ToDo: have this class implement a stream interface. Later to write e.g. Audio_stream_dynamic
	"""  
	def __init__(self, data, frequency=None):

		self.data = data
		self.length = len(data)
		self.frequency = frequency	
	
	def plot_stream(self):
		plt.plot(range(self.length), self.data, 'b')
		plt.show()
	
	def return_mono_amplitude_array(self): 
		return self.data

class Audio_stream_csv_reader_mono():
	"""A class to read vocab from a saved numpy array (csv) representing an audio stream
	   For reading of other file types (e.g. .wav) - Implement new classes!	
	
	   read() creates a constant stream instance, because the file is assumed to be fixed.
	 
		ToDo: this class should implement an interface for a generic stream_reader 
		(as should e.g. Audio_stream_live_recorder())
	"""
	
	def __init__(self, fname=None):

		self.fname = fname
			
		try:
			f = open(fname)
			f.close()
		except:
			raise IOError('Cannot open audio stream file.')

	def read(self):
		data = np.genfromtxt(self.fname, delimiter=',')
		return Audio_stream_const(data)


##############################################################################################################
## From here on is unit test code for the above defined classes:
import unittest

class Test_audio_stream_csv_reader_mono(unittest.TestCase):
	"""Class to test functionality of Audio_stream_csv_reader_mono

	Note that a valid audio stream file is requried for tests to succeed.
	This should be called 'raw_vocab.data', and have following properties:
		> shape (88240,)
		> comma separated
		> mono i.e. just a list of wave amplitude values
	"""

	def test_file_open(self):
		"""Check that handling of bogus and correct file names is safe"""
		with self.assertRaises(IOError):
			asfr = Audio_stream_csv_reader_mono('bogus_fname.txt')


	def test_return_stream(self):
		"""Check that the read method returns an audio stream object, with correct attribute values"""
		asfr = Audio_stream_csv_reader_mono('raw_vocab.data')
		self.assertIsInstance(asfr.read(), _IAudio_stream)        ## check that the returned stream implements the interface (not strictly necessary given next)	
		self.assertIsInstance(asfr.read(), Audio_stream_const)    ## check that the returned stream is a constant audio stream		
		self.assertEqual(asfr.read().length, 88240)

if __name__=='__main__':

	unittest.main()


