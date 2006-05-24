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
        assert decoder.decode('\001\001\377') == (1, '')
    def testFalse(self):
        assert decoder.decode('\001\001\000') == (0, '')
        
class OctetStringDecoderTestCase(unittest.TestCase):
    def testShortMode(self):
        assert decoder.decode(
            '\004\017Quick brown fox'
            ) == ('Quick brown fox', '')
    def testLongMode(self):
        assert decoder.decode(
            '$\200\004\202\003\350' + 'Q'*1000 + '\004\001Q\000\000'
            ) == ('Q'*1001, '')

if __name__ == '__main__': unittest.main()
