import streamlit as st
from funcs import queries

st.title("Demo: trait phenotype mapping")

api_status = queries.ping()
API_URL_EXTERNAL = "http://ieu-db-inferface.epi.bris.ac.uk:8645"

st.caption(f"""
API:
- url: {API_URL_EXTERNAL}
- connection status: {api_status}
"""
)

st.caption("""
What is this
- This is a (tech demo of) trait mapping via Large Language Model (LLM) embeddings
for curated dictionaries: HPO, ICD10, UK Biobank, OpenGWAS, etc
- The embeddings have been pre-computed from the member `entity` terms from those `dictionaries`
- The LLMs in use are:
  - BGE (https://huggingface.co/BAAI/bge-base-en-v1.5); Version: bge-base-en-v1.5; Dimention: 768
  - LLaMA 3 (https://huggingface.co/meta-llama/Meta-Llama-3-8B; via https://huggingface.co/McGill-NLP/LLM2Vec-Meta-Llama-3-8B-Instruct-mntp); Version: LLM2Vec-Meta-Llama-3-8B-Instruct-mntp; Dimension: 4096

How to use
- First, search for an entity from a dictionary
  - And pick an entity and copy its `id` field
- Go to the knn tab page on the sidebar
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
