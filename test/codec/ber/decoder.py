from pyasn1.type import tag, namedtype, univ
from pyasn1.codec.ber import decoder
from pyasn1.error import PyAsn1Error
try:
    import unittest
except ImportError:
    raise PyAsn1Error(
        'PyUnit package\'s missing. See http://pyunit.sourceforge.net/'
        )

class IntegerDecoderTestCase(unittest.TestCase):
    def testPosInt(self):
        assert decoder.decode('\002\001\014') == (12, '')
    def testNegInt(self):
        assert decoder.decode('\002\001\364') == (-12, '')
    def testZero(self):
        assert decoder.decode('\002\001\000') == (0, '')
    def testMinusOne(self):
        assert decoder.decode('\002\001\377') == (-1, '')
    def testPosLong(self):
        assert decoder.decode(
            '\002\011\000\377\377\377\377\377\377\377\377'
            ) == (0xffffffffffffffffl, '')
    def testNegLong(self):
        assert decoder.decode(
            '\002\011\377\000\000\000\000\000\000\000\001'
            ) == (-0xffffffffffffffffl, '')
    def testSpec(self):
        try:
            decoder.decode(
                '\002\001\014', asn1Spec=univ.Null()
                ) == (12, '')
        except PyAsn1Error:
            pass
        else:
            assert 0, 'wrong asn1Spec worked out'
        assert decoder.decode(
            '\002\001\014', asn1Spec=univ.Integer()
            ) == (12, '')

class BooleanDecoderTestCase(unittest.TestCase):
    def testTrue(self):
        assert decoder.decode('\001\001\001') == (1, '')
    def testExtraTrue(self):
        assert decoder.decode('\001\001\001\000x22') == (1, '\0x22')
    def testFalse(self):
        assert decoder.decode('\001\001\000') == (0, '')

class BitStringDecoderTestCase(unittest.TestCase):
    def testDefMode(self):
        assert decoder.decode(
            '\003\003\001\251\212'
            ) == ((1,0,1,0,1,0,0,1,1,0,0,0,1,0,1), '')
    def testIndefMode(self):
        assert decoder.decode(
            '\003\003\001\251\212'
            ) == ((1,0,1,0,1,0,0,1,1,0,0,0,1,0,1), '')
    def testDefModeChunked(self):
        assert decoder.decode(
            '#\010\003\002\000\251\003\002\001\212'
            ) == ((1,0,1,0,1,0,0,1,1,0,0,0,1,0,1), '')
    def testIndefModeChunked(self):
        assert decoder.decode(
            '#\200\003\002\000\251\003\002\001\212\000\000'
            ) == ((1,0,1,0,1,0,0,1,1,0,0,0,1,0,1), '')
        
class OctetStringDecoderTestCase(unittest.TestCase):
    def testDefMode(self):
        assert decoder.decode(
            '\004\017Quick brown fox'
            ) == ('Quick brown fox', '')
    def testIndefMode(self):
        assert decoder.decode(
            '$\200\004\017Quick brown fox\000\000'
            ) == ('Quick brown fox', '')
    def testDefModeChunked(self):
        assert decoder.decode(
            '$\027\004\004Quic\004\004k br\004\004own \004\003fox'
            ) == ('Quick brown fox', '')
    def testIndefModeChunked(self):
        assert decoder.decode(
            '$\200\004\004Quic\004\004k br\004\004own \004\003fox\000\000'
            ) == ('Quick brown fox', '')
        
class ExpTaggedOctetStringDecoderTestCase(unittest.TestCase):
    def setUp(self):
        self.o = univ.OctetString(
            'Quick brown fox',
            tagSet=univ.OctetString.tagSet.tagExplicitly(
            tag.Tag(tag.tagClassApplication, tag.tagFormatSimple, 5)
            ))
    def testDefMode(self):
        assert self.o.isSameTypeWith(decoder.decode(
            'e\021\004\017Quick brown fox'
            )[0])
    def testIndefMode(self):
        assert self.o.isSameTypeWith(decoder.decode(
            'e\200$\200\004\017Quick brown fox\000\000\000\000'
            )[0])
    def testDefModeChunked(self):
        assert self.o.isSameTypeWith(decoder.decode(
            'e\031$\027\004\004Quic\004\004k br\004\004own \004\003fox'
            )[0])
    def testIndefModeChunked(self):
        assert self.o.isSameTypeWith(decoder.decode(
            'e\200$\200\004\004Quic\004\004k br\004\004own \004\003fox\000\000\000\000'
            )[0])

