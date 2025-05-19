import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

# Initialize session state
if "edges" not in st.session_state:
    st.session_state.edges = []

if "graph" not in st.session_state:
    st.session_state.graph = nx.Graph()

if "ospf_path" not in st.session_state:
    st.session_state.ospf_path = []

st.set_page_config(layout="wide")
st.title("OSPF Shortest Path Visualizer")

# Sidebar input
with st.sidebar:
    st.header("Batch Add Edges")
    edge_input = st.text_area("Enter list of edges (e.g. [[1, 2, 1], [2, 3, 2]])")

    if st.button("Render Batch Graph"):
        try:
            edges = eval(edge_input)
            st.session_state.edges = edges
            G = nx.Graph()
            for src, dst, cost in edges:
                G.add_edge(src, dst, weight=cost)
            st.session_state.graph = G
            st.success("Graph rendered successfully!")
        except Exception as e:
            st.error(f"Error parsing edges: {e}")

    st.header("Add Single Link")
    parent = st.text_input("Parent Router ID")
    child = st.text_input("Child Router ID")
    cost = st.number_input("Link Cost", min_value=1, step=1)

    if st.button("Add Link"):
        try:
            p = int(parent)
            c = int(child)
            st.session_state.graph.add_edge(p, c, weight=cost)
            st.session_state.edges.append([p, c, cost])
            st.success("Link added!")
        except Exception as e:
            st.error(f"Error adding link: {e}")

# Simulate OSPF
st.header("Run OSPF")
col1, col2 = st.columns(2)
with col1:
    source = st.number_input("Source Router", min_value=1, step=1)
with col2:
    destination = st.number_input("Destination Router", min_value=1, step=1)

if st.button("Simulate OSPF"):
    try:
        G = st.session_state.graph
        path = nx.dijkstra_path(G, source=source, target=destination, weight='weight')
        st.session_state.ospf_path = path
        st.success(f"OSPF Path: {path}")
    except Exception as e:
        st.error(f"Error running OSPF: {e}")

# Draw graph
st.header("Graph Visualization")

if not st.session_state.graph.edges:
    st.warning("Graph not rendered yet.")
else:
    G = st.session_state.graph
    path = st.session_state.ospf_path

    pos = nx.spring_layout(G, seed=42)
    edge_labels = nx.get_edge_attributes(G, "weight")

    fig, ax = plt.subplots(figsize=(8, 6))
    nx.draw(G, pos, ax=ax, with_labels=True, node_color='lightblue', edge_color='gray', node_size=700, font_size=10)

    if path:
        highlight_edges = list(zip(path[:-1], path[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=highlight_edges, edge_color='red', width=3, ax=ax)
    
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax)
    st.pyplot(fig)
