import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import random
import time
from datetime import datetime

# Initialize session states
def init_session():
    if "event_logs" not in st.session_state:
        st.session_state.event_logs = []
    if "messages_exchanged" not in st.session_state:
        st.session_state.messages_exchanged = 0
    if "failures" not in st.session_state:
        st.session_state.failures = 0
    if "latency_records" not in st.session_state:
        st.session_state.latency_records = []
init_session()

# Utility function to log events
def log_event(message):
    timestamp = datetime.now().strftime("%H:%M:%S")
    st.session_state.event_logs.append(f"[{timestamp}] {message}")
    if len(st.session_state.event_logs) > 100:
        st.session_state.event_logs.pop(0)

# Page config
st.set_page_config(page_title="Distributed System Simulator", layout="centered")

st.title("\U0001F4E1 Distributed System Simulator")
st.write("Select a system model to simulate and analyze basic performance.")

# Sidebar Metrics & Logs
with st.sidebar:
    st.markdown("### \U0001F4CA Performance Metrics")
    st.metric("Messages Exchanged", st.session_state.messages_exchanged)
    st.metric("Node Failures", st.session_state.failures)
    avg_latency = (sum(st.session_state.latency_records) / len(st.session_state.latency_records)
                   if st.session_state.latency_records else 0)
    st.metric("Avg Latency (s)", f"{avg_latency:.2f}")

    st.markdown("---")
    st.markdown("### \U0001F4DD Event Logs (Latest 10)")
    for event in st.session_state.event_logs[-10:][::-1]:
        st.write(f"• {event}")

# ---------- Tabs ----------
tab1, tab2 = st.tabs(["🔧 Simulator", "📘 Theory Concepts"])

