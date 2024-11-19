from langchain_community.document_loaders import PyPDFLoader


def load_document(file):
    file_path = file.name
    loader = PyPDFLoader(file_path)

    docs = loader.load()

    print(docs)