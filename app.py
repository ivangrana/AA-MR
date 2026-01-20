import asyncio

import streamlit as st
from agno.tools.mcp import MCPTools

from src.agents import main_agent

st.set_page_config(page_title="AA-MR", layout="wide", page_icon=":material/graph_3:")

# ---------- sidebar navigation ----------
with st.sidebar:
    st.markdown("# :material/graph_3: :blue[AA-MR]")
    st.divider()

    page = st.selectbox(
        "Navigation",
        options=[
            "Dashboard",
            "Chat",
            "Gapfilling",
            "Reconaissance agent",
            "Training",
        ],
        index=1,
        format_func=lambda x: {
            "Dashboard": "Dashboard",
            "Chat": "Chat",
            "Gapfilling": "Gapfilling",
            "Reconaissance agent": "Model Building",
            "Training": "Knowledge Base",
        }[x],
        help="Select a page",
        label_visibility="visible",
    )
    st.divider()

    # docs button,redirects to google.com link on click
    st.link_button(
        "Documentation",
        url="https://google.com",
        help="Open the documentation",
        width="content",
        icon=":material/book_2:",
    )

    @st.dialog("Connect to MCP Server")
    def connect_mcp_dialog():
        host = st.text_input("MCP Server Host", placeholder="e.g., 127.0.0.1")
        port = st.text_input("Port")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("Connect"):
                # Save connection info to session state or handle connection here
                st.session_state.mcp_server = {
                    "host": host,
                    "port": port,
                    "username": username,
                    "password": password,
                }

                main_agent.tools.append(
                    MCPTools(
                        url=f"http://{host}:{port}/mcp",
                    )
                )

                st.success("MCP server connection parameters saved.")
                # st.rerun()

        with col2:
            if st.button("Close"):
                st.rerun()

    if st.button(
        "Connect MCP server",
        width="content",
        icon=":material/plug_connect:",
    ):
        connect_mcp_dialog()


st.session_state.page = page

page = st.session_state.page

# ---------- session state ----------
# Separate chat histories for each chat page
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []
if "recon_messages" not in st.session_state:
    st.session_state.recon_messages = []

if "swagger_analysis" not in st.session_state:
    st.session_state.swagger_analysis = []

if "knowledge_snippets" not in st.session_state:
    # Initialize knowledge snippets as a list of dicts with 'title' and 'content'
    st.session_state.knowledge_snippets = []

if page == "Chat":
    # ---------- display history ----------
    for msg in st.session_state.chat_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"], unsafe_allow_html=False)
    # ---------- input ----------
    if prompt := st.chat_input("Ask me anything…"):
        st.session_state.chat_messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # ---------- run agent ----------
        async def async_run_agent(prompt):
            full = ""
            placeholder = st.empty()
            async for chunk in main_agent.arun(prompt, stream=True, debug_mode=True):
                if chunk.content:
                    full += chunk.content
                    placeholder.markdown(full + "▌")
            placeholder.markdown(full)
            return full

        with st.chat_message("assistant"):
            full = asyncio.run(async_run_agent(prompt))
        st.session_state.chat_messages.append({"role": "assistant", "content": full})

elif page == "Gapfilling":
    st.header("Gapfilling Tool")
    swagger_file = st.file_uploader("Upload a SBML model file", type=["sbml", "xml"])
    if swagger_file is not None:
        try:
            file_bytes = swagger_file.read()
            # Try to decode as UTF-8 text
            content_str = file_bytes.decode("utf-8")
            with st.spinner("Analyzing Model..."):
                pass
        except Exception as e:
            st.error(f"Error reading or analyzing the SBML model file: {e}")

elif page == "Dashboard":
    import numpy as np
    import pandas as pd
    import plotly.express as px

    st.header("Dashboard")

    # Use Streamlit's native columns for layout
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(label="Total Metabolic Pathways", value=128, delta="3%")
    with col2:
        st.metric(label="Active Reactions", value=456, delta="10%")
    with col3:
        st.metric(label="Coverage Score", value="76%", delta="-1%")

    # Placeholder for a Plotly visualization of metabolic pathways
    st.subheader("Pathway Activity Across Samples")

    # Generate example data
    samples = [f"Sample {i + 1}" for i in range(10)]
    pathway_activities = np.random.uniform(low=0, high=100, size=10)
    df = pd.DataFrame({"Sample": samples, "Activity": pathway_activities})

    # Display a Plotly chart for better interactivity
    fig = px.density_heatmap(
        df, x="Sample", y="Activity", title="Pathway Activity Across Samples"
    )
    st.plotly_chart(fig, use_container_width=True)

    # Trend line graph using Plotly for better integration
    st.subheader("Trend Line of Pathway Activity")
    line_fig = px.line(df, x="Sample", y="Activity", markers=True)
    st.plotly_chart(line_fig, use_container_width=True)


elif page == "Reconaissance agent":
    print("hi")

elif page == "Training":
    st.header("Knowledge Base")

    # Ensure session state initialization
    if "knowledge_snippets" not in st.session_state:
        st.session_state.knowledge_snippets = []

    if "new_title" not in st.session_state:
        st.session_state.new_title = ""

    if "new_content" not in st.session_state:
        st.session_state.new_content = ""

    def add_snippet():
        if (
            st.session_state.new_title.strip() == ""
            or st.session_state.new_content.strip() == ""
        ):
            st.warning("Both title and content must be provided.")
            return

        st.session_state.knowledge_snippets.append(
            {
                "title": st.session_state.new_title.strip(),
                "content": st.session_state.new_content.strip(),
            }
        )

        st.session_state.new_title = ""
        st.session_state.new_content = ""

    # Display existing snippets
    snippets = st.session_state.knowledge_snippets

    for idx, snippet in enumerate(snippets):
        with st.expander(f"{snippet['title']}"):
            col1, col2 = st.columns([4, 1])

            with col1:
                new_title = st.text_input(
                    "Title",
                    value=snippet["title"],
                    key=f"title_{idx}",
                )
                new_content = st.text_area(
                    "Content",
                    value=snippet["content"],
                    height=150,
                    key=f"content_{idx}",
                )

            with col2:
                if st.button("Edit", key=f"update_{idx}"):
                    st.session_state.knowledge_snippets[idx]["title"] = new_title
                    st.session_state.knowledge_snippets[idx]["content"] = new_content
                    st.success("Knowledge updated.")

                if st.button("Delete", key=f"delete_{idx}"):
                    st.session_state.knowledge_snippets.pop(idx)
                    st.rerun()

    st.subheader("Add New Knowledge")

    st.text_input("Title for new Knowledge", key="new_title")
    st.text_area("Content for new Knowledge", height=150, key="new_content")

    st.button("Add Knowledge", on_click=add_snippet, icon=":material/add:")
