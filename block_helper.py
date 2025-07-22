import streamlit as st

def render_block_detail(block):
    st.write(f"**Block Index:** {block.index}")
    st.write(f"**Timestamp:** {block.timestamp}")
    st.write(f"**Nonce:** {block.nonce}")
    st.write(f"**Hash:** `{block.hash}`")
    st.write(f"**Previous Hash:** `{block.previous_hash}`")

    if isinstance(block.transactions, str):
        st.write("No transactions (Genesis Block).")
    else:
        st.write(f"**Number of Transactions:** {len(block.transactions)}")
        total_fees = 0
        for txn in block.transactions:
            fee = txn.get("fee", 0.0)
            total_fees += fee
            st.markdown(
                f"📤 **{txn['sender']}** → 📥 **{txn['receiver']}** | 💰 {txn['amount']} | 🪙 Fee: {fee}"
            )
        st.markdown(f"**💎 Miner Reward (Total Fees):** `{total_fees}`")

    st.write("---")
