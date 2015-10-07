## This module relates to the processing of audio stream objects

## ToDo: Why is envelope extraction so slow?
from collections import deque
import numpy as np
import audio_streaming as ast


class Audio_envelope():

	def __init__(self, data=None):
		if isinstance(data, dict):
			self.data = data
		else:
			raise TypeError('Require dictionary to create instance of  Audio_envelope') 


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
		envelope = dict()

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

		return Audio_envelope(envelope)


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

if __name__=='__main__':

        unittest.main()

	#data = np.genfromtxt('raw_vocab.data', delimiter=',')
	#asc = ast.Audio_stream_const(data)
	#print isinstance(asc, ast._IAudio_stream)
	#asc.plot_stream()

