import streamlit as st
from funcs import queries

st.title("Demo: vectology-ng")

api_status = queries.ping()

st.write(f"API connected: {api_status}")

st.caption("""
How to use
- First, search for an entity from a dictionary
- Then paste the entity's id and dictionary into the search form to get matched entities
""")


with st.form("entity_search"):
    st.header("Search for an entity")

    query = st.text_input(label="search for a label")

    dictionary = st.selectbox(
        label="choose dictionary",
        options=("hpo", "icd10", "ukbiobank", "opengwas"),
    )
    entity_search_form_submit = st.form_submit_button("Confirm")


if entity_search_form_submit:
    st.write("dictionary", dictionary)
    st.write("query", query)
    entity_search_results = queries.search_entity(q=query, dictionary=dictionary)
    if entity_search_results:
        st.subheader("Results")
        st.json(entity_search_results)
