from pyasn1.type import namedtype, univ
from pyasn1.codec.der import encoder
try:
    import unittest
except ImportError:
    raise error.PyAsn1Error(
        'PyUnit package\'s missing. See http://pyunit.sourceforge.net/'
        )

class OctetStringEncoderTestCase(unittest.TestCase):
    def testShortMode(self):
        assert encoder.encode(
            univ.OctetString('Quick brown fox')
            ) == '\x04\x0fQuick brown fox'

class BitStringEncoderTestCase(unittest.TestCase):
    def testShortMode(self):
        assert encoder.encode(
            univ.BitString((1,))
            ) == '\x03\x02\x07\x80'
        
class SetWithChoiceEncoderTestCase(unittest.TestCase):
    def setUp(self):
        c = univ.Choice(componentType=namedtype.NamedTypes(
            namedtype.NamedType('name', univ.OctetString()),
            namedtype.NamedType('amount', univ.Integer())
            ))
        self.s = univ.Set(componentType=namedtype.NamedTypes(
            namedtype.NamedType('place-holder', univ.Null()),
            namedtype.NamedType('status', c)
            ))

    def testDefMode(self):
        self.s.setComponentByPosition(0)
        self.s.setComponentByName('status')
        self.s.getComponentByName('status').setComponentByPosition(0, 'ann')
        assert encoder.encode(self.s) == '1\x07\x04\x03ann\x05\x00'

if __name__ == '__main__': unittest.main()
