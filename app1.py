# app.py
import streamlit as st
import streamlit.components.v1 as components
from blockchain import Blockchain
from utils import draw_blockchain_graph

st.set_page_config(layout="wide")
st.title("🔗 Crypto Blockchain Demo & Visualization")

if "bc" not in st.session_state:
    st.session_state.bc = Blockchain()

bc = st.session_state.bc

# Sidebar
st.sidebar.header("💸 New Transaction")
sender = st.sidebar.selectbox("Sender", list(bc.balances.keys()))
receiver = st.sidebar.selectbox("Receiver", [x for x in bc.balances if x != sender])
amount = st.sidebar.number_input("Amount", min_value=1.0, max_value=1000.0, step=1.0)

if st.sidebar.button("➕ Add Transaction"):
    if bc.add_transaction(sender, receiver, amount):
        st.sidebar.success("Transaction added.")
    else:
        st.sidebar.error("Insufficient balance.")

if st.sidebar.button("⛏️ Mine Block"):
    with st.spinner("Mining..."):
        block = bc.mine()
        if block:
            st.sidebar.success(f"Block {block.index} mined!")

# Balances
st.subheader("💰 Wallet Balances")
st.table(bc.balances)

# Transactions
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
        st.json(block.transactions)
        st.code(f"Hash: {block.hash}")
        st.code(f"Previous Hash: {block.previous_hash}")

# Visual Graph
st.subheader("🕸️ Blockchain Chain Graph")
html_path = draw_blockchain_graph(bc)
components.html(open(html_path, 'r', encoding='utf-8').read(), height=450)

# Concepts
st.subheader("📖 Blockchain Concepts")

with st.expander("🧱 What is a Blockchain?"):
    st.markdown("""
    - Digital ledger of blocks linked by hashes.
    - Each block contains verified transaction data.
    """)

with st.expander("⛏️ Mining Explained"):
    st.markdown("""
    - Mining adds transactions to the blockchain by solving puzzles.
    - It ensures network security and prevents double-spending.
    """)

with st.expander("🔐 Why Cryptography?"):
    st.markdown("""
    - Hashing ensures integrity.
    - Signatures ensure transaction ownership.
    """)

with st.expander("🧾 Why It's Useful for Investigators"):
    st.markdown("""
    - Public ledgers can be traced.
    - Wallet addresses may link to real-world identities via KYC.
    - Can reveal undeclared income.
    """)
