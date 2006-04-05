from pyasn1.type import univ, tag, constraint, namedtype, namedval, error
from pyasn1.error import PyAsn1Error
try:
    import unittest
except ImportError:
    raise PyAsn1Error(
        'PyUnit package\'s missing. See http://pyunit.sourceforge.net/'
        )

class IntegerTestCase(unittest.TestCase):
    def testStr(self): assert str(univ.Integer(1)) == '1', 'str() fails'
    def testAnd(self): assert univ.Integer(1) & 0 == 0, '__and__() fails'
    def testOr(self): assert univ.Integer(1) | 0 == 1, '__or__() fails'
    def testXor(self): assert univ.Integer(1) ^ 0 == 1, '__xor__() fails'
    def testRand(self): assert 0 & univ.Integer(1) == 0, '__rand__() fails'
    def testRor(self): assert 0 | univ.Integer(1) == 1, '__ror__() fails'
    def testRxor(self): assert 0 ^ univ.Integer(1) == 1, '__rxor__() fails'    
    def testAdd(self): assert univ.Integer(-4) + 6 == 2, '__add__() fails'
    def testRadd(self): assert 4 + univ.Integer(5) == 9, '__radd__() fails'
    def testSub(self): assert univ.Integer(3) - 6 == -3, '__sub__() fails'
    def testRsub(self): assert 6 - univ.Integer(3) == 3, '__rsub__() fails'
    def testMul(self): assert univ.Integer(3) * -3 == -9, '__mul__() fails'
    def testRmul(self): assert 2 * univ.Integer(3) == 6, '__rmul__() fails'
    def testDiv(self): assert univ.Integer(3) / 2 == 1, '__div__() fails'
    def testRdiv(self): assert 6 / univ.Integer(3) == 2, '__rdiv__() fails'
    def testMod(self): assert univ.Integer(3) % 2 == 1, '__mod__() fails'
    def testRmod(self): assert 4 % univ.Integer(3) == 1, '__rmod__() fails'
    def testPow(self): assert univ.Integer(3) ** 2 == 9, '__pow__() fails'
    def testRpow(self): assert 2 ** univ.Integer(2) == 4, '__rpow__() fails'
    def testLshift(self): assert univ.Integer(1) << 1 == 2, '<< fails'
    def testRshift(self): assert univ.Integer(2) >> 1 == 1, '>> fails'
    def testInt(self): assert int(univ.Integer(3)) == 3, '__int__() fails'
    def testLong(self): assert int(univ.Integer(8)) == 8, '__long__() fails'
    def testFloat(self): assert float(univ.Integer(4))==4.0,'__float__() fails'
    def testPrettyIn(self): assert univ.Integer('3') == 3, 'prettyIn() fails'
    def testTag(self):
        assert univ.Integer().getTagSet() == tag.TagSet(
            (),
            tag.Tag(tag.tagClassUniversal, tag.tagFormatSimple, 0x02)
            )
    def testNamedVals(self):
        i = univ.Integer(
            'asn1', namedValues=univ.Integer.namedValues.clone(('asn1', 1))
            )
        assert i == 1, 'named val fails'
        assert str(i) != 'asn1', 'named val __str__() fails'

class BooleanTestCase(unittest.TestCase):
    def testStr(self): assert str(univ.Boolean(1)) == '1', 'str() fails'
    def testTag(self):
        assert univ.Boolean().getTagSet() == tag.TagSet(
            (),
            tag.Tag(tag.tagClassUniversal, tag.tagFormatSimple, 0x01)
            )
    def testConstraints(self):
        try:
            univ.Boolean(2)
        except error.ValueConstraintError:
            pass
        else:
            assert 0, 'constraint fail'
    def testSubtype(self):
        assert univ.Integer().subtype(
            value=1,
            implicitTag=tag.Tag(tag.tagClassPrivate,tag.tagFormatSimple,2),
            subtypeSpec=constraint.SingleValueConstraint(1,3)
            ) == univ.Integer(
            value=1,
            tagSet=tag.TagSet(tag.Tag(tag.tagClassPrivate,
                                        tag.tagFormatSimple,2)),
            subtypeSpec=constraint.ConstraintsIntersection(constraint.SingleValueConstraint(1,3))
            )

