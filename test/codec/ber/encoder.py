from pyasn1.type import tag, namedtype, univ
from pyasn1.codec.ber import encoder
from pyasn1.error import PyAsn1Error
try:
    import unittest
except ImportError:
    raise PyAsn1Error(
        'PyUnit package\'s missing. See http://pyunit.sourceforge.net/'
        )

class IntegerEncoderTestCase(unittest.TestCase):
    def testPosInt(self):
        assert encoder.encode(univ.Integer(12)) == '\x02\x01\x0c'
    def testNegInt(self):
        assert encoder.encode(univ.Integer(-12)) == '\x02\x01\xf4'
    def testZero(self):
        assert encoder.encode(univ.Integer(0)) == '\x02\x01\x00'
    def testMinusOne(self):
        assert encoder.encode(univ.Integer(-1)) == '\x02\x01\xff'
    def testPosLong(self):
        assert encoder.encode(
            univ.Integer(0xffffffffffffffffl)
            ) == '\x02\t\x00\xff\xff\xff\xff\xff\xff\xff\xff'
    def testNegLong(self):
        assert encoder.encode(
            univ.Integer(-0xffffffffffffffffl)
            ) == '\x02\t\xff\x00\x00\x00\x00\x00\x00\x00\x01'

class BooleanEncoderTestCase(unittest.TestCase):
    def testTrue(self):
        assert encoder.encode(univ.Boolean(1)) == '\x01\x01\x01'
    def testFalse(self):
        assert encoder.encode(univ.Boolean(0)) == '\x01\x01\x00'

class BitStringEncoderTestCase(unittest.TestCase):
    def setUp(self):
        self.b = univ.BitString("'A98A'H")
    def testDefMode(self):
        assert encoder.encode(self.b) == '\x03\x03\x00\xa9\x8a'

    def testIndefMode(self):
        assert encoder.encode(
            self.b, defMode=0
            ) == '\x03\x03\x00\xa9\x8a'
        
    def testDefModeChunked(self):
        assert encoder.encode(
            self.b, maxChunkSize=1
            ) == '#\x08\x03\x02\x00\xa9\x03\x02\x00\x8a'

    def testIndefModeChunked(self):
        assert encoder.encode(
            self.b, defMode=0, maxChunkSize=1
            ) == '#\x80\x03\x02\x00\xa9\x03\x02\x00\x8a\x00\x00'
        
class OctetStringEncoderTestCase(unittest.TestCase):
    def setUp(self):
        self.o = univ.OctetString('Quick brown fox')
    def testDefMode(self):
        assert encoder.encode(self.o) == '\x04\x0fQuick brown fox'
    def testIndefMode(self):
        assert encoder.encode(
            self.o, defMode=0
            ) == '\x04\x0fQuick brown fox'
    def testDefModeChunked(self):
        assert encoder.encode(
            self.o, maxChunkSize=4
            ) == '$\x17\x04\x04Quic\x04\x04k br\x04\x04own \x04\x03fox'
    def testIndefModeChunked(self):
        assert encoder.encode(
            self.o, defMode=0, maxChunkSize=4
            ) == '$\x80\x04\x04Quic\x04\x04k br\x04\x04own \x04\x03fox\x00\x00'
        
class ExpTaggedOctetStringEncoderTestCase(unittest.TestCase):
    def setUp(self):
        self.o = univ.OctetString().subtype(
            value='Quick brown fox',
            explicitTag=tag.Tag(tag.tagClassApplication,tag.tagFormatSimple,5)
            )
    def testDefMode(self):
        assert encoder.encode(self.o) == 'e\x11\x04\x0fQuick brown fox'
    def testIndefMode(self):
        assert encoder.encode(
            self.o, defMode=0
            ) == 'e\x80\x04\x0fQuick brown fox\x00\x00'
    def testDefModeChunked(self):
        assert encoder.encode(
            self.o, defMode=1, maxChunkSize=4
            ) == 'e\x19$\x17\x04\x04Quic\x04\x04k br\x04\x04own \x04\x03fox'
    def testIndefModeChunked(self):
        assert encoder.encode(
            self.o, defMode=0, maxChunkSize=4
            ) == 'e\x80$\x80\x04\x04Quic\x04\x04k br\x04\x04own \x04\x03fox\x00\x00\x00\x00'

class NullEncoderTestCase(unittest.TestCase):
    def testNull(self):
        assert encoder.encode(univ.Null()) == '\x05\x00'

class ObjectIdentifierEncoderTestCase(unittest.TestCase):
    def testNull(self):
        assert encoder.encode(
            univ.ObjectIdentifier((1,3,6,0,0xffffe))
            ) == '\x06\x06+\x06\x00\xbf\xff~'

