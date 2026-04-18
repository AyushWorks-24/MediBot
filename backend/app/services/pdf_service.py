import fitz
from utils.logger import logger

def extract_text_from_pdf(pdf_bytes:bytes)->str:
    doc=fitz.open(stream=pdf_bytes,filetype="pdf")
    pages_text=[]

    for page_num in range(len(doc)):
        page=doc[page_num]
        text=page.get_text("text")
        pages_text.append(f"[Page{page_num+1}]\n{text}")

    full_text="\n\n".join(pages_text)
    logger.info(
        f"Pdf extracted:{len(doc)} pages | {len(full_text)} characters"
    )    
    return full_text