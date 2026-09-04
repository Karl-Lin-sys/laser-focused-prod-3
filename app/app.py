import os
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA

def build_qa_chain():
    db_dir = os.path.join(os.path.dirname(__file__), "..", "chroma_db")
    
    # 無料枠を利用するためGemini APIを指定
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vectorstore = Chroma(persist_directory=db_dir, embedding_function=embeddings)
    
    # 軽量かつ高性能なGemini 1.5 Flashモデルを使用
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0)
    
    # 検索チェーンの構築
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
        return_source_documents=True
    )
    return qa_chain

def main():
    print("Initializing RAG system (Powered by Google Gemini)...")
    qa_chain = build_qa_chain()
    print("System ready. Type 'exit' to quit.")
    
    while True:
        query = input("\nQuery: ")
        if query.lower() in ["exit", "quit"]:
            break
            
        if not query.strip():
            continue
            
        try:
            result = qa_chain.invoke({"query": query})
            print("\n--- Answer ---")
            print(result["result"])
            print("--------------")
            
            print("\nSources:")
            for doc in result["source_documents"]:
                print(f"- {doc.metadata.get('source', 'Unknown')}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
