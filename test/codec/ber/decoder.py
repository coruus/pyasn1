from pyasn1.type import tag, namedtype, univ
from pyasn1.codec.ber import decoder
from pyasn1.compat.octets import ints2octs, str2octs, null
from pyasn1.error import PyAsn1Error
try:
    import unittest
except ImportError:
    raise PyAsn1Error(
        'PyUnit package\'s missing. See http://pyunit.sourceforge.net/'
        )

class LargeTagDecoderTestCase(unittest.TestCase):
    def testLargeTag(self):
        assert decoder.decode(ints2octs((127, 141, 245, 182, 253, 47, 3, 2, 1, 1))) == (1, null)

class IntegerDecoderTestCase(unittest.TestCase):
    def testPosInt(self):
        assert decoder.decode(ints2octs((2, 1, 12))) == (12, null)
    def testNegInt(self):
        assert decoder.decode(ints2octs((2, 1, 244))) == (-12, null)
    def testZero(self):
        assert decoder.decode(ints2octs((2, 1, 0))) == (0, null)
    def testMinusOne(self):
        assert decoder.decode(ints2octs((2, 1, 255))) == (-1, null)
    def testPosLong(self):
        assert decoder.decode(
            ints2octs((2, 9, 0, 255, 255, 255, 255, 255, 255, 255, 255))
            ) == (0xffffffffffffffff, null)
    def testNegLong(self):
        assert decoder.decode(
            ints2octs((2, 9, 255, 0, 0, 0, 0, 0, 0, 0, 1))
            ) == (-0xffffffffffffffff, null)
    def testSpec(self):
        try:
            decoder.decode(
                ints2octs((2, 1, 12)), asn1Spec=univ.Null()
                ) == (12, null)
        except PyAsn1Error:
            pass
        else:
            assert 0, 'wrong asn1Spec worked out'
        assert decoder.decode(
            ints2octs((2, 1, 12)), asn1Spec=univ.Integer()
            ) == (12, null)

class BooleanDecoderTestCase(unittest.TestCase):
    def testTrue(self):
        assert decoder.decode(ints2octs((1, 1, 1))) == (1, null)
    def testExtraTrue(self):
        assert decoder.decode(ints2octs((1, 1, 1, 0, 120, 50, 50))) == (1, ints2octs((0, 120, 50, 50)))
    def testFalse(self):
        assert decoder.decode(ints2octs((1, 1, 0))) == (0, null)

class BitStringDecoderTestCase(unittest.TestCase):
    def testDefMode(self):
        assert decoder.decode(
            ints2octs((3, 3, 1, 169, 138))
            ) == ((1,0,1,0,1,0,0,1,1,0,0,0,1,0,1), null)
    def testIndefMode(self):
        assert decoder.decode(
            ints2octs((3, 3, 1, 169, 138))
            ) == ((1,0,1,0,1,0,0,1,1,0,0,0,1,0,1), null)
    def testDefModeChunked(self):
        assert decoder.decode(
            ints2octs((35, 8, 3, 2, 0, 169, 3, 2, 1, 138))
            ) == ((1,0,1,0,1,0,0,1,1,0,0,0,1,0,1), null)
    def testIndefModeChunked(self):
        assert decoder.decode(
            ints2octs((35, 128, 3, 2, 0, 169, 3, 2, 1, 138, 0, 0))
            ) == ((1,0,1,0,1,0,0,1,1,0,0,0,1,0,1), null)
        
class OctetStringDecoderTestCase(unittest.TestCase):
    def testDefMode(self):
        assert decoder.decode(
            ints2octs((4, 15, 81, 117, 105, 99, 107, 32, 98, 114, 111, 119, 110, 32, 102, 111, 120))
            ) == (str2octs('Quick brown fox'), null)
    def testIndefMode(self):
        assert decoder.decode(
            ints2octs((36, 128, 4, 15, 81, 117, 105, 99, 107, 32, 98, 114, 111, 119, 110, 32, 102, 111, 120, 0, 0))
            ) == (str2octs('Quick brown fox'), null)
    def testDefModeChunked(self):
        assert decoder.decode(
            ints2octs((36, 23, 4, 4, 81, 117, 105, 99, 4, 4, 107, 32, 98, 114, 4, 4, 111, 119, 110, 32, 4, 3, 102, 111, 120))
            ) == (str2octs('Quick brown fox'), null)
    def testIndefModeChunked(self):
        assert decoder.decode(
            ints2octs((36, 128, 4, 4, 81, 117, 105, 99, 4, 4, 107, 32, 98, 114, 4, 4, 111, 119, 110, 32, 4, 3, 102, 111, 120, 0, 0))
            ) == (str2octs('Quick brown fox'), null)
        
