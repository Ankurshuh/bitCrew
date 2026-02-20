# import streamlit as st
# import pandas as pd
# import json
# import tempfile
# import os
# import sys
# from pyvis.network import Network
# import streamlit.components.v1 as components

# # Backend import
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# from BACKEND.main import run_engine

# st.set_page_config(page_title="Money Muling Detection", layout="wide")

# st.title("💰 Money Muling Detection – Financial Forensics Engine")

# uploaded_file = st.file_uploader("📂 Upload CSV File", type=["csv"])

# if uploaded_file is not None:

#     # Run backend engine
#     with st.spinner("Analyzing transactions..."):
#         result = run_engine(uploaded_file)

#     st.success("✅ Analysis Completed")

#     # ------------------- Summary ------------------- #
#     st.subheader("📊 Summary Metrics")
#     col1, col2, col3, col4 = st.columns(4)
#     col1.metric("Total Accounts", result["summary"]["total_accounts_analyzed"])
#     col2.metric("Suspicious Accounts", result["summary"]["suspicious_accounts_flagged"])
#     col3.metric("Fraud Rings", result["summary"]["fraud_rings_detected"])
#     col4.metric("Processing Time (s)", result["summary"]["processing_time_seconds"])

#     st.divider()

#     # ------------------- Fraud Rings Table ------------------- #
#     st.subheader("🔎 Fraud Ring Summary")
#     ring_table = []
#     for ring in result["fraud_rings"]:
#         ring_table.append({
#             "Ring ID": ring["ring_id"],
#             "Pattern Type": ring["pattern_type"],
#             "Member Count": len(ring["member_accounts"]),
#             "Risk Score": ring["risk_score"],
#             "Members": ", ".join(ring["member_accounts"])
#         })
#     if ring_table:
#         st.dataframe(pd.DataFrame(ring_table), use_container_width=True)
#     else:
#         st.info("No fraud rings detected.")

#     st.divider()

#     # ------------------- Interactive Graph ------------------- #
#     st.subheader("🌐 Transaction Graph")
#     df = pd.read_csv(uploaded_file)
#     nodes = set(df["sender_id"]).union(set(df["receiver_id"]))

#     # Suspicious accounts & ring members
#     suspicious_set = {acc["account_id"] for acc in result["suspicious_accounts"]}
#     ring_members = set()
#     for ring in result["fraud_rings"]:
#         ring_members.update(ring["member_accounts"])

#     net = Network(height="650px", width="100%", directed=True, notebook=False)
#     net.barnes_hut(gravity=-20000, central_gravity=0.3, spring_length=200, spring_strength=0.05, damping=0.09)

#     # Add nodes
#     for node in nodes:
#         title = f"Account ID: {node}"
#         if node in suspicious_set:
#             net.add_node(node, label=node, color="#ff4b4b", size=30, title="Suspicious\n" + title)
#         elif node in ring_members:
#             net.add_node(node, label=node, color="#ffa500", size=22, title="Ring Member\n" + title)
#         else:
#             net.add_node(node, label=node, color="#6baed6", size=15, title=title)

#     # Add edges
#     for _, row in df.iterrows():
#         net.add_edge(row["sender_id"], row["receiver_id"], title=f"Amount: {row['amount']}")

#     # Render graph
#     with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp_file:
#         net.save_graph(tmp_file.name)
#         HtmlFile = open(tmp_file.name, 'r', encoding='utf-8')
#         components.html(HtmlFile.read(), height=650)

#     st.divider()

#     # ------------------- Suspicious Accounts Table ------------------- #
#     st.subheader("🚨 Suspicious Accounts")
#     if result["suspicious_accounts"]:
#         susp_df = pd.DataFrame(result["suspicious_accounts"])
#         susp_df = susp_df.sort_values(by="suspicion_score", ascending=False)
#         st.dataframe(susp_df, use_container_width=True)
#     else:
#         st.info("No suspicious accounts detected.")

#     st.divider()

#     # ------------------- JSON Download ------------------- #
#     st.subheader("⬇ Download JSON Output")
#     json_data = json.dumps(result, indent=4)
#     st.download_button(
#         label="Download JSON File",
#         data=json_data,
#         file_name="money_muling_output.json",
#         mime="application/json"
#     )




import streamlit as st
import pandas as pd
import json
import tempfile
import os
import sys
from pyvis.network import Network
import streamlit.components.v1 as components

# Backend import
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from BACKEND.main import run_engine

st.set_page_config(page_title="Money Muling Detection", layout="wide")

st.title("💰 Money Muling Detection – Financial Forensics Engine")

uploaded_file = st.file_uploader("📂 Upload CSV File", type=["csv"])

