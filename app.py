import hashlib
import json
from time import time
from urllib.parse import urlparse
from uuid import uuid4

import requests
from flask import Flask, jsonify, request

class BlockChain:
    def __init__(self):
        self.transaction_pool = []
        self.chain = []
        self.nodes = set()

        #make genesis block
        #self.block = self.generate_new_block(self, 0, 0, '0AAA')
        self.make_genesis_block()

    def make_genesis_block(self):
        coinbasetransaction = {
            'sender': '0',
            'receiver': 0,
            'amount': 1
        }
        self.transaction_pool.append(coinbasetransaction)
        self.generate_new_block(0, 0, '0AAA')

    def mine_new_block(self, data):
        latest_block = self.get_latestblock()
        self.generate_new_block(latest_block['previoushash'], data, '0AAA')

    def generate_new_block(self, previoushash, data, targetvalue):
        t = time()
        t /= 1000
        block = {
            'index': len(self.chain)+1,
            'previoushash': previoushash,
            'data': data,
            'timestamp': t,
            'hash':'',
            'nonce': 0,
            'transaction_set': self.transaction_pool,
            'merkletree': [],
            'root': '',
            'targetvalue': targetvalue
        }
        block['root'] = self.makemerkletree(block)
        block['nonce']= self.proove_of_work(block)


        self.transaction_pool = []
        self.chain.append(block)
        return block

    def calculateHashForBlock(self, block):#return self.calculateHash(block.index, block.previoushash, block.timestamp, block.data)
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()
    @staticmethod
    def calculateHash(index, previoushash, timestamp, data):
        return hashlib.sha256(index + previoushash + timestamp + data + '')

    def proove_of_work(self, block):
        hashvalue = ''
        while True:
            #hashvalue = hashlib.sha256(block['root'] + block['previoushash'] + block['data'] + block['index'] + block['nonce'] + '') + ''
            hashvalue = self.calculateHashForBlock(block)
            toCompare = hashvalue[0:3]
            if toCompare < block['targetvalue']: break
            block['nonce'] += 1
        return block['nonce']


    def makemerkletree(self, block):
        for tx in block['transaction_set']:
            tx_string = json.dumps(tx, sort_keys=True).encode()
            tx_hash = hashlib.sha256(tx_string).hexdigest()
            block['merkletree'].append(tx_hash)
        index_s = 0
        index_e = len(block['transaction_set'])

        while index_s + 1 != index_e:

            i = index_s
            while i < index_e:
                if i+1 < index_e:
                    tx_hash = hashlib.sha256(block['merkletree'][i].encode() + block['merkletree'][i+1].encode()).hexdigest()
                    block['merkletree'].append(tx_hash)
                else:
                    tx_hash = hashlib.sha256(block['merkletree'][i].encode()).hexdigest()
                    block['merkletree'].append(tx_hash)
                i+=2
            index_s = index_e
            index_e = len(block['merkletree'])

        block['root'] = block['merkletree'][index_s]
        return block['root']

    def get_latestblock(self):
        return self.chain[-1]

    def add_transaction(self,sender, receiver, amount):
        transaction = {
            'sender' : sender,
            'receiver' : receiver,
            'amount' : amount
        }
        self.transaction_pool.append(transaction)

    def get_block_info(self):
        block_info_array = []
        for block in self.chain:
            block_info_json = json.dumps(block, indent=4)
            block_info_array.append(block_info_json)
        return block_info_array

    #def is_valid_block(self):

app = Flask(__name__)


@app.route('/')
def hello_world():
    bc = BlockChain()
    bc.add_transaction('a','b',100)
    bc.add_transaction('b', 'c', 100)
    bc.add_transaction('a', 'c', 100)
    bc.add_transaction('a', 'd', 100)
    print(bc.get_block_info())
    bc.mine_new_block({'name' : 'apple'})
    print(bc.get_block_info())
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
'''
    bc = BlockChain()
    bc.add_transaction('a','b',100)
    bc.add_transaction('b', 'c', 100)
    bc.add_transaction('a', 'c', 100)
    bc.add_transaction('a', 'd', 100)
    print(bc.get_block_info())
    bc.mine_new_block({'name' : 'apple'})
    print(bc.get_block_info())
'''