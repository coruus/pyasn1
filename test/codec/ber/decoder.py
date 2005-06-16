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
        assert decoder.decode('\x02\x01\x0c') == (12, '')
    def testNegInt(self):
        assert decoder.decode('\x02\x01\xf4') == (-12, '')
    def testZero(self):
        assert decoder.decode('\x02\x01\x00') == (0, '')
    def testMinusOne(self):
        assert decoder.decode('\x02\x01\xff') == (-1, '')
    def testPosLong(self):
        assert decoder.decode(
            '\x02\t\x00\xff\xff\xff\xff\xff\xff\xff\xff'
            ) == (0xffffffffffffffffl, '')
    def testNegLong(self):
        assert decoder.decode(
            '\x02\t\xff\x00\x00\x00\x00\x00\x00\x00\x01'
            ) == (-0xffffffffffffffffl, '')
    def testSpec(self):
        try:
            decoder.decode(
                '\x02\x01\x0c', asn1Spec=univ.Null()
                ) == (12, '')
        except PyAsn1Error:
            pass
        else:
            assert 0, 'wrong asn1Spec worked out'
        assert decoder.decode(
            '\x02\x01\x0c', asn1Spec=univ.Integer()
            ) == (12, '')

class BooleanDecoderTestCase(unittest.TestCase):
    def testTrue(self):
        assert decoder.decode('\x01\x01\x01') == (1, '')
    def testExtraTrue(self):
        assert decoder.decode('\x01\x01\x01\0x22') == (1, '\0x22')
    def testFalse(self):
        assert decoder.decode('\x01\x01\x00') == (0, '')

class BitStringDecoderTestCase(unittest.TestCase):
    def testDefMode(self):
        assert decoder.decode(
            '\x03\x03\x00\xa9\x8a'
            ) == ((1,0,1,0,1,0,0,1,1,0,0,0,1,0,1,0), '')
    def testIndefMode(self):
        assert decoder.decode(
            '#\x80\x03\x03\x00\xa9\x8a\x00\x00'
            ) == ((1,0,1,0,1,0,0,1,1,0,0,0,1,0,1,0), '')

    def testDefModeChunked(self):
        assert decoder.decode(
            '#\x08\x03\x02\x00\xa9\x03\x02\x00\x8a'
            ) == ((1,0,1,0,1,0,0,1,1,0,0,0,1,0,1,0), '')
    def testIndefModeChunked(self):
        assert decoder.decode(
            '#\x80\x03\x02\x00\xa9\x03\x02\x00\x8a\x00\x00'
            ) == ((1,0,1,0,1,0,0,1,1,0,0,0,1,0,1,0), '')
        
class OctetStringDecoderTestCase(unittest.TestCase):
    def testDefMode(self):
        assert decoder.decode(
            '\x04\x0fQuick brown fox'
            ) == ('Quick brown fox', '')
    def testIndefMode(self):
        assert decoder.decode(
            '$\x80\x04\x0fQuick brown fox\x00\x00'
            ) == ('Quick brown fox', '')
    def testDefModeChunked(self):
        assert decoder.decode(
            '$\x17\x04\x04Quic\x04\x04k br\x04\x04own \x04\x03fox'
            ) == ('Quick brown fox', '')
    def testIndefModeChunked(self):
        assert decoder.decode(
            '$\x80\x04\x04Quic\x04\x04k br\x04\x04own \x04\x03fox\x00\x00'
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
            'e\x11\x04\x0fQuick brown fox'
            )[0])
    def testIndefMode(self):
        assert self.o.isSameTypeWith(decoder.decode(
            'e\x80$\x80\x04\x0fQuick brown fox\x00\x00\x00\x00'
            )[0])
    def testDefModeChunked(self):
        assert self.o.isSameTypeWith(decoder.decode(
            'e\x19$\x17\x04\x04Quic\x04\x04k br\x04\x04own \x04\x03fox'
            )[0])
    def testIndefModeChunked(self):
        assert self.o.isSameTypeWith(decoder.decode(
            'e\x80$\x80\x04\x04Quic\x04\x04k br\x04\x04own \x04\x03fox\x00\x00\x00\x00'
            )[0])

