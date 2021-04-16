import json
import hashlib as aliasHash


def hash_the_string_256(string):
    """Create a SHA256 hash for a given input string.

    Arguments:
        :string: The string which should be hashed.
    """
    return aliasHash.sha256(string).hexdigest()

def hashed_block_def(block):
    """Hashes a block and returns a string representation of it.

    Arguments:
        :block: The block that should be hashed.
    """
    
    # print('What the hashed_block DEF Retunrs: ', '-'.join([str(block[key]) for key in block]) )
    #print('What the hashed_block DEF Retunrs: ', aliasHash.sha256(json.dumps(hashable_blockConverted).encode()).hexdigest() )
    hashable_blockConvert = block.__dict__.copy()
    hashable_blockConvert['transactions'] = [tx.to_order_dict() for tx in hashable_blockConvert['transactions']]
    return hash_the_string_256(json.dumps(hashable_blockConvert, sort_keys=True).encode())