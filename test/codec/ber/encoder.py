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
        assert encoder.encode(univ.Integer(12)) == '\002\001\014'
    def testNegInt(self):
        assert encoder.encode(univ.Integer(-12)) == '\002\001\364'
    def testZero(self):
        assert encoder.encode(univ.Integer(0)) == '\002\001\000'
    def testMinusOne(self):
        assert encoder.encode(univ.Integer(-1)) == '\002\001\377'
    def testPosLong(self):
        assert encoder.encode(
            univ.Integer(0xffffffffffffffffl)
            ) == '\002\011\000\377\377\377\377\377\377\377\377'
    def testNegLong(self):
        assert encoder.encode(
            univ.Integer(-0xffffffffffffffffl)
            ) == '\002\011\377\000\000\000\000\000\000\000\001'

class BooleanEncoderTestCase(unittest.TestCase):
    def testTrue(self):
        assert encoder.encode(univ.Boolean(1)) == '\001\001\001'
    def testFalse(self):
        assert encoder.encode(univ.Boolean(0)) == '\001\001\000'

class BitStringEncoderTestCase(unittest.TestCase):
    def setUp(self):
        self.b = univ.BitString((1,0,1,0,1,0,0,1,1,0,0,0,1,0,1))
    def testDefMode(self):
        assert encoder.encode(self.b) == '\003\003\001\251\212'
    def testIndefMode(self):
        assert encoder.encode(
            self.b, defMode=0
            ) == '\003\003\001\251\212'
    def testDefModeChunked(self):
        assert encoder.encode(
            self.b, maxChunkSize=1
            ) == '#\010\003\002\000\251\003\002\001\212'
    def testIndefModeChunked(self):
        assert encoder.encode(
            self.b, defMode=0, maxChunkSize=1
            ) == '#\200\003\002\000\251\003\002\001\212\000\000'
        
class OctetStringEncoderTestCase(unittest.TestCase):
    def setUp(self):
        self.o = univ.OctetString('Quick brown fox')
    def testDefMode(self):
        assert encoder.encode(self.o) == '\004\017Quick brown fox'
    def testIndefMode(self):
        assert encoder.encode(
            self.o, defMode=0
            ) == '\004\017Quick brown fox'
    def testDefModeChunked(self):
        assert encoder.encode(
            self.o, maxChunkSize=4
            ) == '$\027\004\004Quic\004\004k br\004\004own \004\003fox'
    def testIndefModeChunked(self):
        assert encoder.encode(
            self.o, defMode=0, maxChunkSize=4
            ) == '$\200\004\004Quic\004\004k br\004\004own \004\003fox\000\000'
        
class ExpTaggedOctetStringEncoderTestCase(unittest.TestCase):
    def setUp(self):
        self.o = univ.OctetString().subtype(
            value='Quick brown fox',
            explicitTag=tag.Tag(tag.tagClassApplication,tag.tagFormatSimple,5)
            )
    def testDefMode(self):
        assert encoder.encode(self.o) == 'e\021\004\017Quick brown fox'
    def testIndefMode(self):
        assert encoder.encode(
            self.o, defMode=0
            ) == 'e\200\004\017Quick brown fox\000\000'
    def testDefModeChunked(self):
        assert encoder.encode(
            self.o, defMode=1, maxChunkSize=4
            ) == 'e\031$\027\004\004Quic\004\004k br\004\004own \004\003fox'
    def testIndefModeChunked(self):
        assert encoder.encode(
            self.o, defMode=0, maxChunkSize=4
            ) == 'e\200$\200\004\004Quic\004\004k br\004\004own \004\003fox\000\000\000\000'

class NullEncoderTestCase(unittest.TestCase):
    def testNull(self):
        assert encoder.encode(univ.Null('')) == '\005\000'

class ObjectIdentifierEncoderTestCase(unittest.TestCase):
    def testNull(self):
        assert encoder.encode(
            univ.ObjectIdentifier((1,3,6,0,0xffffe))
            ) == '\006\006+\006\000\277\377~'

