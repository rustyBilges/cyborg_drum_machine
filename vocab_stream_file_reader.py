## This file contains code relating to recording and reading of audio streams.
## And a basic audio stream class (conts, also use dynamic for a stream that can update?)


import unittest
import numpy as np

class Audio_stream_const():
	"""A class to represent a fixed stream of audio data.
		ToDo: have this class implement a stream interface. Later to write e.g. Audio_stream_dynamic
	"""  
	def __init__(self, length=None, frequency=None):

		self.length = length
		self.frequency = frequency	

class Audio_stream_file_reader():
	"""A class to read vocab from a saved numpy array representing an audio stream
	   For reading of other file types (e.g. .wav) - Implement new classes!	
	 
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

		return Audio_stream_const()


##############################################################################################################
## From here on is unit test code for the above defined classes:

class Test_audio_stream_file_reader(unittest.TestCase):
	"""Class to test functionality of Audio_stream_file_reader

	Note that a valid audio stream file is requried for tests to succeed.
	This should be called 'raw_vocab.data'
	"""

	def test_file_open(self):
		"""Check that handling of bogus and correct file names is safe"""
		with self.assertRaises(IOError):
			asfr = Audio_stream_file_reader('bogus_fname.txt')


	def test_return_stream(self):
		"""Check that the read method returns an audio stream object"""
		asfr = Audio_stream_file_reader('raw_vocab.data')
		self.assertIsInstance(asfr.read(), Audio_stream_const)    ## maybe this will need to change to Audio_stream (dynamic or const)
		

if __name__=='__main__':

	unittest.main()



