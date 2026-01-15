import asyncio

import streamlit as st

from src.agents import orchestrator_agent

st.set_page_config(page_title="AA-MR", layout="wide")
st.title("AA-MR")
st.divider()
# ---------- sidebar navigation ----------
with st.sidebar:
    st.markdown("### Toolbox")
    report_btn = st.button(
        "Dashboard", key="report_btn", icon=":material/analytics:", width="stretch"
    )
    chat_btn = st.button(
        "Chat", key="chat_btn", icon=":material/chat:", width="stretch"
    )
    swagger_btn = st.button(
        "Gapfilling", key="swagger_btn", icon=":material/mystery:", width="stretch"
    )
    recon_btn = st.button(
        "Model Building", key="recon_btn", icon=":material/graph_3:", width="stretch"
    )

    training_btn = st.button(
        "Knowledge Base",
        key="training_btn",
        icon=":material/neurology:",
        width="stretch",
    )

    if "page" not in st.session_state:
        st.session_state.page = "Chat"

    if chat_btn:
        st.session_state.page = "Chat"
    if swagger_btn:
        st.session_state.page = "Swagger Docs Analyzer"
    if recon_btn:
        st.session_state.page = "Reconaissance agent"
    if report_btn:
        st.session_state.page = "Reports"
    if training_btn:
        st.session_state.page = "Training"

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
            st.markdown(msg["content"])

    # ---------- input ----------
    if prompt := st.chat_input("Ask me anything…"):
        st.session_state.chat_messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # ---------- run agent ----------
        with st.chat_message("assistant"):
            placeholder = st.empty()
            full = ""
            for chunk in orchestrator_agent.run(
                prompt, stream=True, debug_mode=True
            ):  # 2️⃣ streaming straight into UI
                if chunk.content:
                    full += chunk.content
                    placeholder.markdown(full + "▌")
            placeholder.markdown(full)
        st.session_state.chat_messages.append({"role": "assistant", "content": full})

elif page == "Swagger Docs Analyzer":
    st.header("Swagger/OpenAPI Docs Analyzer")
    swagger_file = st.file_uploader(
        "Upload a Swagger/OpenAPI JSON or YAML file", type=["json", "yaml", "yml"]
    )
    if swagger_file is not None:
        try:
            file_bytes = swagger_file.read()
            # Try to decode as UTF-8 text
            content_str = file_bytes.decode("utf-8")

            analyze_prompt = f"Analyze the following Swagger/OpenAPI specification and summarize its endpoints, authentication, and notable features:\n\n{content_str}"
            with st.spinner("Analyzing Swagger/OpenAPI docs..."):
                analyzer = IDORAnalyzer()
                spec = analyzer.analyze_file_bytes(file_bytes)
                st.success("Analysis completed")
                st.markdown(generate_markdown(spec))
        except Exception as e:
            st.error(f"Error reading or analyzing Swagger/OpenAPI file: {e}")

elif page == "Reports":
    import numpy as np
    import pandas as pd
    import plotly.express as px

    st.header("Metabolic Reconstruction Dashboard")

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
    st.header("Reconaissance Agent")
    # ---------- display history ----------
    for msg in st.session_state.recon_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    # ---------- input ----------
    if prompt := st.chat_input("Ask me anything…"):
        st.session_state.recon_messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # ---------- run agent ----------
        async def async_run_agent(prompt):
            full = ""
            placeholder = st.empty()
            async for chunk in recon_agent.arun(prompt, stream=True, debug_mode=True):
                if chunk.content:
                    full += chunk.content
                    placeholder.markdown(full + "▌")
            placeholder.markdown(full)
            return full

        with st.chat_message("assistant"):
            full = asyncio.run(async_run_agent(prompt))
        st.session_state.recon_messages.append({"role": "assistant", "content": full})

elif page == "Training":
    st.header("Knowledge Base - Manage Knowledge Snippets")

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
                    st.success("Snippet updated.")

                if st.button("Delete", key=f"delete_{idx}"):
                    st.session_state.knowledge_snippets.pop(idx)
                    st.rerun()

    st.subheader("Add New Knowledge Snippet")

    st.text_input("Title for new snippet", key="new_title")
    st.text_area("Content for new snippet", height=150, key="new_content")

    st.button("Add Knowledge", on_click=add_snippet, icon=":material/add:")
