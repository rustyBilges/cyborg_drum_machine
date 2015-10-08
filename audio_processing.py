## This module relates to the processing of audio stream objects

## ToDo: Why is envelope extraction so slow?
##	 > introduce sampling class (remove sampling from extract( ) method)

from collections import deque, OrderedDict
from abc import ABCMeta, abstractmethod
import numpy as np
import matplotlib.pyplot as plt
import audio_streaming as ast


class Audio_envelope():

	def __init__(self, original_stream=None, data=None):
		if isinstance(data, dict) and isinstance(original_stream, ast._IAudio_stream):
			self.original_stream = original_stream
			self.data = data
		else:
			raise TypeError('Require audio stream and env dictionary to create instance of  Audio_envelope') 

	def return_envelope_dict(self):
		return self.data

	def sub_envelope(self, start, finish):
		stream = self.original_stream.sub_stream(start,finish)

		data = OrderedDict()
		for t in self.data.keys():
			if t>=start and t<=finish:
				data[t] = self.data[t]

		return Audio_envelope(stream, data)


	def plot(self, color = 'r'):
		plt.plot(self.data.keys(), self.data.values(), color)
		#plt.show()	


class Envelope_extractor():
	"""Class for extraction of audio envelope
		> Only variable is window_length
		> extract()  returns Audio_envelope method
	"""
	def __init__(self, audio_stream, window_length=100):

		self.stream = audio_stream
		self.window_length = window_length

	def extract(self):

		if not isinstance(self.stream, ast._IAudio_stream):
			raise TypeError('Can only extract envelope from an audio stream')

		if self.window_length >= self.stream.length:
			raise ValueError('Envelope window too long by far.')

		data = self.stream.return_mono_amplitude_array()
		data = data[::10]              ## THIS IS UNACCOUNTED FOR
		envelope = OrderedDict()

                time = 0
                window = deque([])
                t_window = deque([])
                for i in data:
                        window.append(np.abs(i))
                        t_window.append(time)
                        if len(window)>self.window_length:
                                window.popleft()
                                t_window.popleft()
                                envelope[np.mean(t_window)] = np.mean(window)
                        time += 1
		return Audio_envelope(self.stream, envelope)



class Drum_hit():

	def __init__(self, envelope, hit_start, hit_finish):
		
		self.start = hit_start
		self.finish = hit_finish
		self.envelope = envelope.sub_envelope(hit_start, hit_finish)

class _IHit_detector():

	__metaclass__=ABCMeta

	@abstractmethod
	def front_edge_detector(self): pass
	
	@abstractmethod
	def back_edge_detector(self): pass
	
	@abstractmethod
	def second_front_edge_detector(self): pass

class Hit_detector_naive(_IHit_detector):
	"""Implement hit detector interface.

	   Naive hit detection based on thresholding audio envelope.
	   ToDO:  calculate audio metrics (e.g. velocity) for the hits (add to interfacemethods or another class?)		
	"""
	def __init__(self, envelope, hit_count=None, threshold_on=10):

		self.envelope = envelope
		self.envelope_dict = envelope.return_envelope_dict()
		self.hit_count = hit_count

		self.state = 'off'  ## 'not hit'
		self.threshold_on = threshold_on
		self.threshold_off = threshold_on

		self.hits  = []

	def detect(self):

		hit_start = None
		hit_end   = None
		for t in self.envelope_dict.keys():
	
			if self.state=='off' and self.front_edge_detector(t):
				self.state = 'on'
				hit_start = t
			if self.state=='on':
				hit_end = t
				self.hits.append(Drum_hit(self.envelope, hit_start, hit_end))
				self.state = 'off'
				
	def front_edge_detector(self, t): 
		if self.envelope_dict[t] > self.threshold_on:
			return True	
	

	def back_edge_detector(self): pass
	

	def second_front_edge_detector(self): pass

##############################################################################################################
## From here on is unit test code for the above defined classes:
import unittest

class Test_envelope_extractor(unittest.TestCase):
        """Class to test envelope extractor

        Note that a valid audio stream file is requried for tests to succeed.
        This should be called 'raw_vocab.data', and have following properties:
                > shape (88240,)
                > comma separated
                > mono i.e. just a list of wave amplitude values
        """

        def test_return(self):
                """Check that it returns a valid instance of audio_envelope
		   Irrespective of the window length.
		"""
		data = np.genfromtxt('raw_vocab.data', delimiter=',')
		asc = ast.Audio_stream_const(data)

		ee = Envelope_extractor(asc, asc.length+1.1)  ## test with window length greater than stream length
		with self.assertRaises(ValueError):
			ee.extract()
		ee = Envelope_extractor(asc)  ## test with default window length (100)
		self.assertIsInstance(ee.extract(), Audio_envelope)


class Test_hit_detector_naive(unittest.TestCase):
	"""Class to test most basic implementation of a hit detector
		> requires functioning audio stream, and envelope extractor
	"""

	def test_return(self):	
		"""Test that two hits are detected from the envelope"""
			
		data = np.genfromtxt('raw_vocab.data', delimiter=',')
		asc = ast.Audio_stream_const(data)
		ee = Envelope_extractor(asc, 100) 			
		envelope = ee.extract()
		hd = Hit_detector_naive(envelope, hit_count=2)
		hits = hd.detect()

		self.assertEqual(len(hits), 2)
		self.assertIsInstance(hits[0], Drum_hit)
		self.assertIsInstance(hits[1], Drum_hit)


if __name__=='__main__':

        unittest.main()

	#data = np.genfromtxt('raw_vocab.data', delimiter=',')
	#asc = ast.Audio_stream_const(data)
	
	#i = 0
	#cols = ['r','b','g']
	#for le in [100, 500, 1000]:
	#	ee = Envelope_extractor(asc, le) 
#		env = ee.extract()
#		env.plot(cols[i])
#		i += 1

#	plt.show()  #edit plot func#  