# ---------- Simulator Tab ----------
with tab1:
    st.header("🔧 Distributed System Simulator")
    model = st.selectbox(
        "Choose a Distributed System Model",
        ("Client-Server", "Peer-to-Peer", "Cluster-Based", "Cloud Model")
    )

    # ----- CLIENT-SERVER -----
    if model == "Client-Server":
        st.subheader("Client-Server Model")
        st.write("Clients send requests to a central server for processing.")
        st.image("https://upload.wikimedia.org/wikipedia/commons/4/4e/Client-server-model.svg", width=500)

        def draw_client_server():
            G = nx.DiGraph()
            G.add_nodes_from(["Server", "Client 1", "Client 2", "Client 3"])
            G.add_edges_from([("Client 1", "Server"), ("Client 2", "Server"), ("Client 3", "Server")])
            G.add_edges_from([("Server", "Client 1"), ("Server", "Client 2"), ("Server", "Client 3")])
            pos = {
                "Server": (0.5, 1),
                "Client 1": (0.2, 0.1),
                "Client 2": (0.5, 0.1),
                "Client 3": (0.8, 0.1)
            }
            fig, ax = plt.subplots()
            nx.draw(G, pos, with_labels=True, node_color="skyblue", node_size=2000, font_size=10, arrows=True, ax=ax)
            st.pyplot(fig)

        draw_client_server()
        col1, col2 = st.columns(2)

        with col1:
            if st.button("\U0001F4E8 Simulate Message"):
                st.session_state.messages_exchanged += 1
                log_event("Client 1 → Server: Request Sent")
                log_event("Server → Client 1: Response Sent")
                st.success("Message exchanged successfully!")

        with col2:
            if st.button("❌ Simulate Node Failure"):
                failed_node = random.choice(["Client 1", "Client 2", "Client 3"])
                st.session_state.failures += 1
                log_event(f"{failed_node} has failed!")
                st.error(f"{failed_node} is down! ❌")

        if st.button("⏱ Simulate Latency"):
            delay = random.uniform(0.5, 2.5)
            st.session_state.latency_records.append(delay)
            log_event(f"Simulating latency of {delay:.2f} seconds...")
            with st.spinner(f"Waiting {delay:.2f} seconds..."):
                time.sleep(delay)
            st.success("Message delivered!")

    # ----- PEER-TO-PEER -----
    elif model == "Peer-to-Peer":
        st.subheader("Peer-to-Peer Model")
        st.write("Every node acts as both client and server, sharing resources directly.")
        st.image("https://upload.wikimedia.org/wikipedia/commons/f/f4/Peer-to-peer-network.svg", width=500)

        def draw_p2p():
            G = nx.Graph()
            peers = ["Peer A", "Peer B", "Peer C", "Peer D"]
            G.add_nodes_from(peers)
            G.add_edges_from([("Peer A", "Peer B"), ("Peer A", "Peer C"), ("Peer B", "Peer D"), ("Peer C", "Peer D")])
            pos = {
                "Peer A": (0.1, 0.5),
                "Peer B": (0.4, 0.8),
                "Peer C": (0.4, 0.2),
                "Peer D": (0.7, 0.5)
            }
            fig, ax = plt.subplots()
            nx.draw(G, pos, with_labels=True, node_color="lightgreen", node_size=2000, font_size=10, ax=ax)
            st.pyplot(fig)

        draw_p2p()
        col1, col2 = st.columns(2)

        with col1:
            if st.button("🔁 Simulate File Sharing"):
                sender = random.choice(["Peer A", "Peer B", "Peer C", "Peer D"])
                receiver = random.choice([p for p in ["Peer A", "Peer B", "Peer C", "Peer D"] if p != sender])
                st.session_state.messages_exchanged += 1
                log_event(f"{sender} → {receiver}: File Sent Successfully")
                st.success(f"{sender} → {receiver}: 'File Sent Successfully'")

        with col2:
            if st.button("❌ Simulate Node Failure"):
                failed_node = random.choice(["Peer A", "Peer B", "Peer C", "Peer D"])
                st.session_state.failures += 1
                log_event(f"{failed_node} has failed!")
                st.error(f"{failed_node} is down! ❌")

        if st.button("⏱ Simulate Latency"):
            delay = random.uniform(0.5, 2.5)
            st.session_state.latency_records.append(delay)
            log_event(f"Simulating latency of {delay:.2f} seconds...")
            with st.spinner(f"Waiting {delay:.2f} seconds..."):
                time.sleep(delay)
            st.success("File successfully shared!")

    # ----- CLUSTER-BASED -----
    elif model == "Cluster-Based":
        st.subheader("Cluster-Based Model")
        st.write("A master node distributes tasks to multiple workers for parallel processing.")

        def draw_cluster():
            G = nx.DiGraph()
            master = "Master Node"
            workers = ["Worker 1", "Worker 2", "Worker 3", "Worker 4"]
            G.add_node(master)
            G.add_nodes_from(workers)
            for w in workers:
                G.add_edge(master, w)
            pos = {
                "Master Node": (0.5, 0.8),
                "Worker 1": (0.1, 0.4),
                "Worker 2": (0.35, 0.4),
                "Worker 3": (0.65, 0.4),
                "Worker 4": (0.9, 0.4),
            }
            fig, ax = plt.subplots()
            nx.draw(G, pos, with_labels=True, node_color="lightcoral", node_size=2000, font_size=10, arrows=True, ax=ax)
            st.pyplot(fig)

        draw_cluster()
        col1, col2 = st.columns(2)

        with col1:
            if st.button("🚀 Distribute Task"):
                worker = random.choice(["Worker 1", "Worker 2", "Worker 3", "Worker 4"])
                st.session_state.messages_exchanged += 1
                log_event(f"Master → {worker}: Task Assigned")
                st.success(f"Master Node → {worker}: 'Task Assigned ✅'")

        with col2:
            if st.button("❌ Simulate Node Failure"):
                failed_node = random.choice(["Worker 1", "Worker 2", "Worker 3", "Worker 4"])
                st.session_state.failures += 1
                log_event(f"{failed_node} has failed!")
                st.error(f"{failed_node} is down! ❌")

        if st.button("⏱ Simulate Latency"):
            delay = random.uniform(0.5, 2.5)
            st.session_state.latency_records.append(delay)
            log_event(f"Simulating latency of {delay:.2f} seconds...")
            with st.spinner(f"Waiting {delay:.2f} seconds..."):
                time.sleep(delay)
            st.success("Task successfully distributed!")

    # ----- CLOUD MODEL -----
    elif model == "Cloud Model":
        st.subheader("Cloud Model")
        st.write("Resources are delivered as services over the internet from data centers.")
        st.image("https://upload.wikimedia.org/wikipedia/commons/3/37/Cloud_computing.svg", width=500)

        def draw_cloud():
            G = nx.DiGraph()
            G.add_nodes_from(["User 1", "User 2", "Cloud Provider", "Data Center 1", "Data Center 2"])
            G.add_edges_from([
                ("User 1", "Cloud Provider"), ("User 2", "Cloud Provider"),
                ("Cloud Provider", "Data Center 1"), ("Cloud Provider", "Data Center 2"),
                ("Data Center 1", "Cloud Provider"), ("Data Center 2", "Cloud Provider"),
                ("Cloud Provider", "User 1"), ("Cloud Provider", "User 2")
            ])

            pos = {
                "User 1": (0.2, 0.2),
                "User 2": (0.8, 0.2),
                "Cloud Provider": (0.5, 0.5),
                "Data Center 1": (0.3, 0.8),
                "Data Center 2": (0.7, 0.8)
            }

            fig, ax = plt.subplots()
            nx.draw(G, pos, with_labels=True, node_color="plum", node_size=2000, font_size=10, arrows=True, ax=ax)
            st.pyplot(fig)

        draw_cloud()

        col1, col2 = st.columns(2)

        with col1:
            if st.button("☁️ Simulate Service Request"):
                sender = random.choice(["User 1", "User 2"])
                datacenter = random.choice(["Data Center 1", "Data Center 2"])
                st.session_state.messages_exchanged += 1
                log_event(f"{sender} → Cloud Provider → {datacenter}: Request Delivered")
                st.success(f"{sender}'s service request successfully routed to {datacenter}")

        with col2:
            if st.button("🌩 Simulate Node Failure"):
                failed_node = random.choice(["User 1", "User 2", "Data Center 1", "Data Center 2"])
                st.session_state.failures += 1
                log_event(f"{failed_node} has failed!")
                st.error(f"{failed_node} is down!")

        if st.button("📶 Simulate Latency"):
            delay = random.uniform(0.5, 2.5)
            st.session_state.latency_records.append(delay)
            log_event(f"Latency: {delay:.2f} seconds")
            with st.spinner(f"Waiting {delay:.2f} seconds..."):
                time.sleep(delay)
            st.success("Data successfully transmitted!")

