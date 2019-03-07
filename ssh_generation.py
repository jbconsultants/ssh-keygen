#!/usr/bin/python

'''
  Version 1.0
    Create SSH private/public key pair
  Version 1.1
    Converted public key generation to utilize cryptography
'''

__author__  = "Jason Brown"
__email__   = 'jason@jbconsultants.llc'
__version__ = '1.1'
__status__  = 'Production'
__date__    = '20190215'

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
import getpass, os


def main():
    keyname = raw_input("Name of Key: ")
    passwd_in = getpass.getpass("Password: ") 

    '''
      Generate ECDSA 521 bit private key and write it to stdout
    '''
    priv_key = ec.generate_private_key(ec.SECP521R1(), default_backend())

    with open(keyname, "w") as privkey:
    	privkey.write(priv_key.private_bytes(
    		encoding=serialization.Encoding.PEM,
    		format=serialization.PrivateFormat.TraditionalOpenSSL,
    		encryption_algorithm=serialization.BestAvailableEncryption(passwd_in)
    	))

    '''
      Extract SSH public key from private key     
    '''
    with open(keyname + ".pub", "w") as pubkey:
        pubkey.write(priv_key.public_key().public_bytes(
            encoding=serialization.Encoding.OpenSSH,
            format=serialization.PublicFormat.OpenSSH
        ))


    os.chmod(keyname, 0o400)

if __name__ == '__main__':
	main()
