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
        assert encoder.encode(univ.Boolean(1)) == '\001\001\377'
    def testFalse(self):
        assert encoder.encode(univ.Boolean(0)) == '\001\001\000'

class BitStringEncoderTestCase(unittest.TestCase):
    def testShortMode(self):
        assert encoder.encode(
            univ.BitString((1,0)*501)
            ) == '\003\177\006' + '\252' * 125 + '\200'

    def testLongMode(self):
        assert encoder.encode(
            univ.BitString((1,0)*501)
            ) == '\003\177\006' + '\252' * 125 + '\200'
        
class OctetStringEncoderTestCase(unittest.TestCase):
    def testShortMode(self):
        assert encoder.encode(
            univ.OctetString('Quick brown fox')
            ) == '\004\017Quick brown fox'
    def testLongMode(self):
        assert encoder.encode(
            univ.OctetString('Q'*1001)
            ) == '$\200\004\202\003\350' + 'Q'*1000 + '\004\001Q\000\000'
        
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
        assert encoder.encode(self.s) == '1\200\005\000\000\000'

    def testWithOptionalIndefMode(self):
        self.__initWithOptional()
        assert encoder.encode(
            self.s
            ) == '1\200\004\013quick brown\005\000\000\000'

    def testWithDefaultedIndefMode(self):
        self.__initWithDefaulted()
        assert encoder.encode(
            self.s
            ) == '1\200\002\001\001\005\000\000\000'

    def testWithOptionalAndDefaultedIndefMode(self):
        self.__initWithOptionalAndDefaulted()
        assert encoder.encode(
            self.s
            ) == '1\200\002\001\001\004\013quick brown\005\000\000\000'

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
        assert encoder.encode(self.s) == '1\200\001\001\377\005\000\000\000'

if __name__ == '__main__': unittest.main()