# ---------- Theory Tab ----------
with tab2:
    st.header("📘 Theory Concepts in Distributed Systems")

    with st.expander("📦 Network Packet Drop"):
        st.markdown("""
        Packet drops occur when data packets traveling across a network fail to reach their destination.
        Reasons include network congestion, faulty routing, or physical layer issues.
        In distributed systems, this can affect consistency and reliability.
        """)

    with st.expander("⚖️ Load Balancing"):
        st.markdown("""
        Load balancing is the process of distributing tasks evenly across multiple nodes.
        This prevents any single node from becoming a bottleneck and improves performance.
        Common algorithms include Round Robin, Least Connections, and Resource-Based.
        """)

    with st.expander("🛡️ Fault Tolerance"):
        st.markdown("""
        Fault tolerance ensures that a system continues to operate even if some components fail.
        Techniques include replication, failover mechanisms, and distributed consensus protocols.
        """)

    with st.expander("🔁 Replication and Consistency"):
        st.markdown("""
        Data replication involves maintaining multiple copies of data across different nodes.
        Consistency ensures all replicas reflect the same data state. Models include eventual consistency,
        strong consistency, and causal consistency.
        """)

    with st.expander("🧠 Scalability"):
        st.markdown("""
        Scalability refers to the system’s ability to handle growth (in users, data, etc.).
        Horizontal scaling adds more nodes, while vertical scaling upgrades existing ones.
        """)

    with st.expander("🧪 Testing in Distributed Systems"):
        st.markdown("""
        Testing distributed systems involves validating functionality, performance,
        fault recovery, and consistency under different network conditions and failures.
        Simulations and chaos testing tools are often used.
        """)
    with st.expander("📖 Transparency in Distributed Systems"):
         st.markdown("""
    Distributed systems aim to provide transparency to users in several ways:
    
    - **Access Transparency**: Hide differences in data representation and how resources are accessed.
    - **Location Transparency**: Hide the physical location of resources.
    - **Concurrency Transparency**: Allow concurrent access to shared resources without interference.
    - **Replication Transparency**: Hide replication of resources to improve reliability and performance.
    - **Failure Transparency**: Hide failure and recovery of resources.
    """)

with st.expander("⚡ Types of Latency"):
    st.markdown("""
    - **Propagation Delay**: Time taken for a signal to travel from sender to receiver.
    - **Transmission Delay**: Time to push all bits into the wire.
    - **Processing Delay**: Time taken by nodes to process the packet header.
    """)

with st.expander("⚖️ CAP Theorem"):
    st.markdown("""
    The **CAP Theorem** states that a distributed system can only satisfy **two out of three** guarantees:
    
    - **Consistency**: All nodes see the same data at the same time.
    - **Availability**: Every request receives a (non-error) response.
    - **Partition Tolerance**: The system continues to operate despite network partitioning.
    
    > 📌 In practice, distributed systems choose **CA**, **CP**, or **AP** based on their needs.
    """)

with st.expander("💣 Types of Failures in Distributed Systems"):
    st.markdown("""
    - **Crash Failure**: Node stops working and becomes unresponsive.
    - **Omission Failure**: Message is lost during transmission.
    - **Timing Failure**: Node responds, but outside the expected time window.
    - **Byzantine Failure**: Node behaves arbitrarily or maliciously (hardest to detect).
    """)

with st.expander("🧩 Middleware in Distributed Systems"):
    st.markdown("""
    Middleware is a software layer that lies between the operating system and distributed applications. It:
    
    - Provides communication, data exchange, and service management.
    - Hides system complexity.
    - Ensures interoperability between different systems.
    """)

with st.expander("📊 Comparison of System Models"):
    st.markdown("""
    | Model         | Central Control | Scalability | Fault Tolerance | Example |
    |---------------|------------------|-------------|------------------|---------|
    | Client-Server | ✅ Yes           | ❌ Limited   | ❌ Low            | Web Apps |
    | Peer-to-Peer  | ❌ No            | ✅ High      | ✅ High           | BitTorrent |
    | Cluster-Based | ✅ Yes           | ✅ Good      | ✅ Moderate       | Hadoop |
    | Cloud Model   | ✅ Yes           | ✅ Excellent | ✅ High           | AWS, Azure |
    """)
