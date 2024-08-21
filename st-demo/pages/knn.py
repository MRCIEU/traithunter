import streamlit as st
from funcs import queries

with st.form("entity_knn"):
    st.header("k-Nearest Neighbour search for matched terms")

    entity_id = st.text_input(label="Paste the ID of the query entity here")

    dictionary = st.selectbox(
        label="choose the dictionary of the entity of interest",
        options=("hpo", "icd10", "ukbiobank", "opengwas"),
    )

    dictionary_to_query = st.selectbox(
        label="choose the dictionary of the entities you want to search for",
        options=("hpo", "icd10", "ukbiobank", "opengwas"),
    )

    embedding_type = st.selectbox(
        label="choose type of large language model embeddings",
        options=("bge", "llama3"),
    )

    param_k = st.slider(
        label="Top K neighbours to search (which usually returns K results)",
        value=15,
        min_value=5,
        max_value=40,
    )

    entity_knn_form_submit = st.form_submit_button("Confirm")


    if entity_knn_form_submit:
        st.write("id", entity_id)
        st.write("dictionary", dictionary)
        st.write("dictionary_to_query", dictionary_to_query)
        st.write("embedding_type", embedding_type)
        st.write("param_k", param_k)
        knn_results = queries.knn(id=entity_id, dictionary=dictionary, dictionary_to_query=dictionary_to_query, embedding_type=embedding_type, k=param_k)
        if knn_results:
            st.json(knn_results)
