from functools import reduce
import hashlib as aliasHash
import json
import pickle
# Import two functions from our hash_util.py file. Omit the ".py" in the import
from utiles.hash_util import hashed_block_def
from utiles.verification import Verification
from blockFile import BlockClass
from transaction import Transaction
from wallet import Wallet
#CONSTANT:
MINING_REWARD = 8

print(__name__)

class BlockCHAIN:
    def __init__(self, hosting_node_id):
        #Our Starting blokc for the blockchain
        genesis_block = BlockClass(0,'',[],100,0)
        #To initialize the empty blockchain
        self.chain = [genesis_block]
        #Unhandled Transactions
        self.__open_transactions = []           
        self.hosting_node = hosting_node_id
        self.__peer_nodes = set()#this would just initialize a set
        self.load_data()    

    @property
    def chain(self):
        return self.__chain[:]

    @chain.setter
    def chain(self, val):
        self.__chain = val
    

    def get_open_trans(self):
        return self.__open_transactions[:]    

    def load_data(self):
    
        try:
            with open('***********************************', mode='r') as fileVariable:
                file_content =  fileVariable.readlines()
                #file_content = pickle.loads(fileVariable.read()) 
                # blockchain = file_content['chain']
                # open_transactions = file_content['ot']
                blockchain = json.loads(file_content[0][:-1])
                updated_blockchain = []            
                for block in blockchain:
                    convertedTXVar = [Transaction(tx['sender'], tx['recipient'],tx['signature'],tx['amount']) for tx in block['transactions']]                
                    updated_block = BlockClass(block['index'],block['previous_hash'],convertedTXVar, block['proof'], block['timestamp'])                
                    updated_blockchain.append(updated_block)         
                self.chain = updated_blockchain    
                open_transactions= json.loads(file_content[1])[:-1]
                # We need to convert  the loaded data because Transactions should use OrderedDict
                updated_transactions = []
                for tx in open_transactions:
                    updated_transaction = Transaction(tx['sender'], tx['recipient'],tx['signature'],tx['amount'])
                    updated_transactions.append(updated_transaction)
                self.__open_transactions = updated_transactions  
                peer_nodes=json.loads(file_content[2])
                self.peer_nodes = set(peer_nodes)
        except (IOError, IndexError):           
            pass  
         #print('Handled EXCEPTION')
        finally:
            print('CLEANUP!!!')             

    def save_data(self):
        try:
            with open('\\**********************', mode='w') as fileVariable:
                saveable_chain = [block.__dict__ for block in [BlockClass(block_el.index, block_el.previous_hash, [tx.__dict__ for tx in block_el.transactions],block_el.proof, block_el.timestamp) for block_el in self.__chain]]
                print('THIS SHOULD BE SAVEABLE', saveable_chain)
                fileVariable.write(json.dumps(saveable_chain))
                fileVariable.write('\n')
                saveable_TX = [tx.__dict__ for tx in self.__open_transactions]
                fileVariable.write(json.dumps(saveable_TX))
                fileVariable.write('\n')
                fileVariable.write(json.dumps(list(self.__peer_nodes)))
                # save_data = {
                #     'chain': blockchain,
                #     'ot': open_transactions
                # }
                # fileVariable.write(pickle.dumps(save_data))            
        except IOError:
            print('Saving FAILED!!!!')

    def proof_of_work(self):
        """Generate a proof of work for the open transactions, the hash of the previous block and a random number (which is guessed until it fits)."""
        last_block = self.__chain[-1]
        last_hash = hashed_block_def(last_block)
        proof = 0
     
        while not Verification.valid_proof(self.__open_transactions,last_hash, proof):
            proof += 1
        return proof      


    def get_balance(self):
        """Calculate and return the balance for a participant.
        """
        if self.hosting_node == None:
            return None
        participant = self.hosting_node
        tx_sender = [[tx.amount for tx in block.transactions if tx.sender == participant] for block in self.__chain]
        open_tx_sender = [tx.amount for tx in self.__open_transactions if tx.sender == participant]
        tx_sender.append(open_tx_sender)
        print('FIX BUG for TX_ SENDER: ', tx_sender)
        amount_sent = reduce(lambda tx_sum,tx_amt: tx_sum + sum(tx_amt)if len(tx_amt) > 0 else tx_sum + 0,tx_sender,0)        
        # This fetches received coin amounts of transactions that were already included in blocks of the blockchain
        # We ignore open transactions here because you shouldn't be able to spend coins before the transaction was confirmed + included in a block
        tx_recipient = [[tx.amount for tx in block.transactions if tx.recipient == participant] for block in self.__chain]
        amount_received = reduce(lambda tx_sum,tx_amt: tx_sum + sum(tx_amt)if len(tx_amt) > 0 else tx_sum  + 0,tx_recipient,0)
        
        print('Amount Received : ' , amount_received)
        print('Amount Sent : ' , amount_sent)                 
        return amount_received - amount_sent
        
    def get_last_blockchain_value(self):
        """ Returns the last value of the current blockchain. """
        if len(self.__chain) <1:
            return None 
        return self.__chain[-1]

