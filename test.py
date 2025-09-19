# import os
# from pathlib import Path
# from src.document_analyzer.data_ingestion import DocumentHandler       # Your PDFHandler class
# from src.document_analyzer.data_analysis import DocumentAnalyzer  # Your DocumentAnalyzer class

# # Path to the PDF you want to test
# PDF_PATH = r"D:\llm_live_projects\document_portel\notebook\data\sample.pdf"

# # PDF_PATH=r"D:\llm_live_projects\document_portel\data\document_compare\Long_Report_V1.pdf"

# # Dummy file wrapper to simulate uploaded file (Streamlit style)



# """
# PDF Ingestion and Analysis

# classes to ingest a PDF document, extract its text, and perform metadata analysis.

# Workflow: Ingest a pdf and anayze and extract text using llm-based analysis and print Json results. 
   


# """
# class DummyFile:
#     '''This class converts pdf path to upload a dummy file'''
#     def __init__(self, file_path):
#         self.name = Path(file_path).name
#         self._file_path = file_path

#     def getbuffer(self):
#         return open(self._file_path, "rb").read()

# def main():
#     try:
#         # ---------- STEP 1: DATA INGESTION ----------
#         print("Starting PDF ingestion...")
#         dummy_pdf = DummyFile(PDF_PATH)

#         handler = DocumentHandler(session_id="test_ingestion_analysis")  # To save session with given name 
        
#         saved_path = handler.save_pdf(dummy_pdf)   # To save PDF  
#         print(f"PDF saved at: {saved_path}")

#         text_content = handler.read_pdf(saved_path)
#         print(f"Extracted text length: {len(text_content)} chars\n")

#         # ---------- STEP 2: DATA ANALYSIS ----------
#         print("Starting metadata analysis...")
#         analyzer = DocumentAnalyzer()  # Loads LLM + parser
        
#         analysis_result = analyzer.analyze_document(text_content) # To anayze document and provides meta data with structured format 

#         # ---------- STEP 3: DISPLAY RESULTS ----------
#         print("\n=== METADATA ANALYSIS RESULT ===")
#         for key, value in analysis_result.items():
#             print(f"{key}: {value}")

#     except Exception as e:
#         print(f"Test failed: {e}")

# if __name__ == "__main__":
#     main()

# import io
# from pathlib import Path
# from src.document_compare.data_ingestion import DocumentIngestion
# from src.document_compare.document_comparator import DocumentComparatorLLM

# # ---- Setup: Load local PDF files as if they were "uploaded" ---- #

# def load_fake_uploaded_file(file_path: Path):
#     return io.BytesIO(file_path.read_bytes())  # simulate .getbuffer()

# # ---- Step 1: Save and combine PDFs ---- #
# def test_compare_documents():

#     """
#     This will uses two pdf path and read data and
#     combines to one pdf and this passess to 
#     llm based analysis gives the difference on both  pdf contents

#     """
    
#     # ref_path = Path("D:\llm_live_projects\document_portel\data\document_compare\Long_Report_V1.pdf")
#     # act_path = Path("D:\llm_live_projects\document_portel\data\document_compare\Long_Report_V2.pdf")

#     ref_path = Path(r"D:\llm_live_projects\document_portel\test1.pdf")  # Path of pdf 
#     act_path = Path(r"D:\llm_live_projects\document_portel\test2.pdf")

#     # Wrap them like Streamlit UploadedFile-style
#     class FakeUpload:
#         """
#         Simulate a user-uploaded file (like Streamlit's UploadedFile).
#         """
#         def __init__(self, file_path: Path):
#             self.name = file_path.name
#             self._buffer = file_path.read_bytes()

#         def getbuffer(self):
#             return self._buffer

#     # Instantiate
#     comparator = DocumentIngestion()    # Save files and combine content 
#     ref_upload = FakeUpload(ref_path)    # Instantiate the fake uploaded files
#     act_upload = FakeUpload(act_path)

#     # Save uploaded PDFs to storage and return saved paths
#     ref_file, act_file = comparator.save_uploaded_files(ref_upload, act_upload)

#      # Combine the contents of both PDFs into a single text for analysis
#     combined_text = comparator.combine_documents()

#     # Keep only the latest 3 sessions to avoid clutter
#     comparator.clean_old_sessions(keep_latest=3)

#     print("\n Combined Text Preview (First 1000 chars):\n")
#     print(combined_text[:1000])

#     # ---- Step 2: Run LLM comparison ---- #
#     llm_comparator = DocumentComparatorLLM()
#     df = llm_comparator.compare_documents(combined_text)
    
#     print("\n Comparison DataFrame:\n")
#     print(df)

