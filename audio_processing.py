## This module relates to the processing of audio stream objects

import numpy as np
import audio_streaming as ast

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
                """Check that it returns an instance of audio_envelope"""
		self.assertIsInstance(ee.extract(), Audio_envelope)

if __name__=='__main__':

        unittest.main()

	#data = np.genfromtxt('raw_vocab.data', delimiter=',')
	#asc = ast.Audio_stream_const(data)
	#print isinstance(asc, ast._IAudio_stream)
	#asc.plot_stream()

