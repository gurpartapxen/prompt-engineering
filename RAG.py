import os
import fitz  # PyMuPDF
from tkinter import Tk
from tkinter.filedialog import askopenfilename

from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA

# 🔑 Set your Google Gemini API key
os.environ["GOOGLE_API_KEY"] = "AIzaSyCHuHUcPCevRz-75vZIbPaHJ7GsiC9Hc7A"

def extract_pdf_text(pdf_path):
    doc = fitz.open(pdf_path)
    full_text = ""
    for page in doc:
        full_text += page.get_text()
    return full_text

def create_chunks(text):
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    return splitter.create_documents([text])

def embed_documents(documents):
    embedding = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    return FAISS.from_documents(documents, embedding)

def init_llm():
    return ChatGoogleGenerativeAI(model="models/gemini-1.5-flash", temperature=0)

def build_qa_chain(vectorstore):
    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 4})
    llm = init_llm()
    chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True
    )
    return chain

def select_pdf_file():
    root = Tk()
    root.withdraw()  # hide the tkinter root window
    file_path = askopenfilename(
        title="Select PDF File",
        filetypes=[("PDF files", "*.pdf")]
    )
    root.destroy()
    return file_path

def main(pdf_path):
    print("📄 Extracting PDF text...")
    text = extract_pdf_text(pdf_path)

    print("\n📚 Splitting text into chunks...")
    chunks = create_chunks(text)

    print("\n🔍 Embedding and indexing with FAISS...")
    vectorstore = embed_documents(chunks)

    print("\n✅ Ready! You can now ask questions about the PDF content.\n")
    print("🧠 Context Preview:")
    print("-" * 60)
    print(text[:2000])
    print("-" * 60)

    qa_chain = build_qa_chain(vectorstore)

    while True:
        query = input("\n❓ Ask your question (or type 'exit'): ")
        if query.lower() == 'exit':
            break
        result = qa_chain.invoke({"query": query})
        print(f"\n🤖 Answer: {result['result']}\n")
        print("📚 Source Snippets:")
        for doc in result['source_documents']:
            print("-" * 40)
            print(doc.page_content[:500])  # show first 500 chars of source

if __name__ == "__main__":
    print("📤 Please select a PDF file from the popup window...")
    pdf_path = select_pdf_file()

    if not pdf_path or not os.path.exists(pdf_path):
        print("❌ No file selected or file not found. Exiting.")
    else:
        main(pdf_path)