if uploaded_file is not None:

    # Run backend engine
    with st.spinner("Analyzing transactions..."):
        result = run_engine(uploaded_file)

    st.success("✅ Analysis Completed")

    # ------------------- Summary ------------------- #
    st.subheader("📊 Summary Metrics")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Accounts", result["summary"]["total_accounts_analyzed"])
    col2.metric("Suspicious Accounts", result["summary"]["suspicious_accounts_flagged"])
    col3.metric("Fraud Rings", result["summary"]["fraud_rings_detected"])
    col4.metric("Processing Time (s)", result["summary"]["processing_time_seconds"])

    st.divider()

    # ------------------- Fraud Rings Table ------------------- #
    st.subheader("🔎 Fraud Ring Summary")
    ring_table = []
    for ring in result["fraud_rings"]:
        ring_table.append({
            "Ring ID": ring["ring_id"],
            "Pattern Type": ring["pattern_type"],
            "Member Count": len(ring["member_accounts"]),
            "Risk Score": ring["risk_score"],
            "Members": ", ".join(ring["member_accounts"])
        })
    if ring_table:
        st.dataframe(pd.DataFrame(ring_table), use_container_width=True)
    else:
        st.info("No fraud rings detected.")

    st.divider()

    # ------------------- Interactive Graph ------------------- #
    st.subheader("🌐 Transaction Graph")
    
    # --- GRAPH LEGEND (Added here) ---
    st.markdown("""
    <style>
    .legend-container {
        display: flex;
        gap: 20px;
        padding: 10px;
        background-color: #f0f2f6;
        border-radius: 5px;
        margin-bottom: 15px;
    }
    .legend-item {
        display: flex;
        align-items: center;
        font-size: 14px;
        font-weight: bold;
    }
    .dot {
        height: 12px;
        width: 12px;
        border-radius: 50%;
        display: inline-block;
        margin-right: 8px;
        border: 1px solid #333;
    }
    </style>
    <div class="legend-container">
        <div class="legend-item"><span class="dot" style="background-color: #ff4b4b;"></span>Suspicious Account</div>
        <div class="legend-item"><span class="dot" style="background-color: #ffa500;"></span>Fraud Ring Member</div>
        <div class="legend-item"><span class="dot" style="background-color: #6baed6;"></span>Normal Account</div>
    </div>
    """, unsafe_allow_html=True)
    # ---------------------------

    # FIX: Reset file pointer to start so we can read CSV again for the graph
    uploaded_file.seek(0) 
    
    # Check if columns exist to prevent generic errors
    try:
        df = pd.read_csv(uploaded_file)
        
        # Validate columns required for graph
        required_cols = ["sender_id", "receiver_id", "amount"]
        if not all(col in df.columns for col in required_cols):
            st.error(f"CSV missing required columns: {required_cols}")
        else:
            nodes = set(df["sender_id"]).union(set(df["receiver_id"]))

            # Suspicious accounts & ring members
            suspicious_set = {acc["account_id"] for acc in result["suspicious_accounts"]}
            ring_members = set()
            for ring in result["fraud_rings"]:
                ring_members.update(ring["member_accounts"])

            net = Network(height="650px", width="100%", directed=True, notebook=False)
            net.barnes_hut(gravity=-20000, central_gravity=0.3, spring_length=200, spring_strength=0.05, damping=0.09)

            # Add nodes
            for node in nodes:
                title = f"Account ID: {node}"
                if node in suspicious_set:
                    net.add_node(node, label=node, color="#ff4b4b", size=30, title="Suspicious\n" + title)
                elif node in ring_members:
                    net.add_node(node, label=node, color="#ffa500", size=22, title="Ring Member\n" + title)
                else:
                    net.add_node(node, label=node, color="#6baed6", size=15, title=title)

            # Add edges
            for _, row in df.iterrows():
                # Ensure amount is string for title
                amount_val = row['amount']
                net.add_edge(row["sender_id"], row["receiver_id"], title=f"Amount: {amount_val}")

            # Render graph
            with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp_file:
                net.save_graph(tmp_file.name)
                HtmlFile = open(tmp_file.name, 'r', encoding='utf-8')
                source_code = HtmlFile.read()
                components.html(source_code, height=650)

    except Exception as e:
        st.error(f"Error generating graph: {e}")
        st.info("Please ensure your CSV has 'sender_id', 'receiver_id', and 'amount' columns.")

    st.divider()

    # ------------------- Suspicious Accounts Table ------------------- #
    st.subheader("🚨 Suspicious Accounts")
    if result["suspicious_accounts"]:
        susp_df = pd.DataFrame(result["suspicious_accounts"])
        susp_df = susp_df.sort_values(by="suspicion_score", ascending=False)
        st.dataframe(susp_df, use_container_width=True)
    else:
        st.info("No suspicious accounts detected.")

    st.divider()

    # ------------------- JSON Download ------------------- #
    st.subheader("⬇ Download JSON Output")
    json_data = json.dumps(result, indent=4)
    st.download_button(
        label="Download JSON File",
        data=json_data,
        file_name="money_muling_output.json",
        mime="application/json"
    )