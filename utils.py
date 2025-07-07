# utils.py
import networkx as nx
from pyvis.network import Network

def draw_blockchain_graph(blockchain):
    net = Network(height="400px", width="100%", directed=True)
    for i, block in enumerate(blockchain.chain):
        label = f"Block {block.index}\nHash: {block.hash[:8]}...\nTxns: {len(block.transactions)}"
        net.add_node(i, label=label, title=block.hash, shape='box', color='lightblue')
        if i > 0:
            net.add_edge(i-1, i)
    net.save_graph("blockchain_graph.html")
    return "blockchain_graph.html"
