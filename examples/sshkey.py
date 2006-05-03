# Read unencrypted PKCS#1/PKIX-compliant, PEM&DER encoded private keys on
# stdin, print them pretty and encode back into original wire format.
# Private keys can be generated with "openssl genrsa|gendsa" commands.
import sys, string, base64
from pyasn1.type import univ, namedtype, namedval, constraint
from pyasn1.codec.der import encoder, decoder

class DSAPrivateKey(univ.Sequence):
    """PKIX compliant DSA private key structure"""
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('version', univ.Integer(namedValues=namedval.NamedValues(('v1', 0)))),
        namedtype.NamedType('p', univ.Integer()),
        namedtype.NamedType('q', univ.Integer()),
        namedtype.NamedType('g', univ.Integer()),
        namedtype.NamedType('public', univ.Integer()),
        namedtype.NamedType('private', univ.Integer())
        )

MAX = 16

class OtherPrimeInfo(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('prime', univ.Integer()),
        namedtype.NamedType('exponent', univ.Integer()),
        namedtype.NamedType('coefficient', univ.Integer())
        )
    
class OtherPrimeInfos(univ.SequenceOf):
    componentType = OtherPrimeInfo()
    subtypeSpec = univ.SequenceOf.subtypeSpec + \
                  constraint.ValueSizeConstraint(1, MAX)
    
class RSAPrivateKey(univ.Sequence):
    """PKCS#1 compliant RSA private key structure"""
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('version', univ.Integer(namedValues=namedval.NamedValues(('two-prime', 0), ('multi', 1)))),
        namedtype.NamedType('modulus', univ.Integer()),
        namedtype.NamedType('publicExponent', univ.Integer()),
        namedtype.NamedType('privateExponent', univ.Integer()),
        namedtype.NamedType('prime1', univ.Integer()),
        namedtype.NamedType('prime2', univ.Integer()),
        namedtype.NamedType('exponent1', univ.Integer()),
        namedtype.NamedType('exponent2', univ.Integer()),
        namedtype.NamedType('coefficient', univ.Integer()),
        namedtype.OptionalNamedType('otherPrimeInfos', OtherPrimeInfos())
        )
    
keyMagic = {
    '-----BEGIN DSA PRIVATE KEY-----':
    {'-----END DSA PRIVATE KEY-----': DSAPrivateKey() },
    '-----BEGIN RSA PRIVATE KEY-----':
    {'-----END RSA PRIVATE KEY-----': RSAPrivateKey() }
    }

# Read PEM keys from stdin and print them out in plain text

stSpam, stHam, stDump = 0, 1, 2
state = stSpam
keyCnt = 0

for keyLine in sys.stdin.readlines():
    keyLine = string.strip(keyLine)
    if state == stSpam:
        if state == stSpam:
            if keyMagic.has_key(keyLine):
                keyMagicTail = keyMagic[keyLine]
                keyLines = []
                state = stHam
                continue
    if state == stHam:
        if keyMagicTail.has_key(keyLine):
            asn1Spec = keyMagicTail[keyLine]
            state = stDump
        else:
            keyLines.append(keyLine)
    if state == stDump:
        substrate = ''
        try:
            for keyLine in keyLines:
                substrate = substrate + base64.decodestring(keyLine)
        except TypeError, why:
            print '%s, possibly encrypted key' % (why, )
            state = stSpam
            continue

        key = decoder.decode(substrate, asn1Spec=asn1Spec)[0]
        
        print key.prettyPrint()
        
        if encoder.encode(key) != substrate:
            print 'key re-code yields a diff!'
        
        keyCnt = keyCnt + 1
        state = stSpam

print '*** %s private key(s) re/serialized' % keyCnt