class BitStringTestCase(unittest.TestCase):
    def setUp(self):
        self.b = univ.BitString(
            namedValues=namedval.NamedValues(('Active', 0), ('Urgent', 1))
            )
    def testSet(self):
        assert self.b.clone('Active') == (1,)
        assert self.b.clone("'1010100110001010'B") == (1,0,1,0,1,0,0,1,1,0,0,0,1,0,1,0)
        assert self.b.clone("'A98A'H") == (1,0,1,0,1,0,0,1,1,0,0,0,1,0,1,0)
        assert self.b.clone((1,0,1)) == (1,0,1)
    def testStr(self):
        assert str(self.b.clone('Urgent,Active')) == '(1, 1)'
    def testRepr(self):
        assert repr(self.b.clone('Urgent,Active')) == 'BitString("\'11\'B")'
    def testTag(self):
        assert univ.BitString().getTagSet() == tag.TagSet(
            (),
            tag.Tag(tag.tagClassUniversal, tag.tagFormatSimple, 0x03)
            )
    def testLen(self): assert len(self.b.clone("'A98A'H")) == 16
    def testIter(self):
        assert self.b.clone("'A98A'H")[0] == 1
        assert self.b.clone("'A98A'H")[1] == 0
        assert self.b.clone("'A98A'H")[2] == 1
        
class OctetStringTestCase(unittest.TestCase):
    def testStr(self):
        assert str(univ.OctetString('q')) == 'q', '__str__() fails'
    def testSeq(self):
        assert univ.OctetString('q')[0] == 'q','__getitem__() fails'
    def testAdd(self):
        assert univ.OctetString() + 'q' == 'q', '__add__() fails'
    def testRadd(self):
        assert 'b' + univ.OctetString('q') == 'bq', '__radd__() fails'
    def testMul(self):
        assert univ.OctetString('a') * 2 == 'aa', '__mul__() fails'
    def testRmul(self):
        assert 2 * univ.OctetString('b') == 'bb', '__rmul__() fails'
    def testTag(self):
        assert univ.OctetString().getTagSet() == tag.TagSet(
            (),
            tag.Tag(tag.tagClassUniversal, tag.tagFormatSimple, 0x04)
            )

class Null(unittest.TestCase):
    def testStr(self): assert str(univ.Null()) == '', 'str() fails'
    def testTag(self):
        assert univ.Null().getTagSet() == tag.TagSet(
            (),
            tag.Tag(tag.tagClassUniversal, tag.tagFormatSimple, 0x05)
            )
    def testConstraints(self):
        try:
            univ.Null(2)
        except error.ValueConstraintError:
            pass
        else:
            assert 0, 'constraint fail'

class ObjectIdentifier(unittest.TestCase):
    def testStr(self):
        assert str(univ.ObjectIdentifier((1,3,6))) == '(1, 3, 6)'
    def testEq(self):
        assert univ.ObjectIdentifier((1,3,6)) == (1,3,6), '__cmp__() fails'
    def testAdd(self):
        assert univ.ObjectIdentifier((1,3)) + (6,)==(1,3,6),'__add__() fails'
    def testRadd(self):
        assert (1,) + univ.ObjectIdentifier((3,6))==(1,3,6),'__radd__() fails'
    def testLen(self):
        assert len(univ.ObjectIdentifier((1,3))) == 2,'__len__() fails'
    def testPrefix(self):
        o = univ.ObjectIdentifier('1.3.6')
        assert o.isPrefixOf((1,3,6)), 'isPrefixOf() fails'
        assert o.isPrefixOf((1,3,6,1)), 'isPrefixOf() fails'
        assert not o.isPrefixOf((1,3)), 'isPrefixOf() fails'        
    def testInput(self):
        assert univ.ObjectIdentifier('1.3.6')==(1,3,6),'prettyIn() fails'
    def testTag(self):
        assert univ.ObjectIdentifier().getTagSet() == tag.TagSet(
            (),
            tag.Tag(tag.tagClassUniversal, tag.tagFormatSimple, 0x06)
            )