# This function accepts two arguments.
# One required one (transaction_amount) and one optional one (last_transaction)
# The optional one is optional because it has a default value => [1]
    def add_transaction(self,recipient, sender, signature, amount=1.0):
        """ Append a new value as well as the last blockchain value to the blockchain.
        
        Arguments:
            :sender: The Sender of the coins
            :recepient: The Recepient of the coins
            :amount: The Amount of coins sent with the transaction (default = 1.0)
        """
        #remmeber this is dictionary it opens with {} and it is taking the argument form your function
        # transaction = {
        #        'sender': sender, 
        #        'recipient': recipient, 
        #        'amount': amount
        #     } 
        #
        if self.hosting_node == None:
            return False
        transaction = Transaction(sender,recipient,signature, amount)               
        if  Verification.verify_transaction(transaction, self.get_balance):
            self.__open_transactions.append(transaction)
            """   participantes.add(sender)
            participantes.add(recipient) """
            print('This Is How OPENTRASLOOKAFTER appending: ', self.__open_transactions)
            self.save_data()
            return True
        return False
    
   # blockchain.append([last_transaction, transaction_amount])

    def mine_block(self):
        """Create a new block and add open transactions to it."""
        #add a dictionary with a previous hash key
        if self.hosting_node == None:
            return None
        last_block = self.__chain[-1]
        print('This is the BlockChain as a WHULE', self.__chain)    
        print('AND This is the last_block Or how We are calling it last_block Variable', last_block)       
        hashed_block = hashed_block_def(last_block)
        #print('This Right Here is your HASHED BLOCK Result We SenT TO DEF We Got it back', hashed_block) 
        proof = self.proof_of_work()
        # reward_transaction = {
        #     'sender': 'MINING',
        #     'recipient': owner,
        #     'amount': MINING_REWARD
        # } 
        reward_transaction = Transaction('MINING', self.hosting_node,'', MINING_REWARD)
        copied_transactions = self.__open_transactions [:]
        for tx in copied_transactions:
           if not Wallet.verify_transaction(tx):
               return None 
        copied_transactions.append(reward_transaction)
        block = BlockClass(len(self.__chain), hashed_block, copied_transactions, proof)
       
        print('THIS IS Copied Transactions ', copied_transactions)
        print('THIS IS OPEEEN Transactions ', self.__open_transactions)
        print('THIS IS THE BLOCK TO APPEND To The BLOCKCHAIN: ', block) 
        self.__chain.append(block)
        print('AND this is the BLOCKCHAIN AFTER ALL APPEND', self.__chain)
        self.__open_transactions = []
        self.save_data()
        return block

    def add_peer_node(self, node):
        """Adds a new node the peer node set
        
        Arguments: 
            :node: The node URL which should be added"""

        self.__peer_nodes.add(node)
        self.save_data()



    def remove_peer_nodes(self, node):
        """Removes a node the peer node set
        
        Arguments: 
            :node: The node URL which should be added"""

        self.__peer_nodes.discard(node)
        self.save_data()
    

    def get_peer_nodes(self):
        """Return a list of all connected peer nodes"""
        return list(self.__peer_nodes)