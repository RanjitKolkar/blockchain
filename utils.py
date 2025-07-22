from pyvis.network import Network

def draw_blockchain_graph(blockchain):
    net = Network(height="400px", width="100%", directed=True)
    for i, block in enumerate(blockchain.chain):
        if isinstance(block.transactions, str):
            tx_summary = "Genesis"
        else:
            tx_summary = f"{len(block.transactions)} txns"
        label = f"Block {block.index}\nHash: {block.hash[:8]}...\n{tx_summary}"
        net.add_node(i, label=label, title=block.hash, shape='box', color='lightblue')
        if i > 0:
            net.add_edge(i - 1, i, title="prev_hash")

    net.set_options("""
        var options = {
          "nodes": {
            "font": {
              "size": 14
            }
          },
          "edges": {
            "arrows": {
              "to": {
                "enabled": true
              }
            }
          }
        }
    """)
    net.save_graph("blockchain_graph.html")
    return "blockchain_graph.html"