class SequenceOf(unittest.TestCase):
    def setUp(self):
        self.s1 = univ.SequenceOf(
            componentType=univ.OctetString()
            )
        self.s2 = self.s1.clone()
    def testTag(self):
        assert self.s1.getTagSet() == tag.TagSet(
            (),
            tag.Tag(tag.tagClassUniversal, tag.tagFormatConstructed, 0x10)
            ), 'wrong tagSet'
    def testSeq(self):
        self.s1.setComponentByPosition(0, univ.OctetString('abc'))
        assert self.s1[0] == 'abc', 'set by idx fails'
        self.s1.setComponentByPosition(0, 'cba')
        assert self.s1[0] == 'cba', 'set by idx fails'
    def testCmp(self):
        self.s1.clear()
        self.s1.setComponentByPosition(0, 'abc')
        self.s2.clear()
        self.s2.setComponentByPosition(0, univ.OctetString('abc'))
        assert self.s1 == self.s2, '__cmp__() fails'
    def testSubtypeSpec(self):
        s = self.s1.clone(subtypeSpec=constraint.ConstraintsUnion(
            constraint.SingleValueConstraint('abc')
            ))
        try:
            s.setComponentByPosition(0, univ.OctetString('abc'))
        except:
            assert 0, 'constraint fails'
        try:
            s.setComponentByPosition(1, univ.OctetString('Abc'))
        except:
            pass
        else:
            assert 0, 'constraint fails'
    def testSizeSpec(self):
        s = self.s1.clone(sizeSpec=constraint.ConstraintsUnion(
            constraint.ValueSizeConstraint(1,1)
            ))
        s.setComponentByPosition(0, univ.OctetString('abc'))
        try:
            s.verifySizeSpec()
        except:
            assert 0, 'size spec fails'
        s.setComponentByPosition(1, univ.OctetString('abc'))
        try:
            s.verifySizeSpec()
        except:
            pass
        else:
            assert 0, 'size spec fails'
    def testGetComponentTypeMap(self):
        assert self.s1.getComponentTypeMap() == {
            univ.OctetString.tagSet: univ.OctetString()
            }
    def testSubtype(self):
        self.s1.clear()
        assert self.s1.subtype(
            implicitTag=tag.Tag(tag.tagClassPrivate,tag.tagFormatSimple,2),
            subtypeSpec=constraint.SingleValueConstraint(1,3),
            sizeSpec=constraint.ValueSizeConstraint(0,1)
            ) == self.s1.clone(
            tagSet=tag.TagSet(tag.Tag(tag.tagClassPrivate,
                                        tag.tagFormatSimple,2)),
            subtypeSpec=constraint.ConstraintsIntersection(constraint.SingleValueConstraint(1,3)),
            sizeSpec=constraint.ValueSizeConstraint(0,1)
            )
    def testClone(self):
        self.s1.setComponentByPosition(0, univ.OctetString('abc'))
        s = self.s1.clone()
        assert len(s) == 0
        s = self.s1.clone(cloneValueFlag=1)
        assert len(s) == 1
        assert s.getComponentByPosition(0) == self.s1.getComponentByPosition(0)
        
class Sequence(unittest.TestCase):
    def setUp(self):
        self.s1 = univ.Sequence(componentType=namedtype.NamedTypes(
            namedtype.NamedType('name', univ.OctetString()),
            namedtype.OptionalNamedType('nick', univ.OctetString()),
            namedtype.DefaultedNamedType('age', univ.Integer(34))
            ))
    def testTag(self):
        assert self.s1.getTagSet() == tag.TagSet(
            (),
            tag.Tag(tag.tagClassUniversal, tag.tagFormatConstructed, 0x10)
            ), 'wrong tagSet'
    def testById(self):
        self.s1.setComponentByName('name', univ.OctetString('abc'))
        assert self.s1.getComponentByName('name') == 'abc', 'set by name fails'
    def testGetNearPosition(self):
        assert self.s1.getComponentTypeMapNearPosition(1) == {
            univ.OctetString.tagSet: univ.OctetString(),
            univ.Integer.tagSet: univ.Integer(34)
            }
        assert self.s1.getComponentPositionNearType(
            univ.OctetString.tagSet, 1
            ) == 1
    def testGetDefaultComponentByPosition(self):
        self.s1.clear()
        assert self.s1.getDefaultComponentByPosition(0) == None
        assert self.s1.getDefaultComponentByPosition(2) == univ.Integer(34)
    def testSetDefaultComponents(self):
        self.s1.clear()
        assert self.s1.getComponentByPosition(2) == None
        self.s1.setComponentByPosition(0, univ.OctetString('Ping'))
        self.s1.setComponentByPosition(1, univ.OctetString('Pong'))
        self.s1.setDefaultComponents()
        assert self.s1.getComponentByPosition(2) == 34
    def testClone(self):
        self.s1.setComponentByPosition(0, univ.OctetString('abc'))
        self.s1.setComponentByPosition(1, univ.OctetString('def'))
        self.s1.setComponentByPosition(2, univ.Integer(123))
        s = self.s1.clone()
        assert s.getComponentByPosition(0) != self.s1.getComponentByPosition(0)
        assert s.getComponentByPosition(1) != self.s1.getComponentByPosition(1)
        assert s.getComponentByPosition(2) != self.s1.getComponentByPosition(2)
        s = self.s1.clone(cloneValueFlag=1)
        assert s.getComponentByPosition(0) == self.s1.getComponentByPosition(0)
        assert s.getComponentByPosition(1) == self.s1.getComponentByPosition(1)
        assert s.getComponentByPosition(2) == self.s1.getComponentByPosition(2)