class ExpTaggedOctetStringDecoderTestCase(unittest.TestCase):
    def setUp(self):
        self.o = univ.OctetString(
            'Quick brown fox',
            tagSet=univ.OctetString.tagSet.tagExplicitly(
            tag.Tag(tag.tagClassApplication, tag.tagFormatSimple, 5)
            ))
    def testDefMode(self):
        assert self.o.isSameTypeWith(decoder.decode(
            ints2octs((101, 17, 4, 15, 81, 117, 105, 99, 107, 32, 98, 114, 111, 119, 110, 32, 102, 111, 120))
            )[0])
    def testIndefMode(self):
        v, s = decoder.decode(ints2octs((101, 128, 36, 128, 4, 15, 81, 117, 105, 99, 107, 32, 98, 114, 111, 119, 110, 32, 102, 111, 120, 0, 0, 0, 0)))
        assert self.o.isSameTypeWith(v)
        assert not s

    def testDefModeChunked(self):
        v, s = decoder.decode(ints2octs((101, 25, 36, 23, 4, 4, 81, 117, 105, 99, 4, 4, 107, 32, 98, 114, 4, 4, 111, 119, 110, 32, 4, 3, 102, 111, 120)))
        assert self.o.isSameTypeWith(v)
        assert not s

    def testIndefModeChunked(self):
        v, s = decoder.decode(ints2octs((101, 128, 36, 128, 4, 4, 81, 117, 105, 99, 4, 4, 107, 32, 98, 114, 4, 4, 111, 119, 110, 32, 4, 3, 102, 111, 120, 0, 0, 0, 0)))
        assert self.o.isSameTypeWith(v)
        assert not s

class NullDecoderTestCase(unittest.TestCase):
    def testNull(self):
        assert decoder.decode(ints2octs((5, 0))) == (null, null)

class ObjectIdentifierDecoderTestCase(unittest.TestCase):
    def testNull(self):
        assert decoder.decode(
            ints2octs((6, 6, 43, 6, 0, 191, 255, 126))
            ) == ((1,3,6,0,0xffffe), null)

class SequenceDecoderTestCase(unittest.TestCase):
    def setUp(self):
        self.s = univ.Sequence(componentType=namedtype.NamedTypes(
            namedtype.NamedType('place-holder', univ.Null(null)),
            namedtype.NamedType('first-name', univ.OctetString(null)),
            namedtype.NamedType('age', univ.Integer(33)),
            ))
        self.s.setComponentByPosition(0, univ.Null(null))
        self.s.setComponentByPosition(1, univ.OctetString('quick brown'))
        self.s.setComponentByPosition(2, univ.Integer(1))
        self.s.setDefaultComponents()
        
    def testWithOptionalAndDefaultedDefMode(self):
        assert decoder.decode(
            ints2octs((48, 18, 5, 0, 4, 11, 113, 117, 105, 99, 107, 32, 98, 114, 111, 119, 110, 2, 1, 1))
            ) == (self.s, null)
        
    def testWithOptionalAndDefaultedIndefMode(self):
        assert decoder.decode(
            ints2octs((48, 128, 5, 0, 36, 128, 4, 11, 113, 117, 105, 99, 107, 32, 98, 114, 111, 119, 110, 0, 0, 2, 1, 1, 0, 0))
            ) == (self.s, null)

    def testWithOptionalAndDefaultedDefModeChunked(self):
        assert decoder.decode(
            ints2octs((48, 24, 5, 0, 36, 17, 4, 4, 113, 117, 105, 99, 4, 4, 107, 32, 98, 114, 4, 3, 111, 119, 110, 2, 1, 1))
            ) == (self.s, null)

    def testWithOptionalAndDefaultedIndefModeChunked(self):
        assert decoder.decode(
            ints2octs((48, 128, 5, 0, 36, 128, 4, 4, 113, 117, 105, 99, 4, 4, 107, 32, 98, 114, 4, 3, 111, 119, 110, 0, 0, 2, 1, 1, 0, 0))
            ) == (self.s, null)

