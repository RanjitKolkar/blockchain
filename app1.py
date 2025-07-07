# app.py
import streamlit as st
import streamlit.components.v1 as components
from blockchain import Blockchain
from utils import draw_blockchain_graph
import streamlit as st
import time

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
    - A distributed and immutable digital ledger.
    - Consists of blocks linked by cryptographic hashes.
    - Decentralized: No single point of control.
    - Transparent: Anyone can view the public ledger.
    - Secure: Data once written cannot be easily changed.
    - Trustless system: No need to trust a third party.
    - Each block contains timestamp, transactions, nonce, and hash.
    """)

with st.expander("⛏️ Mining Explained"):
    st.markdown("""
    - Process of validating transactions and adding them to the blockchain.
    - Miners solve cryptographic puzzles (Proof-of-Work).
    - Rewards include new coins and transaction fees.
    - Secures the network and maintains consensus.
    - High computational effort required (hashing).
    - Block difficulty adjusts over time.
    - Popular mining algorithms: SHA-256 (Bitcoin), Ethash (Ethereum).
    """)

with st.expander("🔐 Cryptography in Blockchain"):
    st.markdown("""
    - Hashing: Converts input data into fixed-length hash (e.g., SHA-256).
    - Digital Signatures: Ensures authenticity of sender using private keys.
    - Public-Key Cryptography: Transactions signed with private key, verified with public key.
    - Merkle Tree: Hierarchical hash tree for fast verification of transactions in blocks.
    - Nonce: A number used once to achieve desired hash pattern.
    - Immutable Ledger: Tampering with one block affects all following blocks.
    """)

with st.expander("🧾 Blockchain for Investigators"):
    st.markdown("""
    - Helps trace digital currency trails.
    - Wallet addresses are pseudo-anonymous.
    - KYC-compliant exchanges can link addresses to real users.
    - Used to detect money laundering, undeclared income.
    - Chain analysis tools can cluster wallets by entity.
    - Historical transactions available publicly.
    - Supports forensic tracing and audit trails.
    """)

with st.expander("🧩 Key Terms and Definitions"):
    st.markdown("""
    **Block**: A container of data (transactions) with a unique hash and a pointer to the previous block.

    **Genesis Block**: The first block in a blockchain.

    **Ledger**: Record of all transactions; in blockchain, it is distributed and shared.

    **Node**: A computer that maintains a copy of the blockchain and validates transactions.

    **Consensus Mechanism**: Rules that nodes follow to agree on the validity of transactions (e.g., PoW, PoS).

    **Proof of Work (PoW)**: Mining algorithm where miners compete to solve complex problems.

    **Proof of Stake (PoS)**: Validators are chosen based on stake (amount held) to validate transactions.

    **Smart Contracts**: Self-executing code on blockchain that runs when predefined conditions are met.

    **Wallet**: Digital tool to send, receive, and store cryptocurrency using public-private key pair.

    **Address**: A hashed public key used as a destination for crypto transactions.

    **Private Key**: A secret key used to sign transactions.

    **Public Key**: A key that can be shared; used to verify signatures and receive funds.

    **Transaction Fee**: Fee paid to miners/validators to prioritize and include the transaction in the block.

    **Fork**: A split in the blockchain protocol (soft fork – backward-compatible, hard fork – not compatible).

    **Exchange**: A platform to trade fiat with crypto or between cryptocurrencies.

    **Token**: A digital asset built on an existing blockchain (e.g., ERC-20 tokens on Ethereum).

    **Altcoin**: Any cryptocurrency other than Bitcoin.

    **Stablecoin**: A crypto asset pegged to a stable value like USD (e.g., USDT, USDC).

    **NFT (Non-Fungible Token)**: Unique cryptographic token representing ownership of a digital asset.

    **Cold Wallet**: Offline crypto storage method for enhanced security.

    **Hot Wallet**: Internet-connected wallet for ease of use but more vulnerable.

    **Gas**: Fee for executing operations (smart contracts, transactions) on Ethereum.

    **Blockchain Explorer**: Tool to view blockchain data like blocks, transactions, and addresses (e.g., blockchain.com).
    """)
st.subheader("🕵️ Investigator’s Corner")

st.markdown("""
Use this section to guide forensic or tax officers on tracing transactions and investigating wallets:

- 🔍 **Check suspicious transactions**
- 📊 **Trace flow of funds**
- 🔗 Use public blockchain explorers like:
    - [blockchain.com](https://www.blockchain.com/explorer)
    - [etherscan.io](https://etherscan.io)
    - [btcscan.org](https://btcscan.org)
    - [blockchair.com](https://blockchair.com)
    - [walletexplorer.com](https://www.walletexplorer.com)

---

### 🛠️ Suggested Tools:
- Chainalysis (paid)
- CipherTrace (paid)
- GraphSense (open-source)
- Bitquery (API-based)
""")


if 'visit_count' not in st.session_state:
    st.session_state.visit_count = 1
else:
    st.session_state.visit_count += 1

st.markdown("---")
st.markdown(f"👣 **Visitor Session Count**: {st.session_state.visit_count}")
st.markdown("🔗 Hosted by Dr. Ranjit Kolkar | Built with ❤️ using Streamlit")