class NullDecoderTestCase(unittest.TestCase):
    def testNull(self):
        assert decoder.decode('\005\000') == ('', '')

class ObjectIdentifierDecoderTestCase(unittest.TestCase):
    def testNull(self):
        assert decoder.decode(
            '\006\006+\006\000\277\377~'
            ) == ((1,3,6,0,0xffffe), '')

class SequenceDecoderTestCase(unittest.TestCase):
    def setUp(self):
        self.s = univ.Sequence(componentType=namedtype.NamedTypes(
            namedtype.NamedType('place-holder', univ.Null('')),
            namedtype.NamedType('first-name', univ.OctetString('')),
            namedtype.NamedType('age', univ.Integer(33)),
            ))
        self.s.setComponentByPosition(0, univ.Null(''))
        self.s.setComponentByPosition(1, univ.OctetString('quick brown'))
        self.s.setComponentByPosition(2, univ.Integer(1))
        self.s.setDefaultComponents()
        
    def testWithOptionalAndDefaultedDefMode(self):
        assert decoder.decode(
            '0\022\005\000\004\013quick brown\002\001\001'
            ) == (self.s, '')
        
    def testWithOptionalAndDefaultedIndefMode(self):
        assert decoder.decode(
            '0\200\005\000$\200\004\013quick brown\000\000\002\001\001\000\000'
            ) == (self.s, '')

    def testWithOptionalAndDefaultedDefModeChunked(self):
        assert decoder.decode(
            '0\030\005\000$\021\004\004quic\004\004k br\004\003own\002\001\001'
            ) == (self.s, '')

    def testWithOptionalAndDefaultedIndefModeChunked(self):
        assert decoder.decode(
            '0\200\005\000$\200\004\004quic\004\004k br\004\003own\000\000\002\001\001\000\000'
            ) == (self.s, '')