class GuidedSequenceDecoderTestCase(unittest.TestCase):
    def setUp(self):
        self.s = univ.Sequence(componentType=namedtype.NamedTypes(
            namedtype.NamedType('place-holder', univ.Null(null)),
            namedtype.OptionalNamedType('first-name', univ.OctetString(null)),
            namedtype.DefaultedNamedType('age', univ.Integer(33)),
            ))

    def __init(self):
        self.s.clear()
        self.s.setComponentByPosition(0, univ.Null(null))
        self.s.setDefaultComponents()
        
    def __initWithOptional(self):
        self.s.clear()
        self.s.setComponentByPosition(0, univ.Null(null))
        self.s.setComponentByPosition(1, univ.OctetString('quick brown'))
        self.s.setDefaultComponents()

    def __initWithDefaulted(self):
        self.s.clear()
        self.s.setComponentByPosition(0, univ.Null(null))
        self.s.setComponentByPosition(2, univ.Integer(1))
        self.s.setDefaultComponents()
        
    def __initWithOptionalAndDefaulted(self):
        self.s.clear()
        self.s.setComponentByPosition(0, univ.Null(null))
        self.s.setComponentByPosition(1, univ.OctetString('quick brown'))
        self.s.setComponentByPosition(2, univ.Integer(1))
        self.s.setDefaultComponents()
        
    def testDefMode(self):
        self.__init()
        assert decoder.decode(
            ints2octs((48, 128, 5, 0, 0, 0)), asn1Spec=self.s
            ) == (self.s, null)
        
    def testIndefMode(self):
        self.__init()
        assert decoder.decode(
            ints2octs((48, 128, 5, 0, 0, 0)), asn1Spec=self.s
            ) == (self.s, null)

    def testDefModeChunked(self):
        self.__init()
        assert decoder.decode(
            ints2octs((48, 2, 5, 0)), asn1Spec=self.s
            ) == (self.s, null)

    def testIndefModeChunked(self):
        self.__init()
        assert decoder.decode(
            ints2octs((48, 128, 5, 0, 0, 0)), asn1Spec=self.s
            ) == (self.s, null)

    def testWithOptionalDefMode(self):
        self.__initWithOptional()
        assert decoder.decode(
            ints2octs((48, 15, 5, 0, 4, 11, 113, 117, 105, 99, 107, 32, 98, 114, 111, 119, 110)), asn1Spec=self.s
            ) == (self.s, null)
        
    def testWithOptionaIndefMode(self):
        self.__initWithOptional()
        assert decoder.decode(
            ints2octs((48, 128, 5, 0, 36, 128, 4, 11, 113, 117, 105, 99, 107, 32, 98, 114, 111, 119, 110, 0, 0, 0, 0)),
            asn1Spec=self.s
            ) == (self.s, null)

    def testWithOptionalDefModeChunked(self):
        self.__initWithOptional()
        assert decoder.decode(
            ints2octs((48, 21, 5, 0, 36, 17, 4, 4, 113, 117, 105, 99, 4, 4, 107, 32, 98, 114, 4, 3, 111, 119, 110)),
            asn1Spec=self.s
            ) == (self.s, null)

    def testWithOptionalIndefModeChunked(self):
        self.__initWithOptional()
        assert decoder.decode(
            ints2octs((48, 128, 5, 0, 36, 128, 4, 4, 113, 117, 105, 99, 4, 4, 107, 32, 98, 114, 4, 3, 111, 119, 110, 0, 0, 0, 0)),
            asn1Spec=self.s
            ) == (self.s, null)

    def testWithDefaultedDefMode(self):
        self.__initWithDefaulted()
        assert decoder.decode(
            ints2octs((48, 5, 5, 0, 2, 1, 1)), asn1Spec=self.s
            ) == (self.s, null)
        
    def testWithDefaultedIndefMode(self):
        self.__initWithDefaulted()
        assert decoder.decode(
            ints2octs((48, 128, 5, 0, 2, 1, 1, 0, 0)), asn1Spec=self.s
            ) == (self.s, null)

    def testWithDefaultedDefModeChunked(self):
        self.__initWithDefaulted()
        assert decoder.decode(
            ints2octs((48, 5, 5, 0, 2, 1, 1)), asn1Spec=self.s
            ) == (self.s, null)

    def testWithDefaultedIndefModeChunked(self):
        self.__initWithDefaulted()
        assert decoder.decode(
            ints2octs((48, 128, 5, 0, 2, 1, 1, 0, 0)), asn1Spec=self.s
            ) == (self.s, null)

    def testWithOptionalAndDefaultedDefMode(self):
        self.__initWithOptionalAndDefaulted()
        assert decoder.decode(
            ints2octs((48, 18, 5, 0, 4, 11, 113, 117, 105, 99, 107, 32, 98, 114, 111, 119, 110, 2, 1, 1)), asn1Spec=self.s
            ) == (self.s, null)
        
    def testWithOptionalAndDefaultedIndefMode(self):
        self.__initWithOptionalAndDefaulted()
        assert decoder.decode(
            ints2octs((48, 128, 5, 0, 36, 128, 4, 11, 113, 117, 105, 99, 107, 32, 98, 114, 111, 119, 110, 0, 0, 2, 1, 1, 0, 0)), asn1Spec=self.s
            ) == (self.s, null)

    def testWithOptionalAndDefaultedDefModeChunked(self):
        self.__initWithOptionalAndDefaulted()
        assert decoder.decode(
            ints2octs((48, 24, 5, 0, 36, 17, 4, 4, 113, 117, 105, 99, 4, 4, 107, 32, 98, 114, 4, 3, 111, 119, 110, 2, 1, 1)), asn1Spec=self.s
            ) == (self.s, null)

    def testWithOptionalAndDefaultedIndefModeChunked(self):
        self.__initWithOptionalAndDefaulted()
        assert decoder.decode(
            ints2octs((48, 128, 5, 0, 36, 128, 4, 4, 113, 117, 105, 99, 4, 4, 107, 32, 98, 114, 4, 3, 111, 119, 110, 0, 0, 2, 1, 1, 0, 0)), asn1Spec=self.s
            ) == (self.s, null)