class NullDecoderTestCase(unittest.TestCase):
    def testNull(self):
        assert decoder.decode('\x05\x00') == ('', '')

class ObjectIdentifierDecoderTestCase(unittest.TestCase):
    def testNull(self):
        assert decoder.decode(
            '\x06\x06+\x06\x00\xbf\xff~'
            ) == ((1,3,6,0,0xffffe), '')

class SequenceDecoderTestCase(unittest.TestCase):
    def setUp(self):
        self.s = univ.Sequence(componentType=namedtype.NamedTypes(
            namedtype.NamedType('place-holder', univ.Null()),
            namedtype.NamedType('first-name', univ.OctetString()),
            namedtype.NamedType('age', univ.Integer(33)),
            ))
        self.s.setComponentByPosition(0, univ.Null())
        self.s.setComponentByPosition(1, univ.OctetString('quick brown'))
        self.s.setComponentByPosition(2, univ.Integer(1))
        self.s.setDefaultComponents()
        
    def testWithOptionalAndDefaultedDefMode(self):
        assert decoder.decode(
            '0\x12\x05\x00\x04\x0bquick brown\x02\x01\x01',
            ) == (self.s, '')
        
    def testWithOptionalAndDefaultedIndefMode(self):
        assert decoder.decode(
            '0\x80\x05\x00$\x80\x04\x0bquick brown\x00\x00\x02\x01\x01\x00\x00'
            ) == (self.s, '')

    def testWithOptionalAndDefaultedDefModeChunked(self):
        assert decoder.decode(
            '0\x18\x05\x00$\x11\x04\x04quic\x04\x04k br\x04\x03own\x02\x01\x01'
            ) == (self.s, '')

    def testWithOptionalAndDefaultedIndefModeChunked(self):
        assert decoder.decode(
            '0\x80\x05\x00$\x80\x04\x04quic\x04\x04k br\x04\x03own\x00\x00\x02\x01\x01\x00\x00'
            ) == (self.s, '')

