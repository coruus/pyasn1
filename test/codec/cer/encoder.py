from pyasn1.type import namedtype, univ
from pyasn1.codec.cer import encoder
from pyasn1.error import PyAsn1Error
try:
    import unittest
except ImportError:
    raise PyAsn1Error(
        'PyUnit package\'s missing. See http://pyunit.sourceforge.net/'
        )

class BooleanEncoderTestCase(unittest.TestCase):
    def testTrue(self):
        assert encoder.encode(univ.Boolean(1)) == '\x01\x01\xff'
    def testFalse(self):
        assert encoder.encode(univ.Boolean(0)) == '\x01\x01\x00'

class BitStringEncoderTestCase(unittest.TestCase):
    def testShortMode(self):
        assert encoder.encode(
            univ.BitString((1,0)*501)
            ) == '\x03\x7f\x06' + '\xaa' * 125 + '\x80'

    def testLongMode(self):
        assert encoder.encode(
            univ.BitString((1,0)*501)
            ) == '\x03\x7f\x06' + '\xaa' * 125 + '\x80'
        
class OctetStringEncoderTestCase(unittest.TestCase):
    def testShortMode(self):
        assert encoder.encode(
            univ.OctetString('Quick brown fox')
            ) == '\x04\x0fQuick brown fox'
    def testLongMode(self):
        assert encoder.encode(
            univ.OctetString('Q'*1001)
            ) == '$\x80\x04\x82\x03\xe8' + 'Q'*1000 + '\x04\x01Q\x00\x00'
        
class SetEncoderTestCase(unittest.TestCase):
    def setUp(self):
        self.s = univ.Set(componentType=namedtype.NamedTypes(
            namedtype.NamedType('place-holder', univ.Null('')),
            namedtype.OptionalNamedType('first-name', univ.OctetString('')),
            namedtype.DefaultedNamedType('age', univ.Integer(33))
            ))

    def __init(self):
        self.s.clear()
        self.s.setComponentByPosition(0)
    def __initWithOptional(self):
        self.s.clear()
        self.s.setComponentByPosition(0)
        self.s.setComponentByPosition(1, 'quick brown')
        
    def __initWithDefaulted(self):
        self.s.clear()
        self.s.setComponentByPosition(0)
        self.s.setComponentByPosition(2, 1)
        
    def __initWithOptionalAndDefaulted(self):
        self.s.clear()
        self.s.setComponentByPosition(0, univ.Null(''))
        self.s.setComponentByPosition(1, univ.OctetString('quick brown'))
        self.s.setComponentByPosition(2, univ.Integer(1))
        
    def testIndefMode(self):
        self.__init()
        assert encoder.encode(self.s) == '1\x80\x05\x00\x00\x00'

    def testWithOptionalIndefMode(self):
        self.__initWithOptional()
        assert encoder.encode(
            self.s
            ) == '1\x80\x04\x0bquick brown\x05\x00\x00\x00'

    def testWithDefaultedIndefMode(self):
        self.__initWithDefaulted()
        assert encoder.encode(
            self.s
            ) == '1\x80\x02\x01\x01\x05\x00\x00\x00'

    def testWithOptionalAndDefaultedIndefMode(self):
        self.__initWithOptionalAndDefaulted()
        assert encoder.encode(
            self.s
            ) == '1\x80\x02\x01\x01\x04\x0bquick brown\x05\x00\x00\x00'

class SetWithChoiceEncoderTestCase(unittest.TestCase):
    def setUp(self):
        c = univ.Choice(componentType=namedtype.NamedTypes(
            namedtype.NamedType('actual', univ.Boolean(0))
            ))
        self.s = univ.Set(componentType=namedtype.NamedTypes(
            namedtype.NamedType('place-holder', univ.Null('')),
            namedtype.NamedType('status', c)
            ))

    def testIndefMode(self):
        self.s.setComponentByPosition(0)
        self.s.setComponentByName('status')
        self.s.getComponentByName('status').setComponentByPosition(0, 1)
        assert encoder.encode(self.s) == '1\x80\x01\x01\xff\x05\x00\x00\x00'

if __name__ == '__main__': unittest.main()
