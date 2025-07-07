# blockchain.py
import hashlib
from datetime import datetime

class Block:
    def __init__(self, index, timestamp, transactions, previous_hash, difficulty=2):
        self.index = index
        self.timestamp = timestamp
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = 0
        self.difficulty = difficulty
        self.hash = self.mine_block()

    def compute_hash(self):
        block_string = str(self.index) + self.timestamp + str(self.transactions) + self.previous_hash + str(self.nonce)
        return hashlib.sha256(block_string.encode()).hexdigest()

    def mine_block(self):
        target = '0' * self.difficulty
        while True:
            if self.compute_hash()[:self.difficulty] == target:
                return self.compute_hash()
            self.nonce += 1

class Blockchain:
    def __init__(self):
        self.chain = []
        self.unconfirmed_transactions = []
        self.balances = {"Alice": 100, "Bob": 100, "Charlie": 100}
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis = Block(0, str(datetime.utcnow()), "Genesis Block", "0")
        self.chain.append(genesis)

    def add_transaction(self, sender, receiver, amount):
        amount = float(amount)
        if self.balances.get(sender, 0) < amount:
            return False
        self.unconfirmed_transactions.append({
            "sender": sender,
            "receiver": receiver,
            "amount": amount
        })
        return True

    def mine(self):
        if not self.unconfirmed_transactions:
            return None
        last_block = self.chain[-1]
        new_block = Block(len(self.chain), str(datetime.utcnow()),
                          self.unconfirmed_transactions, last_block.hash)
        self.chain.append(new_block)
        for txn in self.unconfirmed_transactions:
            self.balances[txn['sender']] -= txn['amount']
            self.balances[txn['receiver']] += txn['amount']
        self.unconfirmed_transactions = []
        return new_block
