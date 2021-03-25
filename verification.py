from hash_util import hashed_block_def, hash_the_string_256

class Verification:
    @staticmethod
    def valid_proof(transactions,last_hash, proof):
        """Validate a proof of work number and see if it solves the puzzle algorithm (two leading 0s)

        Arguments:
            :transactions: The transactions of the block for which the proof is created.
            :last_hash: The previous block's hash which will be stored in the current block.
            :proof: The proof number we're testing.
        """
        guess = (str([tx.to_order_dict() for tx in transactions]) + str(last_hash) + str(proof)).encode()
        guess_hash = hash_the_string_256(guess)
        print('This is the GUESS HASH on valid Proof',guess_hash)
        return guess_hash[0:2] == '00'

    @classmethod
    def verify_the_blockChain(cls, blockchain):
        """ Verify the current blockchain and return True if it's valid"""
        #With the Helper function we will get our Tuple back so we use our unpacking
        for (index,block) in enumerate(blockchain):
            if index == 0:
                continue
            if block.previous_hash != hashed_block_def(blockchain[index -1]):
                return False
            if not cls.valid_proof(block.transactions[:-1], block.previous_hash, block.proof):
             print('PROOOF of work IS INVALID')
            return False    
        return True  
    @staticmethod
    def verify_transaction(transaction, get_balance):
        """Verify a transaction by checking whether the sender has sufficient coins.

        Arguments:
            :transaction: The transaction that should be verified.
        """
        sender_balance = get_balance()
        #will return of course wether true or false
        return sender_balance >= transaction.amount
  
    @classmethod
    def verify_transaction_validity(cls, open_transactions, get_balance):
        """Verifies all open transactions."""
        return all([cls.verify_transaction(tx, get_balance) for tx in open_transactions])