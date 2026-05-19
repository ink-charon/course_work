"""PDF Handler for processing PDF files and extracting text content."""

import os
from knowledge_base.pdf_process import extract_text_from_pdf, clean_text, split_text_into_chunks
from ui.cli_utils import print_section_header

def get_pdf_path():
    """to get path of the PDF file from the user.
    Returns:
        str: The path to the PDF file, or None if the input is invalid.
    """
    print_section_header("upload PDF file")
    print("Please enter the path to the PDF file you want to upload: ")
    print("or enter file name if the file is in the current directory.")
    print()

    file_path = input("PDF file path: ").strip().strip('"').strip("'")
    # Validate the input
    if not file_path:
        print("No file path provided. Please try again.")
        return None
    # Check if the file exists
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}. Please check the path and try again.")
        return None
    # Check if the file is a PDF
    if not file_path.lower().endswith('.pdf'):
        print("Invalid file type. Please upload a PDF file.")
        return None
    
    return file_path

def process_pdf(file_path):
    """"Processes the PDF file
    Args:
        file_path (str): The path to the PDF file.
        
    Returns:
        chunks processed from the PDF file.
        if faile to process the PDF file, returns None.
    """
    print(f"\nProcessing PDF file: {file_path}...")

    #1. Extract text from the PDF file
    try:
        with open(file_path, 'rb') as f:
            raw_text = extract_text_from_pdf(f)
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        input("\nPress Enter to continue...")
        return None
    
    #2. Clean the extracted text
    print("Cleaning extracted text...")
    cleaned_text = clean_text(raw_text)

    #3. Split the cleaned text into chunks
    print("Splitting text into chunks...")
    chunks = split_text_into_chunks(cleaned_text)
    print(f"have split the text into {len(chunks)} chunks.")

    return chunks


def upload_pdf(vector_store):
    """uplaod pdf file to the knowledge base.
    
    args:
        vector_store: the vector store to store the processed chunks.
    
    returns:
        tuple: (file_name, did successfully upload the PDF file or not)
    """
    #get pdf file path
    file_path = get_pdf_path()
    if not file_path:
        return None, False
    #chunks processed
    chunks = process_pdf(file_path)
    if not chunks:
        return None, False
    
    #4.vectorize the chunks and store them in the vector store
    print("Vectorizing chunks and storing in the vector store...")
    try:
        vector_store.clear_collection()  # Clear existing data in the vector store
        vector_store.add_text_chunks(chunks)
    except Exception as e:
        print(f"Error vectorizing chunks or storing in vector store: {e}")
        input("\nPress Enter to continue...")
        return None, False
    #get file_name from file_path
    file_name = os.path.basename(file_path)

    #screen output
    print(f"\nhave successfully loaded knowledge_base! ({file_name})")
    print(f"file_name: {file_name}")
    print(f"nums of chunks: {len(chunks)}")
    input("\nPress Enter to continue...")

    return file_name, True
