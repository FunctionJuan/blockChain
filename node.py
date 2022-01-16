#from crypt import methods
from urllib import response
from flask import Flask, jsonify,request, send_from_directory
from flask_cors import CORS
from wallet import Wallet   
from blockchain import BlockCHAIN

aplicacion = Flask(__name__)
wallet = Wallet()
blockchain = BlockCHAIN(wallet.public_key) 
CORS(aplicacion)


@aplicacion.route('/', methods=['GET'])
def get_node_ui():
    return send_from_directory('ui', 'node.html')

@aplicacion.route('/network', methods=['GET'])
def get_network_ui():
    return send_from_directory('ui', 'network.html')

@aplicacion.route('/wallet', methods=['POST'])
def create_keys():
    wallet.create_keys()
    if wallet.save_keys():       
        global blockchain
        blockchain = BlockCHAIN(wallet.public_key) 
        response= {
            'public_key': wallet.public_key,
            'private_key': wallet.private_key,
            'funds': blockchain.get_balance()
        }
        return jsonify(response), 201
    else:
        response = {
          'message': 'Saving the Keys failed'
        }
        return jsonify(response), 500

@aplicacion.route('/wallet', methods=['GET'])
def load_keys():
    if wallet.load_keys():
        global blockchain
        blockchain = BlockCHAIN(wallet.public_key) 
        response= {
            'public_key': wallet.public_key,
            'private_key': wallet.private_key,
            'funds': blockchain.get_balance()
        }
        return jsonify(response), 201
    else:
        response = {
          'message': 'Loading the Keys failed'
        }
        return jsonify(response), 500

@aplicacion.route('/balance', methods=['GET'])
def get_balance():
    balance = blockchain.get_balance()
    if balance != None:
       response = {
           'message': 'Fetched Balance successfully',
           'funds': balance
       }
       return jsonify(response), 200
    else:
        response = {
            'message': 'Loading balance failed',
            'wallet_set_up': wallet.public_key != None
        }
        return jsonify(response), 500

@aplicacion.route('/transaction', methods=['POST'])
def add_transaction():
    if wallet.public_key == None:
        response = {
            'message': 'No WALLET SET UP'
        }
        return jsonify(response), 400
    values = request.get_json()
    if not values:
        response = {
            'message': 'NO DATA FOUND'
        }
        return jsonify(response), 400
    required_fields = ['recipient', 'amount']
    if not all(field in values for field in required_fields):
        response = {
             'message': 'Required Data is MISSING'   
        } 
        return  jsonify(response), 400
    recipient = values['recipient']#and this is a dictionary
    amount = values['amount']
    signature = wallet.sign_transaction(wallet.public_key,recipient, amount)
    #Now We should have all the data We need to create a new transaction
    success = blockchain.add_transaction(recipient, wallet.public_key, signature, amount)
    if success:
        response = {
            'message': 'Transaction succefully added',
            'transaction':{
                'sender': wallet.public_key,
                'recipient': recipient,
                'amount': amount,
                'signature': signature
            },
            'funds': blockchain.get_balance()
        }
        return jsonify(response), 201
    else:
        response = {
            'message': 'Creating a transaction FAILED!!!!!!!!!!!!!!!!!'
        }
        return jsonify(response), 500
@aplicacion.route('/minar', methods=['POST'])
def mineTheMine():
    block = blockchain.mine_block()    
    if block != None:
        dict_block = block.__dict__.copy()
        dict_block['transactions'] = [tx.__dict__ for tx in dict_block['transactions']]
        response = {
            'message': 'Block Added Successfully',
            'block': dict_block,
            'funds': blockchain.get_balance()
        }
        return jsonify(response), 201
    else:
        response = {
            'message': 'Adding a Block has failed',
            'wallet_set_up': wallet.public_key != None
        }
        return jsonify(response), 500

@aplicacion.route('/transactions', methods=['GET'])
def opened_trasactions():
    transactions = blockchain.get_open_trans()
    dict_transactions = [tx.__dict__ for tx in transactions]
    return jsonify(dict_transactions), 200
    """ response = {
        'message': 'Fetched transaction succesfully.',
        'transactions': dict_transactions
    } """

@aplicacion.route('/returnChain', methods=['GET'])
def get_chain():
    chain_snapshot = blockchain.chain    
    dictionaryChain = [block.__dict__.copy() for block in chain_snapshot]
    for dict_block in dictionaryChain:
        dict_block['transactions'] = [tx.__dict__ for tx in dict_block['transactions']]
    return jsonify(dictionaryChain), 200

@aplicacion.route('/nodo', methods=['POST'])
def add_node():
    values = request.get_json()
    if not values:
        response = {
            'message' : 'No Data Attached'
        }
        return jsonify(response), 400
    if 'node' not in values:
        response = {
            'message' : 'No node data found'
        }
        return jsonify(response), 400
    node = values.get('node')
    blockchain.add_peer_node(node)
    response =  {
            'message' : 'Node added succesfully',
            'all_nodes' : blockchain.get_peer_nodes()
        }
    return jsonify(response), 201  

#remember for DELETE better to encode this as URI parameter you mark it down in flask as: <>
@aplicacion.route('/nodo/<node_uri>', methods=['DELETE'])
def remove_node(node_uri):
    if node_uri == '' or node_uri == None:
        response = {
            'message': 'no node found.'
        }
        return jsonify(response), 400
    blockchain.remove_peer_nodes(node_uri)
    response = {
        'message': 'Noded removed',
        'all_nodes': blockchain.get_peer_nodes()
        }
    return jsonify(response), 200

@aplicacion.route('/returnNodes', methods=['GET'])
def get_nodes():
    nodes= blockchain.get_peer_nodes()
    response = {
        'all_nodes': nodes
    }
    return jsonify(response), 200

if __name__ == '__main__':
    aplicacion.run(host= '0.0.0.0', port=7000)
