import streamlit as st
from pdf_logic import read_and_extract_text
from embedding_logic import encode_paragraphs, tokenize_paragraphs, generate_mappings_and_embeddings, initialize_qdrant_client, upsert_data_to_qdrant, search_in_qdrant

NUM2EMOJI = {1:"1️⃣", 2:"2️⃣", 3:"3️⃣", 4:"4️⃣", 5:"5️⃣"}

# Caching the Qdrant client to improve performance
@st.cache_resource
def get_qdrant_client():
    return initialize_qdrant_client()

# Caching the process of reading and extracting text from PDF, and processing content
@st.cache_data
def process_pdf(file_content, _qdrant_client):
    paragraphs = read_and_extract_text(file_content)
    embeddings = encode_paragraphs(paragraphs)
    tokenized_paragraphs = tokenize_paragraphs(paragraphs)
    ids, texts, vectors = generate_mappings_and_embeddings(paragraphs, tokenized_paragraphs, embeddings)
    paragraph_ids = list(range(len(paragraphs)))
    upsert_data_to_qdrant(_qdrant_client, ids, texts, vectors, paragraph_ids)
    return paragraphs#, ids, texts, vectors, paragraph_ids


@st.cache_data
def get_search_results(_qdrant_client, query, paragraphs, limit=5):
    results = search_in_qdrant(_qdrant_client, query)
    return [paragraphs[res.id] for res in results][:limit]


def main():
    st.header("PDF Content Search App", divider="blue")
    st.sidebar.subheader("Upload & Search", divider='blue')
    uploaded_file = st.sidebar.file_uploader("Choose a PDF file", type="pdf")
    query = st.sidebar.text_input("Enter your search query", "")
    search_button = st.sidebar.button("Search")
    tab_only_results, tab_highlighted = st.tabs(["Only Search Results", "Full Content with Highlighted Search Results"])

    if uploaded_file and query and search_button:
        with st.spinner("Processing PDF and performing search..."):
            file_content = uploaded_file.getvalue()
            qdrant_client = get_qdrant_client()
            paragraphs = process_pdf(file_content, qdrant_client)
            results = get_search_results(qdrant_client, query, paragraphs, limit=5)
            
            if results:
                for i, res in enumerate(results, start=1):
                    tab_only_results.markdown(f"👉{NUM2EMOJI[i]}: {res}\n")
                    tab_only_results.divider()
                for paragraph in paragraphs:
                    if paragraph in results:
                        rank = results.index(paragraph) + 1
                        tab_highlighted.markdown(f"👉{NUM2EMOJI[rank]}: :violet[{paragraph}]\n")
                    else:
                        tab_highlighted.markdown(paragraph)
            else:
                st.error("No results found.")

if __name__ == "__main__":
    main()
