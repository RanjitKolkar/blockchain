import streamlit as st
import hashlib
import time
from datetime import datetime
import networkx as nx
from pyvis.network import Network
import streamlit.components.v1 as components

# -----------------------------
# Blockchain Core
# -----------------------------

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
            hash_attempt = self.compute_hash()
            if hash_attempt[:self.difficulty] == target:
                return hash_attempt
            self.nonce += 1

class Blockchain:
    def __init__(self):
        self.unconfirmed_transactions = []
        self.chain = []
        self.create_genesis_block()
        self.balances = {"Alice": 100, "Bob": 100, "Charlie": 100}

    def create_genesis_block(self):
        genesis = Block(0, str(datetime.utcnow()), "Genesis Block", "0")
        self.chain.append(genesis)

    def add_transaction(self, sender, receiver, amount):
        amount = float(amount)
        if self.balances.get(sender, 0) < amount:
            return False
        self.unconfirmed_transactions.append({'sender': sender, 'receiver': receiver, 'amount': amount})
        return True

    def mine(self):
        if not self.unconfirmed_transactions:
            return None
        last_block = self.chain[-1]
        block = Block(len(self.chain), str(datetime.utcnow()), self.unconfirmed_transactions, last_block.hash)
        self.chain.append(block)
        for txn in self.unconfirmed_transactions:
            self.balances[txn['sender']] -= txn['amount']
            self.balances[txn['receiver']] += txn['amount']
        self.unconfirmed_transactions = []
        return block

# -----------------------------
# Pyvis Graph for Blockchain
# -----------------------------

def draw_blockchain_graph(blockchain):
    G = nx.DiGraph()
    net = Network(height="400px", width="100%", directed=True)
    for i, block in enumerate(blockchain.chain):
        label = f"Block {block.index}\nHash: {block.hash[:8]}...\nTxns: {len(block.transactions)}"
        net.add_node(i, label=label, title=block.hash, shape='box', color='lightblue')
        if i > 0:
            net.add_edge(i-1, i)
    net.save_graph('blockchain_graph.html')
    return 'blockchain_graph.html'

# -----------------------------
# Streamlit Interface
# -----------------------------

st.set_page_config(layout="wide")
st.title("🔗 Crypto Blockchain Demo & Visualization")
st.markdown("Explore how blockchain, mining, and transactions work — interactively.")

if "bc" not in st.session_state:
    st.session_state.bc = Blockchain()

bc = st.session_state.bc

# Sidebar - Transaction
st.sidebar.header("💸 New Transaction")
sender = st.sidebar.selectbox("Sender", list(bc.balances.keys()))
receiver = st.sidebar.selectbox("Receiver", [x for x in bc.balances if x != sender])
amount = st.sidebar.number_input("Amount", min_value=1.0, max_value=1000.0, step=1.0)

if st.sidebar.button("➕ Add Transaction"):
    if bc.add_transaction(sender, receiver, amount):
        st.sidebar.success("Transaction added.")
    else:
        st.sidebar.error("Insufficient funds.")

if st.sidebar.button("⛏️ Mine Block"):
    with st.spinner("Mining block..."):
        block = bc.mine()
        if block:
            st.sidebar.success(f"Block {block.index} mined!")
        else:
            st.sidebar.warning("No transactions to mine.")

# Wallets
st.subheader("💰 Wallet Balances")
st.table(bc.balances)

# Pending Transactions
st.subheader("📬 Pending Transactions")
if bc.unconfirmed_transactions:
    st.json(bc.unconfirmed_transactions)
else:
    st.write("No pending transactions.")

# Blockchain Ledger
st.subheader("📚 Blockchain Ledger")
for block in reversed(bc.chain):
    with st.expander(f"Block #{block.index}"):
        st.write(f"**Timestamp:** {block.timestamp}")
        st.write(f"**Nonce:** {block.nonce}")
        st.write(f"**Transactions:**")
        st.json(block.transactions)
        st.code(f"Hash: {block.hash}")
        st.code(f"Previous Hash: {block.previous_hash}")

# Visual Graph
st.subheader("🕸️ Blockchain Chain Graph")
html_path = draw_blockchain_graph(bc)
components.html(open(html_path, 'r', encoding='utf-8').read(), height=450)

# Concepts Section
st.subheader("📖 Key Blockchain Concepts")

with st.expander("🧱 What is a Blockchain?"):
    st.markdown("""
    - A chain of digital blocks containing transaction data.
    - Each block has a hash linking to the previous block.
    - Ensures transparency, immutability, and public verifiability.
    """)

with st.expander("⛏️ What is Mining?"):
    st.markdown("""
    - Mining is solving a computational puzzle (proof-of-work) to add a new block.
    - Ensures no one can add false transactions.
    - In real blockchains, miners earn rewards for doing this.
    """)

with st.expander("🔐 Cryptography & Hashing"):
    st.markdown("""
    - Hashing ensures data integrity — even 1 character change makes a new hash.
    - Digital signatures ensure only wallet owners can authorize transfers.
    """)

with st.expander("🔍 Immutability & Transparency"):
    st.markdown("""
    - Once a block is mined, it cannot be altered without changing all future blocks.
    - Anyone can verify transactions using public explorers.
    """)

with st.expander("🧾 Why Important for Investigations"):
    st.markdown("""
    - Transactions are public and permanent — ideal for tracing assets.
    - Wallet addresses can be mapped to individuals via exchanges or devices.
    - Helps detect undeclared crypto gains and suspicious financial activity.
    """)

