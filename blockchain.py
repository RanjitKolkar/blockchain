# blockchain.py

import hashlib
from datetime import datetime
import json

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
        block_data = {
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": self.transactions,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }
        block_string = json.dumps(block_data, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

    def mine_block(self):
        target = '0' * self.difficulty
        while True:
            computed_hash = self.compute_hash()
            if computed_hash[:self.difficulty] == target:
                return computed_hash
            self.nonce += 1


class Blockchain:
    def __init__(self):
        self.chain = []
        self.unconfirmed_transactions = []
        self.balances = {"Ravi": 100, "Priya": 100, "Anil": 100}
        self.transaction_fee = 1.0  # Fixed fee per transaction (₹1)

        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(
            index=0,
            timestamp=datetime.utcnow().isoformat(),
            transactions="Genesis Block",
            previous_hash="0"
        )
        self.chain.append(genesis_block)

    def add_transaction(self, sender, receiver, amount):
        amount = float(amount)
        total_cost = amount + self.transaction_fee
        if self.balances.get(sender, 0) < total_cost:
            return False
        self.unconfirmed_transactions.append({
            "sender": sender,
            "receiver": receiver,
            "amount": amount,
            "fee": self.transaction_fee
        })
        return True

    def mine(self, miner="Miner"):
        if not self.unconfirmed_transactions:
            return None

        last_block = self.chain[-1]
        new_block = Block(
            index=len(self.chain),
            timestamp=datetime.utcnow().isoformat(),
            transactions=self.unconfirmed_transactions.copy(),
            previous_hash=last_block.hash
        )
        self.chain.append(new_block)

        # Process transactions: deduct amounts and fees, reward miner
        total_fees = 0
        for txn in self.unconfirmed_transactions:
            self.balances[txn["sender"]] -= txn["amount"] + txn["fee"]
            self.balances[txn["receiver"]] += txn["amount"]
            total_fees += txn["fee"]

        # Reward miner
        self.balances[miner] = self.balances.get(miner, 0) + total_fees

        self.unconfirmed_transactions = []
        return new_block

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            curr = self.chain[i]
            prev = self.chain[i - 1]
            if curr.hash != curr.compute_hash():
                return False
            if curr.previous_hash != prev.hash:
                return False
        return True