class SequenceEncoderTestCase(unittest.TestCase):
    def setUp(self):
        self.s = univ.Sequence(componentType=namedtype.NamedTypes(
            namedtype.NamedType('place-holder', univ.Null('')),
            namedtype.OptionalNamedType('first-name', univ.OctetString('')),
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
        self.s.setComponentByPosition(0, univ.Null(''))
        self.s.setComponentByPosition(1, univ.OctetString('quick brown'))
        self.s.setComponentByPosition(2, univ.Integer(1))
        
    def testDefMode(self):
        self.__init()
        assert encoder.encode(self.s) == '0\002\005\000'
        
    def testIndefMode(self):
        self.__init()
        assert encoder.encode(
            self.s, defMode=0
            ) == '0\200\005\000\000\000'

    def testDefModeChunked(self):
        self.__init()
        assert encoder.encode(
            self.s, defMode=1, maxChunkSize=4
            ) == '0\002\005\000'

    def testIndefModeChunked(self):
        self.__init()
        assert encoder.encode(
            self.s, defMode=0, maxChunkSize=4
            ) == '0\200\005\000\000\000'

    def testWithOptionalDefMode(self):
        self.__initWithOptional()
        assert encoder.encode(self.s) == '0\017\005\000\004\013quick brown'
        
    def testWithOptionalIndefMode(self):
        self.__initWithOptional()
        assert encoder.encode(
            self.s, defMode=0
            ) == '0\200\005\000\004\013quick brown\000\000'

    def testWithOptionalDefModeChunked(self):
        self.__initWithOptional()
        assert encoder.encode(
            self.s, defMode=1, maxChunkSize=4
            ) == '0\025\005\000$\021\004\004quic\004\004k br\004\003own'

    def testWithOptionalIndefModeChunked(self):
        self.__initWithOptional()
        assert encoder.encode(
            self.s, defMode=0, maxChunkSize=4
            ) == '0\200\005\000$\200\004\004quic\004\004k br\004\003own\000\000\000\000'

    def testWithDefaultedDefMode(self):
        self.__initWithDefaulted()
        assert encoder.encode(self.s) == '0\005\005\000\002\001\001'
        
    def testWithDefaultedIndefMode(self):
        self.__initWithDefaulted()
        assert encoder.encode(
            self.s, defMode=0
            ) == '0\200\005\000\002\001\001\000\000'

    def testWithDefaultedDefModeChunked(self):
        self.__initWithDefaulted()
        assert encoder.encode(
            self.s, defMode=1, maxChunkSize=4
            ) == '0\005\005\000\002\001\001'

    def testWithDefaultedIndefModeChunked(self):
        self.__initWithDefaulted()
        assert encoder.encode(
            self.s, defMode=0, maxChunkSize=4
            ) == '0\200\005\000\002\001\001\000\000'

    def testWithOptionalAndDefaultedDefMode(self):
        self.__initWithOptionalAndDefaulted()
        assert encoder.encode(self.s) == '0\022\005\000\004\013quick brown\002\001\001'
        
    def testWithOptionalAndDefaultedIndefMode(self):
        self.__initWithOptionalAndDefaulted()
        assert encoder.encode(
            self.s, defMode=0
            ) == '0\200\005\000\004\013quick brown\002\001\001\000\000'

    def testWithOptionalAndDefaultedDefModeChunked(self):
        self.__initWithOptionalAndDefaulted()
        assert encoder.encode(
            self.s, defMode=1, maxChunkSize=4
            ) == '0\030\005\000$\021\004\004quic\004\004k br\004\003own\002\001\001'

    def testWithOptionalAndDefaultedIndefModeChunked(self):
        self.__initWithOptionalAndDefaulted()
        assert encoder.encode(
            self.s, defMode=0, maxChunkSize=4
            ) == '0\200\005\000$\200\004\004quic\004\004k br\004\003own\000\000\002\001\001\000\000'

class ChoiceEncoderTestCase(unittest.TestCase):
    def setUp(self):
        self.s = univ.Choice(componentType=namedtype.NamedTypes(
            namedtype.NamedType('place-holder', univ.Null('')),
            namedtype.NamedType('number', univ.Integer(0))
            ))

    def testEmpty(self):
        try:
            encoder.encode(self.s)
        except PyAsn1Error:
            pass
        else:
            assert 0, 'encoded unset choice'
        
    def testFilled(self):
        self.s.setComponentByPosition(0, univ.Null(''))
        assert encoder.encode(self.s) == '\005\000'

if __name__ == '__main__': unittest.main()
