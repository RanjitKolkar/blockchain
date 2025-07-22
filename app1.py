import streamlit as st
import streamlit.components.v1 as components
from blockchain import Blockchain
from utils import draw_blockchain_graph
from block_helpers import render_block_detail
import time

st.set_page_config(layout="wide")
st.title("🔗 Crypto Blockchain Demo & Visualization")

# Initialize blockchain
if "bc" not in st.session_state:
    st.session_state.bc = Blockchain()

bc = st.session_state.bc

# Sidebar - New Transaction
st.sidebar.header("💸 New Transaction")
sender = st.sidebar.selectbox("Sender", list(bc.balances.keys()))
receiver = st.sidebar.selectbox("Receiver", [x for x in bc.balances if x != sender])
amount = st.sidebar.number_input("Amount", min_value=1.0, max_value=1000.0, step=1.0)

st.sidebar.info(f"Transaction Fee: {bc.transaction_fee}")

if st.sidebar.button("➕ Add Transaction"):
    if bc.add_transaction(sender, receiver, amount):
        st.sidebar.success("Transaction added.")
    else:
        st.sidebar.error("Insufficient balance.")

# Sidebar - Miner and Mining
miner = st.sidebar.selectbox("Select Miner", list(bc.balances.keys()) + ["Miner"])

if st.sidebar.button("⛏️ Mine Block"):
    with st.spinner("Mining..."):
        start = time.time()
        block = bc.mine(miner)
        duration = time.time() - start
        if block:
            st.sidebar.success(f"Block {block.index} mined by {miner} in {duration:.2f}s!")

# Wallet Balances
st.subheader("💰 Wallet Balances")
st.table(bc.balances)

# Pending Transactions
st.subheader("📬 Pending Transactions")
if bc.unconfirmed_transactions:
    for txn in bc.unconfirmed_transactions:
        st.write(f"📤 **{txn['sender']}** → 📥 **{txn['receiver']}** | 💰 {txn['amount']} | 🪙 Fee: {txn['fee']}")
else:
    st.write("No pending transactions.")

# Blockchain Ledger (Modular View)
st.subheader("📚 Blockchain Ledger")
for block in reversed(bc.chain):
    with st.expander(f"Block #{block.index} Details"):
        render_block_detail(block)

# Blockchain Graph
st.subheader("🕸️ Blockchain Chain Graph")
html_path = draw_blockchain_graph(bc)
components.html(open(html_path, 'r', encoding='utf-8').read(), height=450)

# Concepts and Investigator Sections
# (keep same as your original code)
# ... omitted for brevity