# if __name__ == "__main__":
#     test_compare_documents()
    
    

# Testing code for document chat functionality


# import sys
# from pathlib import Path
# from langchain_community.vectorstores import FAISS
# from src.single_document_chat.data_ingestion import SingleDocIngestor
# from src.single_document_chat.retrieval import ConversationalRAG
# from utils.model_loader import ModelLoader

# FAISS_INDEX_PATH = Path("faiss_index")



# def test_conversational_rag_on_pdf(pdf_path:str, question:str):
#     """
#     This function loads or creates a FAISS index for the provided PDF,
#     sets up a retriever, and runs a conversational Retrieval-Augmented 
#     Generation (RAG) query with the given question.
    
#     """
#     try:

#         model_loader = ModelLoader() # model loader for embeddings and LLM
        
#         # Check if FAISS index already exists
#         if FAISS_INDEX_PATH.exists():
#             print("Loading existing FAISS index...")
#             embeddings = model_loader.load_embeddings() # Load embeddings
#             vectorstore = FAISS.load_local(folder_path=str(FAISS_INDEX_PATH), embeddings=embeddings,allow_dangerous_deserialization=True)
#             retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 5}) # This creates retriever from FAISS Vectorstore
#         else:
#             # Step 2: Ingest document and create retriever
#             print("FAISS index not found. Ingesting PDF and creating index...")
#             with open(pdf_path, "rb") as f:
#                 uploaded_files = [f]

#                 # Initialize the document ingestion class for a single document
#                 ingestor = SingleDocIngestor()

#                 #  This will process the file, extract text, and prepare a retriever (e.g., for search or embeddings)
#                 retriever = ingestor.ingest_files(uploaded_files)
                
#         print("Running Conversational RAG...")
#         session_id = "test_conversational_rag"
#         rag = ConversationalRAG(retriever=retriever, session_id=session_id)
#         response = rag.invoke(question)
#         print(f"\nQuestion: {question}\nAnswer: {response}")
                    
#     except Exception as e:
#         print(f"Test failed: {str(e)}")
#         sys.exit(1)
    
# if __name__ == "__main__":
#     # Example PDF path and question
#     pdf_path = "D:\\llm_live_projects\\document_portel\\data\single_document_chat\\NIPS-2017-attention-is-all-you-need-Paper.pdf"
#     question = "What is the significance of the attention mechanism? can you explain it in simple terms?"

#     if not Path(pdf_path).exists():
#         print(f"PDF file does not exist at: {pdf_path}")
#         sys.exit(1)
    
#     # Run the test
#     test_conversational_rag_on_pdf(pdf_path, question)

   

import sys
from pathlib import Path
from src.multi_document_chat.data_ingestion import DocumentIngestor
from src.multi_document_chat.retrieval import ConversationalRAG

def test_document_ingestion_and_rag():
    """
    Test the multi-document ingestion and Conversational RAG pipeline

    This function:
        Loads a list of test documents (PDF, DOCX, TXT, etc.).
        Reads each file in binary mode and stores them in a list.
        Uses DocumentIngestor to process the uploaded files and create a retriever.
        Initializes a ConversationalRAG instance with a session ID and the retriever.
        Sends a sample question to the RAG model and prints the answer.
    
    """
    try:
        test_files = [
            "D:\llm_live_projects\document_portel\data\multi_doc_chat\market_analysis_report.docx",
            "D:\\llm_live_projects\\document_portel\\data\\multi_doc_chat\\state_of_the_union.txt",
            
        ]

        # Check if each file exists, then open it in binary mode
        uploaded_files = []
        for file_path in test_files:
            if Path(file_path).exists():
                uploaded_files.append(open(file_path, "rb"))     # Reading this in binary format and appending 
            else:
                print(f"File does not exist: {file_path}")
                
        if not uploaded_files:
            print("No valid files to upload.")
            sys.exit(1)
        
        # Ingest documents and create a retriever for RAG
        ingestor = DocumentIngestor()
        retriever = ingestor.ingest_files(uploaded_files)
        
        for f in uploaded_files:
            f.close()
        
        # Define a session ID for multi-document conversational context
        session_id = "test_multi_doc_chat"
        
        rag = ConversationalRAG(session_id=session_id, retriever=retriever)
        question = "what is President Zelenskyy said in their speech in parliament?"
        answer=rag.invoke(question)
        print("\n Question:", question)
        print("Answer:", answer)
        if not uploaded_files:
            print("No valid files to upload.")
            sys.exit(1)
    except Exception as e:
        print(f"Test failed: {str(e)}")
        sys.exit(1)
        
if __name__ == "__main__":
    test_document_ingestion_and_rag()


