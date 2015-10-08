## This file contains code relating to recording and reading of audio streams.
## And a basic audio stream classes

## ToDo : Implement a dynamic audio stream

from abc import ABCMeta, abstractmethod

import numpy as np
import matplotlib.pyplot as plt
import wave, struct

class _IAudio_stream():
	"""Interface class for an audio stream"""
	__metaclass__ = ABCMeta
	
	@abstractmethod
	def plot_stream(self): pass
	
	@abstractmethod
	def return_mono_amplitude_array(self): pass

	@abstractmethod
	def sub_stream(self): pass

class Audio_stream_const(_IAudio_stream):
	"""A class to represent a fixed stream of audio data.
	"""  
	def __init__(self, data, frequency=44100):

		self.data = data
		self.length = len(data)
		self.frequency = frequency	

		print("nframes = " + str(self.length))
		print("framerate = " + str(self.frequency))
	
	def plot_stream(self):
		plt.plot(range(self.length), self.data, 'b')
		plt.show()
	
	def return_mono_amplitude_array(self): 
		return self.data

	def sub_stream(self, start, finish):
		data = self.data[int(start):int(finish)]
		return Audio_stream_const(data, self.frequency) 


class _IAudio_stream_reader():
	
	__metaclass__ = ABCMeta

	@abstractmethod
	def read(self): pass

class Audio_stream_csv_reader_mono():
	"""A class to read vocab from a saved numpy array (csv) representing an audio stream
	
	   read() creates a constant stream instance, because the file is assumed to be fixed.
	"""
	
	def __init__(self, fname=None):

		self.fname = fname
			
		try:
			f = open(fname)
			f.close()
		except:
			raise IOError('Cannot open audio stream file:' + fname)

	def read(self):
		data = np.genfromtxt(self.fname, delimiter=',')
		return Audio_stream_const(data)


class Audio_stream_wav_reader():
	"""A class to read vocab from a .wav audio file
	
	   read() creates a constant stream instance, because the file is assumed to be fixed.
	   This is implemented for 16-bit stereo wav file, uncompressed.
	"""
	
	def __init__(self, fname=None):

		self.fname = fname
			
		try:
			f = wave.open(fname, 'r')
			f.close()
		except:
			raise IOError('Cannot open audio stream file:' + fname)

	def read(self):
		
		wav = wave.open (self.fname, "r")
		(nchannels, sampwidth, framerate, nframes, comptype, compname) = wav.getparams ()
		frames = wav.readframes (nframes * nchannels)
		out = struct.unpack_from ("%dh" % nframes * nchannels, frames)

		# Convert 2 channles to numpy arrays
		if nchannels == 2:
			left = np.asarray (list (out[0::2]))
			right = np.asarray (list  (out[1::2]))
			data = (left + right) / 2.0
		else:
		       data = array (out)
	 	return Audio_stream_const(data, framerate)

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
		"""Check that the rea	d method returns an audio stream object, with correct attribute values"""
		asfr = Audio_stream_csv_reader_mono('raw_vocab.data')
		self.assertIsInstance(asfr.read(), _IAudio_stream)        ## check that the returned stream implements the interface (not strictly necessary given next)	
		self.assertIsInstance(asfr.read(), Audio_stream_const)    ## check that the returned stream is a constant audio stream		
		self.assertEqual(asfr.read().length, 88240)

class Test_audio_stream_wav_reader(unittest.TestCase):
	"""Test wav_reader functionality

		NOte: this test requires raw_vocab2.wav which contains 3 hits (generated in hydrogen)
	"""

	def test_file_open(self):
		"""Check that handling of bogus and correct file names is safe"""
		with self.assertRaises(IOError):
			asfr = Audio_stream_wav_reader('bogus_fname.txt')
	def test_return_stream(self):

		"""Check that the rea	d method returns an audio stream object, with correct attribute values"""
		asfr = Audio_stream_wav_reader('raw_vocab2.wav')
		self.assertIsInstance(asfr.read(), Audio_stream_const)    ## check that the returned stream is a constant audio stream		
		self.assertEqual(asfr.read().length, 88200)

if __name__=='__main__':

	unittest.main()