class GuidedSequenceDecoderTestCase(unittest.TestCase):
    def setUp(self):
        self.s = univ.Sequence(componentType=namedtype.NamedTypes(
            namedtype.NamedType('place-holder', univ.Null('')),
            namedtype.OptionalNamedType('first-name', univ.OctetString('')),
            namedtype.DefaultedNamedType('age', univ.Integer(33)),
            ))

    def __init(self):
        self.s.clear()
        self.s.setComponentByPosition(0, univ.Null(''))
        self.s.setDefaultComponents()
        
    def __initWithOptional(self):
        self.s.clear()
        self.s.setComponentByPosition(0, univ.Null(''))
        self.s.setComponentByPosition(1, univ.OctetString('quick brown'))
        self.s.setDefaultComponents()

    def __initWithDefaulted(self):
        self.s.clear()
        self.s.setComponentByPosition(0, univ.Null(''))
        self.s.setComponentByPosition(2, univ.Integer(1))
        self.s.setDefaultComponents()
        
    def __initWithOptionalAndDefaulted(self):
        self.s.clear()
        self.s.setComponentByPosition(0, univ.Null(''))
        self.s.setComponentByPosition(1, univ.OctetString('quick brown'))
        self.s.setComponentByPosition(2, univ.Integer(1))
        self.s.setDefaultComponents()
        
    def testDefMode(self):
        self.__init()
        assert decoder.decode(
            '0\200\005\000\000\000', asn1Spec=self.s
            ) == (self.s, '')
        
    def testIndefMode(self):
        self.__init()
        assert decoder.decode(
            '0\200\005\000\000\000', asn1Spec=self.s
            ) == (self.s, '')

    def testDefModeChunked(self):
        self.__init()
        assert decoder.decode(
            '0\002\005\000', asn1Spec=self.s
            ) == (self.s, '')

    def testIndefModeChunked(self):
        self.__init()
        assert decoder.decode(
            '0\200\005\000\000\000', asn1Spec=self.s
            ) == (self.s, '')

    def testWithOptionalDefMode(self):
        self.__initWithOptional()
        assert decoder.decode(
            '0\017\005\000\004\013quick brown', asn1Spec=self.s
            ) == (self.s, '')
        
    def testWithOptionaIndefMode(self):
        self.__initWithOptional()
        assert decoder.decode(
            '0\200\005\000$\200\004\013quick brown\000\000\000\000',
            asn1Spec=self.s
            ) == (self.s, '')

    def testWithOptionalDefModeChunked(self):
        self.__initWithOptional()
        assert decoder.decode(
            '0\025\005\000$\021\004\004quic\004\004k br\004\003own',
            asn1Spec=self.s
            ) == (self.s, '')

    def testWithOptionalIndefModeChunked(self):
        self.__initWithOptional()
        assert decoder.decode(
            '0\200\005\000$\200\004\004quic\004\004k br\004\003own\000\000\000\000',
            asn1Spec=self.s
            ) == (self.s, '')

    def testWithDefaultedDefMode(self):
        self.__initWithDefaulted()
        assert decoder.decode(
            '0\005\005\000\002\001\001', asn1Spec=self.s
            ) == (self.s, '')
        
    def testWithDefaultedIndefMode(self):
        self.__initWithDefaulted()
        assert decoder.decode(
            '0\200\005\000\002\001\001\000\000', asn1Spec=self.s
            ) == (self.s, '')

    def testWithDefaultedDefModeChunked(self):
        self.__initWithDefaulted()
        assert decoder.decode(
            '0\005\005\000\002\001\001', asn1Spec=self.s
            ) == (self.s, '')

    def testWithDefaultedIndefModeChunked(self):
        self.__initWithDefaulted()
        assert decoder.decode(
            '0\200\005\000\002\001\001\000\000', asn1Spec=self.s
            ) == (self.s, '')

    def testWithOptionalAndDefaultedDefMode(self):
        self.__initWithOptionalAndDefaulted()
        assert decoder.decode(
            '0\022\005\000\004\013quick brown\002\001\001', asn1Spec=self.s
            ) == (self.s, '')
        
    def testWithOptionalAndDefaultedIndefMode(self):
        self.__initWithOptionalAndDefaulted()
        assert decoder.decode(
            '0\200\005\000$\200\004\013quick brown\000\000\002\001\001\000\000', asn1Spec=self.s
            ) == (self.s, '')

    def testWithOptionalAndDefaultedDefModeChunked(self):
        self.__initWithOptionalAndDefaulted()
        assert decoder.decode(
            '0\030\005\000$\021\004\004quic\004\004k br\004\003own\002\001\001', asn1Spec=self.s
            ) == (self.s, '')

    def testWithOptionalAndDefaultedIndefModeChunked(self):
        self.__initWithOptionalAndDefaulted()
        assert decoder.decode(
            '0\200\005\000$\200\004\004quic\004\004k br\004\003own\000\000\002\001\001\000\000', asn1Spec=self.s
            ) == (self.s, '')

class ChoiceDecoderTestCase(unittest.TestCase):
    def setUp(self):
        self.s = univ.Choice(componentType=namedtype.NamedTypes(
            namedtype.NamedType('place-holder', univ.Null('')),
            namedtype.NamedType('number', univ.Integer(0))
            ))

    def testBySpec(self):
        self.s.setComponentByPosition(0, univ.Null(''))
        assert decoder.decode(
            '\005\000', asn1Spec=self.s
            ) == (self.s, '')

    def testWithoutSpec(self):
        self.s.setComponentByPosition(0, univ.Null(''))
        assert decoder.decode('\005\000') == (self.s, '')
        assert decoder.decode('\005\000') == (univ.Null(''), '')

if __name__ == '__main__': unittest.main()
