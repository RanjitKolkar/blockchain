import streamlit as st
import streamlit.components.v1 as components
from blockchain import Blockchain
from utils import draw_blockchain_graph
from block_helper import render_block_detail
import time

st.set_page_config(layout="wide")
st.title("Crypto Blockchain Demo & Visualization")

if "bc" not in st.session_state:
    st.session_state.bc = Blockchain()

bc = st.session_state.bc

# Sidebar - Add Transaction
st.sidebar.header("💸 New Transaction")
sender = st.sidebar.selectbox("Sender", list(bc.balances.keys()))
receiver = st.sidebar.selectbox("Receiver", [x for x in bc.balances if x != sender])
amount = st.sidebar.number_input("Amount", min_value=1.0, step=1.0)
st.sidebar.info(f"Transaction Fee: {bc.transaction_fee}")

if st.sidebar.button("➕ Add Transaction"):
    if bc.add_transaction(sender, receiver, amount):
        st.sidebar.success("Transaction added.")
    else:
        st.sidebar.error("Insufficient balance.")

# Sidebar - Mine Block
miner = st.sidebar.selectbox("Select Miner", list(bc.balances.keys()) + ["Miner"])
if st.sidebar.button("⛏️ Mine Block"):
    with st.spinner("Mining..."):
        start = time.time()
        block = bc.mine(miner)
        duration = time.time() - start
        if block:
            st.sidebar.success(f"Block #{block.index} mined by {miner} in {duration:.2f}s!")
        else:
            st.sidebar.warning("No transactions to mine.")

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

# Blockchain Ledger
st.subheader("📚 Blockchain Ledger")
for block in reversed(bc.chain):
    with st.expander(f"Block #{block.index}"):
        render_block_detail(block)

# Blockchain Graph
st.subheader("🕸️ Blockchain Chain Graph")
html_path = draw_blockchain_graph(bc)
components.html(open(html_path, 'r', encoding='utf-8').read(), height=450)

# Optional: Validity Check
st.markdown("✅ Chain Validity: " + ("✔️ Valid" if bc.is_chain_valid() else "❌ Invalid"))

# Learn Tab
learn_tab, = st.tabs(["📘 Learn"])

with learn_tab:
    st.subheader("📖 Blockchain Concepts & Explorer Terms")

    with st.expander("🧱 What is a Blockchain?"):
        st.markdown("""
        - A **blockchain** is a secure, distributed digital ledger.
        - It records transactions in **blocks** that are cryptographically linked (via hashes).
        - Once added, blocks cannot be modified (immutability).
        - **Decentralized**: No central authority.
        - **Public or private** depending on use case.
        """)

    with st.expander("📦 Block Parameters Explained (like blockchain.com)"):
        st.markdown("""
        Each block contains several important fields:

        - `index`: The position of the block in the chain.
        - `timestamp`: When the block was created.
        - `transactions`: List of transaction objects included in the block.
        - `nonce`: Number miners change to find a valid hash.
        - `difficulty`: How hard it is to mine the block (affects required hash).
        - `hash`: Unique fingerprint of the block, generated using SHA-256.
        - `previous_hash`: Hash of the previous block, ensuring chain integrity.

        **Example from this app:**
        ```json
        {
            "index": 3,
            "timestamp": "2025-07-22T18:20:45Z",
            "transactions": [
                {"sender": "Alice", "receiver": "Bob", "amount": 10.0, "fee": 1.0}
            ],
            "nonce": 20482,
            "hash": "0000abc123...xyz",
            "previous_hash": "0000cde456...abc"
        }
        ```
        """)

    with st.expander("💳 Transaction Parameters Explained"):
        st.markdown("""
        Each transaction contains:

        - `sender`: Wallet address or name sending the amount.
        - `receiver`: The recipient's wallet or address.
        - `amount`: How much crypto is sent.
        - `fee`: Transaction fee (rewarded to the miner).
        
        **Optional (not in this demo but used in real blockchains):**
        - `signature`: Digital signature to verify authenticity.
        - `txid`: Unique transaction ID.
        - `timestamp`: When the transaction was created.
        """)

    with st.expander("🔐 Cryptographic Concepts"):
        st.markdown("""
        - **Hash Function (SHA-256)**: Converts data into a fixed 64-character string. Used for block hashes.
        - **Nonce**: A number that miners adjust to get a valid hash.
        - **Proof of Work (PoW)**: Requires computation to mine a block.
        - **Digital Signatures**: Verify sender identity in real blockchain networks.
        - **Merkle Root**: Root hash of a tree of transactions (not shown in this app, but used in Bitcoin).
        """)

    with st.expander("🧾 Glossary of Key Terms"):
        st.markdown("""
        - **Genesis Block**: First block in any blockchain.
        - **Wallet**: Software or hardware to send, receive, and store crypto.
        - **Address**: Public key hash, used to identify a wallet.
        - **Private Key**: Secret key used to sign transactions.
        - **Miner**: Participant who validates transactions and mines blocks.
        - **Consensus Mechanism**: Rules for how blocks are validated (e.g., PoW, PoS).
        - **Smart Contract**: Code that runs on blockchain (e.g., Ethereum).
        - **Token**: An asset built on top of a blockchain (e.g., ERC-20).
        - **Fork**: Split in blockchain rules (hard fork or soft fork).
        - **Blockchain Explorer**: Website showing blocks, transactions, wallets (e.g., blockchain.com).
        """)

    with st.expander("🔍 For Investigators / Analysts"):
        st.markdown("""
        - Blockchain is public and immutable: good for tracing digital assets.
        - Tools like **Chainalysis**, **CipherTrace**, or **GraphSense** help visualize flows.
        - KYC-compliant exchanges can de-anonymize wallets.
        - Each transaction can be linked using:
            - Wallet address
            - Time/date
            - Amounts
            - Previous transactions
        """)

# Footer
st.markdown("---")

from datetime import datetime

# 👣 Visitor count already exists above

# 🕓 Last Updated Timestamp
now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
st.markdown(f"<div style='text-align:center; margin-top: 20px;'>🕓 <b>🔗 Built by Coding Club: Dr. Ranjit Kolkar, Last Updated:</b> {now}</div>", unsafe_allow_html=True)

# 🖋️ Inject custom CSS to increase font size
st.markdown("""
    <style>
    html, body, [class*="css"]  {
        font-size: 15px !important;
    }
    .block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
    }
    </style>
""", unsafe_allow_html=True)
