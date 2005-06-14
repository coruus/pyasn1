from pyasn1.type import univ
from pyasn1.codec.der import decoder
try:
    import unittest
except ImportError:
    raise error.PyAsn1Error(
        'PyUnit package\'s missing. See http://pyunit.sourceforge.net/'
        )

class OctetStringDecoderTestCase(unittest.TestCase):
    def testShortMode(self):
        assert decoder.decode(
            '\x04\x0fQuick brown fox'
            ) == ('Quick brown fox', '')

if __name__ == '__main__': unittest.main()
