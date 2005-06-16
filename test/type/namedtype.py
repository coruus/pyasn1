from pyasn1.type import namedtype, univ
from pyasn1.error import PyAsn1Error
try:
    import unittest
except ImportError:
    raise PyAsn1Error(
        'PyUnit package\'s missing. See http://pyunit.sourceforge.net/'
        )

class NamedTypeCaseBase(unittest.TestCase):
    def setUp(self):
        self.e = namedtype.NamedType('age', univ.Integer())
    def testIter(self):
        n, t = self.e
        assert n == 'age' or t == univ.Integer(), 'unpack fails'

class NamedTypesCaseBase(unittest.TestCase):
    def setUp(self):
        self.e = namedtype.NamedTypes(
            namedtype.NamedType('first-name', univ.OctetString()),
            namedtype.OptionalNamedType('age', univ.Integer()),
            namedtype.NamedType('family-name', univ.OctetString())
            )
    def testIter(self):
        for t in self.e:
            break
        else:
            assert 0, '__getitem__() fails'
            
    def testGetTypeByPosition(self):
        assert self.e.getTypeByPosition(0) == univ.OctetString(), \
               'getTypeByPosition() fails'

    def testGetNameByPosition(self):
        assert self.e.getNameByPosition(0) == 'first-name', \
               'getNameByPosition() fails'

    def testGetPositionByName(self):
        assert self.e.getPositionByName('first-name') == 0, \
               'getPositionByName() fails'

    def testGetTypesNearPosition(self):
        assert self.e.getTypeMapNearPosition(0) == {
            univ.OctetString.tagSet: univ.OctetString()
            }
        assert self.e.getTypeMapNearPosition(1) == {
            univ.Integer.tagSet: univ.Integer(),
            univ.OctetString.tagSet: univ.OctetString()
            }
        assert self.e.getTypeMapNearPosition(2) == {
            univ.OctetString.tagSet: univ.OctetString()
            }

    def testGetTypeMap(self):
        assert self.e.getTypeMap() == {
            univ.OctetString.tagSet: univ.OctetString(),
            univ.Integer.tagSet: univ.Integer()
            }

    def testGetTypeMapWithDups(self):
        try:
            self.e.getTypeMap(1)
        except PyAsn1Error:
            pass
        else:
            assert 0, 'Duped types not noticed'
        
    def testGetPositionNearType(self):
        assert self.e.getPositionNearType(univ.OctetString.tagSet, 0) == 0
        assert self.e.getPositionNearType(univ.Integer.tagSet, 1) == 1
        assert self.e.getPositionNearType(univ.OctetString.tagSet, 2) == 2

class OrderedNamedTypesCaseBase(unittest.TestCase):
    def setUp(self):
        self.e = namedtype.NamedTypes(
            namedtype.NamedType('first-name', univ.OctetString()),
            namedtype.NamedType('age', univ.Integer())
            )
            
    def testGetTypeByPosition(self):
        assert self.e.getTypeByPosition(0) == univ.OctetString(), \
               'getTypeByPosition() fails'

if __name__ == '__main__': unittest.main()