class SetOf(unittest.TestCase):
    def setUp(self):
        self.s1 = univ.SetOf(componentType=univ.OctetString())
    def testTag(self):
        assert self.s1.getTagSet() == tag.TagSet(
            (),
            tag.Tag(tag.tagClassUniversal, tag.tagFormatConstructed, 0x11)
            ), 'wrong tagSet'
    def testSeq(self):
        self.s1.setComponentByPosition(0, univ.OctetString('abc'))
        assert self.s1[0] == 'abc', 'set by idx fails'
        self.s1.setComponentByPosition(0, self.s1[0].clone('cba'))
        assert self.s1[0] == 'cba', 'set by idx fails'

class Set(unittest.TestCase):
    def setUp(self):
        self.s1 = univ.Set(componentType=namedtype.NamedTypes(
            namedtype.NamedType('name', univ.OctetString()),
            namedtype.OptionalNamedType('null', univ.Null()),
            namedtype.DefaultedNamedType('age', univ.Integer(34))
            ))
        self.s2 = self.s1.clone()
    def testTag(self):
        assert self.s1.getTagSet() == tag.TagSet(
            (),
            tag.Tag(tag.tagClassUniversal, tag.tagFormatConstructed, 0x11)
            ), 'wrong tagSet'
    def testByTypeWithPythonValue(self):
        self.s1.setComponentByType(univ.OctetString.tagSet, 'abc')
        assert self.s1.getComponentByType(
            univ.OctetString.tagSet
            ) == 'abc', 'set by name fails'
    def testByTypeWithInstance(self):
        self.s1.setComponentByType(univ.OctetString.tagSet, univ.OctetString('abc'))
        assert self.s1.getComponentByType(
            univ.OctetString.tagSet
            ) == 'abc', 'set by name fails'
    def testGetTypeMap(self):
        assert self.s1.getTypeMap() == {
            univ.Set.tagSet: univ.Set()
            }
    def testGetComponentTypeMap(self):
        assert self.s1.getComponentTypeMap() == {
            univ.OctetString.tagSet: univ.OctetString(),
            univ.Null.tagSet: univ.Null(),
            univ.Integer.tagSet: univ.Integer(34)
            }
    def testGetPositionByType(self):
        assert self.s1.getComponentPositionByType(
            univ.Null().getTagSet()
            ) == 1

class Choice(unittest.TestCase):
    def setUp(self):
        innerComp = univ.Choice(componentType=namedtype.NamedTypes(
            namedtype.NamedType('count', univ.Integer()),
            namedtype.NamedType('flag', univ.Boolean())
            ))
        self.s1 = univ.Choice(componentType=namedtype.NamedTypes(
            namedtype.NamedType('name', univ.OctetString()),
            namedtype.NamedType('sex', innerComp)
            ))
    def testTag(self):
        assert self.s1.getTagSet() == tag.TagSet(), 'wrong tagSet'
    def testOuterByTypeWithPythonValue(self):
        self.s1.setComponentByType(univ.OctetString.tagSet, 'abc')
        assert self.s1.getComponentByType(
            univ.OctetString.tagSet
            ) == 'abc'
    def testOuterByTypeWithInstanceValue(self):
        self.s1.setComponentByType(
            univ.OctetString.tagSet, univ.OctetString('abc')
            )
        assert self.s1.getComponentByType(
            univ.OctetString.tagSet
            ) == 'abc'
    def testInnerByTypeWithPythonValue(self):
        self.s1.setComponentByType(univ.Integer.tagSet, 123, 1)
        assert self.s1.getComponentByType(
            univ.Integer.tagSet, 1
            ) == 123
    def testInnerByTypeWithInstanceValue(self):
        self.s1.setComponentByType(
            univ.Integer.tagSet, univ.Integer(123), 1
            )
        assert self.s1.getComponentByType(
            univ.Integer.tagSet, 1
            ) == 123
    def testCmp(self):
        self.s1.setComponentByName('name', univ.OctetString('abc'))
        assert self.s1 == 'abc', '__cmp__() fails'
    def testGetComponent(self):
        self.s1.setComponentByType(univ.OctetString.tagSet, 'abc')
        assert self.s1.getComponent() == 'abc', 'getComponent() fails'
    def testSetComponentByPosition(self):
        self.s1.setComponentByPosition(0, univ.OctetString('Jim'))
        assert self.s1 == 'Jim'
    def testClone(self):
        self.s1.setComponentByPosition(0, univ.OctetString('abc'))
        s = self.s1.clone()
        assert len(s) == 0
        s = self.s1.clone(cloneValueFlag=1)
        assert len(s) == 1
        assert s.getComponentByPosition(0) == self.s1.getComponentByPosition(0)
        
if __name__ == '__main__': unittest.main()
