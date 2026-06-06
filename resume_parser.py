from pypdf import PdfReader

def extract_resume_text(pdf_path):

    print("Opening PDF:", pdf_path)

    reader = PdfReader(pdf_path)

    print("Pages Found:", len(reader.pages))

    text = ""

    for i, page in enumerate(reader.pages):

        print("Reading Page:", i + 1)

        page_text = page.extract_text()

        if page_text:

            text += page_text + "\n"

    print("Extraction Completed")

    return text