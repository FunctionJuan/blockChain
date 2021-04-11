from blockchain import BlockCHAIN
from uuid import uuid4
from utiles.verification import Verification
from wallet import Wallet
class Node:
    def __init__(self):
        #self.wallet.public_key = str(uuid4())
        self.wallet = Wallet()
        self.wallet.create_keys()
        self.blockchain = BlockCHAIN(self.wallet.public_key)

    def get_transaction_value(self):
        """ Returns the input of the user (a new transaction amount) as a float. """
        # Get the user input, transform it from a string to a float and store it in user_input
        tx_recipient = input('Enter The Recipient of the Transaction : ')
        tx_amount = float(input('Your Transaction Amount Please : '))
    
        #to return our Tuple:
        #NOte with 2 arguments you could omit the parenthesis and if it where one to create the Tuple you have to do parenthesis and comma and empty space to generate the tuple
        return tx_recipient, tx_amount

    def get_user_choice(self):
        """Prompts the user for its choice and return it."""
        user_input  = input('Your Choice please: ')
        return user_input

    def print_blockchain_elements(self):
        """ Output all blocks of the blockchain """
        for blocki in self.blockchain.chain:
            print('Outputiting Block')
            print(blocki)
        else:
            print('-' * 80)   
    def listen_for_input_here(self):  
        waiting_for_input = True
    
        while waiting_for_input:
            print('Please Choose : ')
            print(' 1: Add a new Transaction Value ')
            print(' 2: Mine a NEW block')
            print(' 3: Output the blockchain Values...')
            print(' 4: Check TransactionValidity..')
            print(' 5: Create a WALLET')
            print(' 6: Load Wallet' )
            print(' 7: Save Keys' )
            print(' h: Manipulate your chain')
            print(' Q: Quit!!! & Output the blockchain Values...')
            user_choice = self.get_user_choice()
            if user_choice == '1':
                #tx_data is a tuple as to what get_transaction_value returns
                tx_data = self.get_transaction_value()
                #Using a tuple unpacker the only way to unpack this data at this point:
                recipient, amount = tx_data            
                if self.blockchain.add_transaction(recipient, self.wallet.public_key, amount=amount):
                    print('Transaction Added Succesfully!! ')
                else:
                    print('Transaction has failed!!')
                    print('printing the open transactions: ')
                    #print(self.blockchain.get_open_trans())
            elif user_choice == '2':
                if not self.blockchain.mine_block():
                    print ('Mining Failed Dude. No Wallet for you ??')
            elif user_choice == '3':
                self.print_blockchain_elements()
            elif user_choice == '4':               
                if Verification.verify_transaction_validity(self.blockchain.open_transactions, self.blockchain.get_balance):
                    print('All transactions ARE VALID!!')
                else:
                    print('There are Invalid transactions!!')     
            elif user_choice == 5:
                 self.wallet.create_keys()
                 self.blockchain = BlockCHAIN(self.wallet.public_key)
            elif user_choice == 6:
                 self.wallet.load_keys() 
                 self.blockchain = BlockCHAIN(self.wallet.public_key)          
            elif user_choice == 7:
                 self.wallet.save_keys()     
            elif user_choice == 'Q':
                waiting_for_input = False  
            else:
                print('Input is Invalid Enter one of the other choices')
        
            if not Verification.verify_the_blockChain(self.blockchain.chain):        
                self.print_blockchain_elements()
                print('Invalid BlockChain!!!! ')
                #waiting_for_input = False  
                #break out of the loop
                break      
            print('Choice Registered')     
            print('Balance of {}: {:6.2f}'.format(self.wallet.public_key, self.blockchain.get_balance())) 
        else:
            print('User Left')    

    
# Output the blockchain list to the console
   

            print('Done!!!')

if __name__ == '__main__':
    node = Node()
    node.listen_for_input_here()