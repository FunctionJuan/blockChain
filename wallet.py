from Crypto.PublicKey import RSA
import Crypto.Random
import binascii

class Wallet:
    def __init__(self):    
        self.private_key = None
        self.public_key = None

    def create_keys(self):
        private_key, public_key = self.generate_keys()
        self.private_key = private_key
        self.public_key = public_key
     

    def save_keys(self):
           if self.public_key != None and self.private_key != None:
                try:
                    with open('wallet.txt', mode='w') as theFile:
                        theFile.Write(self.public_key)
                        theFile.write('\n')
                        theFile.write(self.private_key)
                except(IOError, IndexError):
                    print('Saving Wallet failed!!!!')

    def load_keys(self):
        try:
            with open('wallet.txt', mode='r') as theFile:
                keys = theFile.readlines()
                public_key = keys[0][:-1]
                private_key = keys[1]
                self.public_key = public_key
                self.private_key = private_key
        except(IOError,IndexError):
            print('Loading Wallet failed....')

    def generate_keys(self):
        private_key = RSA.generate(1024, Crypto.Random.new().read)
        public_key = private_key.publickey()
        return(binascii.hex(private_key.exportKey(format='DER')).decode('ascii'),binascii.hex(public_key.exportKey(format='DER')).decode('ascii'))

