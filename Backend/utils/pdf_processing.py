import fitz


def extract_text_from_pdf(pdf_path):
    doc=fitz.open(pdf_path)
    text_chunks=[]

    for page in doc:
        text=page.get_text("text")
        if text:
            text_chunks.append(text)
    print(text_chunks)
    return text_chunks