class ChoiceDecoderTestCase(unittest.TestCase):
    def setUp(self):
        self.s = univ.Choice(componentType=namedtype.NamedTypes(
            namedtype.NamedType('place-holder', univ.Null(null)),
            namedtype.NamedType('number', univ.Integer(0))
            ))

    def testBySpec(self):
        self.s.setComponentByPosition(0, univ.Null(null))
        assert decoder.decode(
            ints2octs((5, 0)), asn1Spec=self.s
            ) == (self.s, null)

    def testWithoutSpec(self):
        self.s.setComponentByPosition(0, univ.Null(null))
        assert decoder.decode(ints2octs((5, 0))) == (self.s, null)
        assert decoder.decode(ints2octs((5, 0))) == (univ.Null(null), null)

class AnyDecoderTestCase(unittest.TestCase):
    def setUp(self):
        self.s = univ.Any()

    def testByUntagged(self):
        assert decoder.decode(
            ints2octs((4, 3, 102, 111, 120)), asn1Spec=self.s
            ) == (univ.Any('\004\003fox'), null)
            
    def testTaggedEx(self):
        s = univ.Any('\004\003fox').subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 4))
        assert decoder.decode(ints2octs((164, 5, 4, 3, 102, 111, 120)), asn1Spec=s) == (s, null)
                
    def testTaggedIm(self):
        s = univ.Any('\004\003fox').subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 4))
        assert decoder.decode(ints2octs((132, 5, 4, 3, 102, 111, 120)), asn1Spec=s) == (s, null)
                    
if __name__ == '__main__': unittest.main()
