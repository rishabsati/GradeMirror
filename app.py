import os
import json
import streamlit as st

st.set_page_config(page_title="GradeMirror", page_icon="📚", layout="wide")

# Make the API key available to the Anthropic client locally AND on Streamlit Cloud.
try:
    os.environ["ANTHROPIC_API_KEY"] = st.secrets["ANTHROPIC_API_KEY"]
except Exception:
    pass

import core

# Each visitor gets their own private, in-session memory — no one shares data.
if "mistakes" not in st.session_state:
    st.session_state.mistakes = []

with st.sidebar:
    st.title("📚 GradeMirror")
    st.caption("Learn from your own mistakes.")
    page = st.radio("Go to", ["Add feedback", "My patterns", "Pre-submission checklist"])

    st.divider()
    mistakes = st.session_state.mistakes
    assignments = sorted(set(m["assignment"] for m in mistakes))
    st.metric("Mistakes tracked", len(mistakes))
    st.metric("Assignments", len(assignments))

    st.divider()
    st.caption("Your data stays private to you. Save it to keep it across visits.")
    st.download_button(
        "⬇️ Download my data",
        data=json.dumps(st.session_state.mistakes, indent=2),
        file_name="grademirror_data.json",
        mime="application/json",
    )
    restore = st.file_uploader("Restore saved data", type="json")
    if restore and st.button("Load this file"):
        try:
            st.session_state.mistakes = json.loads(restore.read().decode("utf-8"))
            st.success("Loaded your saved data!")
        except Exception:
            st.error("That file couldn't be read. Make sure it's a data file you downloaded from GradeMirror.")

if page == "Add feedback":
    st.header("Add feedback from a graded assignment")
    assignment = st.text_input("Assignment name", placeholder="e.g. CSE 355 - HW5")
    feedback = st.text_area("Paste the feedback comments", height=200)
    pdf_file = st.file_uploader("Optional: upload the assignment PDF (sharpens the results)", type="pdf")
    if st.button("Extract & save"):
        if assignment and feedback:
            try:
                context = core.read_pdf_text(pdf_file) if pdf_file else ""
                with st.spinner("Extracting mistakes..."):
                    new = core.extract_mistakes(feedback, assignment, context)
                st.session_state.mistakes = core.merge_mistakes(st.session_state.mistakes, new, assignment)
                st.success(f"Saved {len(new)} mistakes from {assignment}.")
                for m in new:
                    st.write(f"- **{m['question']}** · {m['concept']} · -{m['points_lost']} pts · {m['mistake']}")
            except Exception as e:
                st.error("Something went wrong while processing that feedback. Please try again.")
                with st.expander("Technical details"):
                    st.write(str(e))
        else:
            st.warning("Please fill in both the assignment name and the feedback.")

elif page == "My patterns":
    st.header("Your recurring weaknesses")
    if st.button("Find my patterns"):
        if st.session_state.mistakes:
            try:
                with st.spinner("Analyzing your history..."):
                    result = core.find_patterns(st.session_state.mistakes)
                st.markdown(result)
            except Exception as e:
                st.error("Couldn't analyze your patterns right now. Please try again.")
                with st.expander("Technical details"):
                    st.write(str(e))
        else:
            st.info("Add feedback from a couple of assignments first.")

elif page == "Pre-submission checklist":
    st.header("Pre-submission checklist")
    upcoming = st.text_input("What assignment are you about to submit?",
                             placeholder="e.g. CSE 355 HW6: Turing machines and decidability")
    if st.button("Generate checklist"):
        if not upcoming:
            st.warning("Describe the assignment first.")
        elif not st.session_state.mistakes:
            st.info("Add feedback from a couple of assignments first.")
        else:
            try:
                with st.spinner("Building your checklist..."):
                    result = core.make_checklist(upcoming, st.session_state.mistakes)
                st.markdown(result)
            except Exception as e:
                st.error("Couldn't build your checklist right now. Please try again.")
                with st.expander("Technical details"):
                    st.write(str(e))