class GuidedSequenceDecoderTestCase(unittest.TestCase):
    def setUp(self):
        self.s = univ.Sequence(componentType=namedtype.NamedTypes(
            namedtype.NamedType('place-holder', univ.Null()),
            namedtype.OptionalNamedType('first-name', univ.OctetString()),
            namedtype.DefaultedNamedType('age', univ.Integer(33)),
            ))

    def __init(self):
        self.s.clear()
        self.s.setComponentByPosition(0, univ.Null())
        self.s.setDefaultComponents()
        
    def __initWithOptional(self):
        self.s.clear()
        self.s.setComponentByPosition(0, univ.Null())
        self.s.setComponentByPosition(1, univ.OctetString('quick brown'))
        self.s.setDefaultComponents()

    def __initWithDefaulted(self):
        self.s.clear()
        self.s.setComponentByPosition(0, univ.Null())
        self.s.setComponentByPosition(2, univ.Integer(1))
        self.s.setDefaultComponents()
        
    def __initWithOptionalAndDefaulted(self):
        self.s.clear()
        self.s.setComponentByPosition(0, univ.Null())
        self.s.setComponentByPosition(1, univ.OctetString('quick brown'))
        self.s.setComponentByPosition(2, univ.Integer(1))
        self.s.setDefaultComponents()
        
    def testDefMode(self):
        self.__init()
        assert decoder.decode(
            '0\x02\x05\x00', asn1Spec=self.s
            ) == (self.s, '')
        
    def testIndefMode(self):
        self.__init()
        assert decoder.decode(
            '0\x80\x05\x00\x00\x00', asn1Spec=self.s
            ) == (self.s, '')

    def testDefModeChunked(self):
        self.__init()
        assert decoder.decode(
            '0\x02\x05\x00', asn1Spec=self.s
            ) == (self.s, '')

    def testIndefModeChunked(self):
        self.__init()
        assert decoder.decode(
            '0\x80\x05\x00\x00\x00', asn1Spec=self.s
            ) == (self.s, '')

    def testWithOptionalDefMode(self):
        self.__initWithOptional()
        assert decoder.decode(
            '0\x0f\x05\x00\x04\x0bquick brown', asn1Spec=self.s
            ) == (self.s, '')
        
    def testWithOptionaIndefMode(self):
        self.__initWithOptional()
        assert decoder.decode(
            '0\x80\x05\x00$\x80\x04\x0bquick brown\x00\x00\x00\x00',
            asn1Spec=self.s
            ) == (self.s, '')

    def testWithOptionalDefModeChunked(self):
        self.__initWithOptional()
        assert decoder.decode(
            '0\x15\x05\x00$\x11\x04\x04quic\x04\x04k br\x04\x03own',
            asn1Spec=self.s
            ) == (self.s, '')

    def testWithOptionalIndefModeChunked(self):
        self.__initWithOptional()
        assert decoder.decode(
            '0\x80\x05\x00$\x80\x04\x04quic\x04\x04k br\x04\x03own\x00\x00\x00\x00',
            asn1Spec=self.s
            ) == (self.s, '')

    def testWithDefaultedDefMode(self):
        self.__initWithDefaulted()
        assert decoder.decode(
            '0\x05\x05\x00\x02\x01\x01', asn1Spec=self.s
            ) == (self.s, '')
        
    def testWithDefaultedIndefMode(self):
        self.__initWithDefaulted()
        assert decoder.decode(
            '0\x80\x05\x00\x02\x01\x01\x00\x00', asn1Spec=self.s
            ) == (self.s, '')

    def testWithDefaultedDefModeChunked(self):
        self.__initWithDefaulted()
        assert decoder.decode(
            '0\x05\x05\x00\x02\x01\x01', asn1Spec=self.s
            ) == (self.s, '')

    def testWithDefaultedIndefModeChunked(self):
        self.__initWithDefaulted()
        assert decoder.decode(
            '0\x80\x05\x00\x02\x01\x01\x00\x00', asn1Spec=self.s
            ) == (self.s, '')

    def testWithOptionalAndDefaultedDefMode(self):
        self.__initWithOptionalAndDefaulted()
        assert decoder.decode(
            '0\x12\x05\x00\x04\x0bquick brown\x02\x01\x01', asn1Spec=self.s
            ) == (self.s, '')
        
    def testWithOptionalAndDefaultedIndefMode(self):
        self.__initWithOptionalAndDefaulted()
        assert decoder.decode(
            '0\x80\x05\x00$\x80\x04\x0bquick brown\x00\x00\x02\x01\x01\x00\x00', asn1Spec=self.s
            ) == (self.s, '')

    def testWithOptionalAndDefaultedDefModeChunked(self):
        self.__initWithOptionalAndDefaulted()
        assert decoder.decode(
            '0\x18\x05\x00$\x11\x04\x04quic\x04\x04k br\x04\x03own\x02\x01\x01', asn1Spec=self.s
            ) == (self.s, '')

    def testWithOptionalAndDefaultedIndefModeChunked(self):
        self.__initWithOptionalAndDefaulted()
        assert decoder.decode(
            '0\x80\x05\x00$\x80\x04\x04quic\x04\x04k br\x04\x03own\x00\x00\x02\x01\x01\x00\x00', asn1Spec=self.s
            ) == (self.s, '')

class ChoiceDecoderTestCase(unittest.TestCase):
    def setUp(self):
        self.s = univ.Choice(componentType=namedtype.NamedTypes(
            namedtype.NamedType('place-holder', univ.Null()),
            namedtype.NamedType('number', univ.Integer())
            ))

    def testBySpec(self):
        self.s.setComponentByPosition(0, univ.Null())
        assert decoder.decode(
            '\x05\x00', asn1Spec=self.s
            ) == (self.s, '')

    def testWithoutSpec(self):
        self.s.setComponentByPosition(0, univ.Null())
        assert decoder.decode('\x05\x00') == (self.s, '')
        assert decoder.decode('\x05\x00') == (univ.Null(), '')

if __name__ == '__main__': unittest.main()
