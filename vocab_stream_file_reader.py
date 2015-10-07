## This file contains code relating to recording and reading of audio streams.
## And ia basic audio stream classe.


import unittest

class Audio_stream_file_reader():
	"""A class to read vocab from a saved .wav audio file"""
	## inevitably this class should implement an interface for a generic stream_reader (as should e.g. Audio_stream_live_recorder())


class Test_audio_stream_file_reader(unittest.TestCase):
	"""Class to test functionality of Audio_stream_file_reader"""

	def test_file_open(self):
		"""Check that handling of bogus fname is safe"""
		asfr = Audio_stream_file_reader('bogus_fname.txt')
		with self.assertRaises(ValueError):
			asfr.check_file()


if __name__=='__main__':

	unittest.main()



