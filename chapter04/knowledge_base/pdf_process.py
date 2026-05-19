import re
import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF file.
    
    Args:
        pdf_path (str): The path to the PDF file.
    Returns:
        str: The extracted text from the PDF file.
    """
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
        return text
    

def clean_text(text):
    """Cleans the extracted text and fix number issues."""
    #fix number issues
    #1.fix numbers with points, e.g., 2 . 5 -> 2.5, 1 . 0 -> 1.0
    text = re.sub(r'(\d)\s*\.\s*(\d)', r'\1.\2', text)
    #2.fix numbers with spaces, e.g., 1 000 -> 1000, 2 500 -> 2500
    text = re.sub(r'(\d)\s+(\d)', r'\1\2', text)
    
    #clean the text
    text = re.sub(r'\s+', ' ', text)  # Replace multiple whitespace with a single space
    #remove useless characters, e.g., \n, \t, etc.
    text = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9.,;:!?()\- ]+', ' ', text)

    return  text

def split_text_into_chunks(text, chunk_size=500, overlap=50):
    """
    split the cleaned text into chunks
    and supose overlap between chunks is 50 characters to maintain context."""
    chunk_overlap = overlap if overlap < chunk_size else 0
    #1.split the text into sentences
    # to split the text with common sentence delimiters, e.g., ., !, ?, etc.
    sentence_parts = re.split(r'(?<=[.!?])\s+', text)

    # clean the sentences and remove empty sentences
    sentences = []
    for part in sentence_parts:
        cleaned_sentence = part.strip()
        if cleaned_sentence:
            sentences.append(cleaned_sentence)
    

    #2.split the sentences into chunks
    chunks = []
    current_chunk = ""
    current_len = 0

    #build chunks by adding sentences until the chunk size is reached
    for sent in sentences:
        sent_len = len(sent)
        if current_len + sent_len > chunk_size and current_chunk:
            if chunk_overlap > 0:
                #add last N characters of the current chunk to the next chunk to maintain context
                overlap = current_chunk[-chunk_overlap:]
            else:
                #dosen't need to maintain context, so no overlap
                overlap = ""
            
            chunks.append(current_chunk)
            current_chunk = overlap + sent#start a new chunk with the current sentence, and add the overlap if needed
            current_len = len(current_chunk)
        else:
            current_chunk += sent +"。"
            current_len = len(current_chunk)

    #add the last chunk if it exists
    if current_chunk:
        chunks.append(current_chunk)
    return chunks


if __name__ == "__main__":
    with open("第1章 自然语言处理概述.pdf", 'rb') as f:
        text = extract_text_from_pdf(f)
    cleaned_text = clean_text(text)
    chunks = split_text_into_chunks(cleaned_text)
    print(f"have split the text into {len(chunks)} chunks., and the first chunk is: {chunks[0]}")
