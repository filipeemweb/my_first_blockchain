#============================================#
# >>>>> Module 1 - Create a Blockchain <<<<< #
#============================================#

import datetime
import hashlib
import json
from flask import Flask, jsonify

#######################################################################################

#--------------------------------#
# Part 1 - Building a Blockchain #
#--------------------------------#

class Blockchain:
    
    def __init__(self):
        self.challenge = '0000'
        self.chain = []
        
        # Create the genesis block
        genesis_block = self.create_block(proof = 1, previous_hash = '0000')
        self.add_new_block(genesis_block)
    
    #=====================================================
    
    def hash_block(self, block):
        # Encodes a JSON formatted block into string
        encoded_block = json.dumps(block, sort_keys=True).encode()
        
        # Gets the hex hash from the encoded_block
        return hashlib.sha256(encoded_block).hexdigest()
    
    #=====================================================
    
    def check_challenge(self, hash_operation):
        # Check if the hash pass the challenge
        return hash_operation[:len(self.challenge)] == self.challenge
    
    #=====================================================
        
    def create_block(self, proof, previous_hash):
        
        # A general purpose block, without data
        block = {'index': len(self.chain) + 1, 
                 'timestamp': str(datetime.datetime.now()), 
                 'proof': proof,
                 'previous_hash': previous_hash}
        
        return block
    
    #=====================================================
        
    def add_new_block(self, new_block):
        # Add the newly created block to the end of the chain
        self.chain.append(new_block)
    
    #=====================================================
    
    def get_previous_block(self):
        return self.chain[-1]
    
    #=====================================================
    
    # Create a challenge that is hard to find, but easy to verify
    def proof_of_work(self, previous_block):
        nonce = 1
        check_proof = False
        
        # Hashes the previous_block
        previous_hash = self.hash_block(previous_block)
        
        #  Creates a new block
        new_block = self.create_block(nonce, previous_hash)
        
        while check_proof is False:
            
            new_block['proof'] = nonce
            
            hash_operation = self.hash_block(new_block)
            
            if self.check_challenge(hash_operation) is True:
                check_proof = True
                
            # If hash fails the challenge, increases new_proof by 1 to try again by brute force
            else:
                nonce += 1
                
        return new_block
    
    #=====================================================
    
    def is_chain_valid(self, chain):
        # Initialing with the first block
        previous_block = chain[0]
        
        for current_block in chain: 
            hash_operation = self.hash_block(current_block)

            if current_block['index'] == 1:
                continue
            
            if current_block['previous_hash'] != self.hash_block(previous_block):
                return False
            
            if self.check_challenge(hash_operation) is False:
                return False
            
            previous_block = current_block
            
        return True
            
    
#######################################################################################       

#--------------------------------#
# Part 2 - Mining our Blockchain #
#--------------------------------#

# Creating a Web App
app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

# Create a Blockchain
blockchain = Blockchain()

# Mining a new block
@app.route('/blockchain/mine', methods = ['GET'])
def mine_block():
    # Get the previous block
    previous_block = blockchain.get_previous_block()
    
    # Gets the new block with a correct proof
    new_block = blockchain.proof_of_work(previous_block)
    
    # Adds the new block to the chain
    blockchain.add_new_block(new_block)
    
    response = {'message': 'Congratulations, you just mined a block!', 'block': new_block}
    
    return jsonify(response), 200

# Getting the full Blockchain
@app.route('/blockchain', methods = ['GET'])
def get_chain():
    response = {'chain': blockchain.chain, 'length': len(blockchain.chain)}
    
    return jsonify(response), 200

# Validating Blockchain
@app.route('/blockchain/validate', methods = ['GET'])
def validate_chain():
    is_chain_valid = blockchain.is_chain_valid(blockchain.chain)

    response = {'chain': blockchain.chain, 'length': len(blockchain.chain), 'is_valid': is_chain_valid}
    
    return jsonify(response), 200


# Running the app
app.run(host = '0.0.0.0', port = 5000)