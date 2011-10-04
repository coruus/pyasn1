from pyasn1.type import univ
from pyasn1.codec.der import decoder
from pyasn1.error import PyAsn1Error
try:
    import unittest
except ImportError:
    raise PyAsn1Error(
        'PyUnit package\'s missing. See http://pyunit.sourceforge.net/'
        )

class OctetStringDecoderTestCase(unittest.TestCase):
    def testShortMode(self):
        assert decoder.decode(
            '\004\017Quick brown fox'.encode()
            ) == ('Quick brown fox'.encode(), ''.encode())

if __name__ == '__main__': unittest.main()
