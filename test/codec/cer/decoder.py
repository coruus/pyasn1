from pyasn1.type import univ
from pyasn1.codec.cer import decoder
from pyasn1.error import PyAsn1Error
try:
    import unittest
except ImportError:
    raise PyAsn1Error(
        'PyUnit package\'s missing. See http://pyunit.sourceforge.net/'
        )

class BooleanDecoderTestCase(unittest.TestCase):
    def testTrue(self):
        assert decoder.decode('\x01\x01\xff') == (1, '')
    def testFalse(self):
        assert decoder.decode('\x01\x01\x00') == (0, '')
        
class OctetStringDecoderTestCase(unittest.TestCase):
    def testShortMode(self):
        assert decoder.decode(
            '\x04\x0fQuick brown fox'
            ) == ('Quick brown fox', '')
    def testLongMode(self):
        assert decoder.decode(
            '$\x80\x04\x82\x03\xe8' + 'Q'*1000 + '\x04\x01Q\x00\x00'
            ) == ('Q'*1001, '')

if __name__ == '__main__': unittest.main()