class SequenceEncoderTestCase(unittest.TestCase):
    def setUp(self):
        self.s = univ.Sequence(componentType=namedtype.NamedTypes(
            namedtype.NamedType('place-holder', univ.Null()),
            namedtype.OptionalNamedType('first-name', univ.OctetString()),
            namedtype.DefaultedNamedType('age', univ.Integer(33)),
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
        self.s.setComponentByPosition(0, univ.Null())
        self.s.setComponentByPosition(1, univ.OctetString('quick brown'))
        self.s.setComponentByPosition(2, univ.Integer(1))
        
    def testDefMode(self):
        self.__init()
        assert encoder.encode(self.s) == '0\x02\x05\x00'
        
    def testIndefMode(self):
        self.__init()
        assert encoder.encode(
            self.s, defMode=0
            ) == '0\x80\x05\x00\x00\x00'

    def testDefModeChunked(self):
        self.__init()
        assert encoder.encode(
            self.s, defMode=1, maxChunkSize=4
            ) == '0\x02\x05\x00'

    def testIndefModeChunked(self):
        self.__init()
        assert encoder.encode(
            self.s, defMode=0, maxChunkSize=4
            ) == '0\x80\x05\x00\x00\x00'

    def testWithOptionalDefMode(self):
        self.__initWithOptional()
        assert encoder.encode(self.s) == '0\x0f\x05\x00\x04\x0bquick brown'
        
    def testWithOptionalIndefMode(self):
        self.__initWithOptional()
        assert encoder.encode(
            self.s, defMode=0
            ) == '0\x80\x05\x00\x04\x0bquick brown\x00\x00'

    def testWithOptionalDefModeChunked(self):
        self.__initWithOptional()
        assert encoder.encode(
            self.s, defMode=1, maxChunkSize=4
            ) == '0\x15\x05\x00$\x11\x04\x04quic\x04\x04k br\x04\x03own'

    def testWithOptionalIndefModeChunked(self):
        self.__initWithOptional()
        assert encoder.encode(
            self.s, defMode=0, maxChunkSize=4
            ) == '0\x80\x05\x00$\x80\x04\x04quic\x04\x04k br\x04\x03own\x00\x00\x00\x00'

    def testWithDefaultedDefMode(self):
        self.__initWithDefaulted()
        assert encoder.encode(self.s) == '0\x05\x05\x00\x02\x01\x01'
        
    def testWithDefaultedIndefMode(self):
        self.__initWithDefaulted()
        assert encoder.encode(
            self.s, defMode=0
            ) == '0\x80\x05\x00\x02\x01\x01\x00\x00'

    def testWithDefaultedDefModeChunked(self):
        self.__initWithDefaulted()
        assert encoder.encode(
            self.s, defMode=1, maxChunkSize=4
            ) == '0\x05\x05\x00\x02\x01\x01'

    def testWithDefaultedIndefModeChunked(self):
        self.__initWithDefaulted()
        assert encoder.encode(
            self.s, defMode=0, maxChunkSize=4
            ) == '0\x80\x05\x00\x02\x01\x01\x00\x00'

    def testWithOptionalAndDefaultedDefMode(self):
        self.__initWithOptionalAndDefaulted()
        assert encoder.encode(self.s) == '0\x12\x05\x00\x04\x0bquick brown\x02\x01\x01'
        
    def testWithOptionalAndDefaultedIndefMode(self):
        self.__initWithOptionalAndDefaulted()
        assert encoder.encode(
            self.s, defMode=0
            ) == '0\x80\x05\x00\x04\x0bquick brown\x02\x01\x01\x00\x00'

    def testWithOptionalAndDefaultedDefModeChunked(self):
        self.__initWithOptionalAndDefaulted()
        assert encoder.encode(
            self.s, defMode=1, maxChunkSize=4
            ) == '0\x18\x05\x00$\x11\x04\x04quic\x04\x04k br\x04\x03own\x02\x01\x01'

    def testWithOptionalAndDefaultedIndefModeChunked(self):
        self.__initWithOptionalAndDefaulted()
        assert encoder.encode(
            self.s, defMode=0, maxChunkSize=4
            ) == '0\x80\x05\x00$\x80\x04\x04quic\x04\x04k br\x04\x03own\x00\x00\x02\x01\x01\x00\x00'

class ChoiceEncoderTestCase(unittest.TestCase):
    def setUp(self):
        self.s = univ.Choice(componentType=namedtype.NamedTypes(
            namedtype.NamedType('place-holder', univ.Null()),
            namedtype.NamedType('number', univ.Integer())
            ))

    def testEmpty(self):
        try:
            encoder.encode(self.s)
        except PyAsn1Error:
            pass
        else:
            assert 0, 'encoded unset choice'
        
    def testFilled(self):
        self.s.setComponentByPosition(0, univ.Null())
        assert encoder.encode(self.s) == '\x05\x00'

if __name__ == '__main__': unittest.main()
