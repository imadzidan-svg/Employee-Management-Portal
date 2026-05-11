from PyPDF2 import PdfReader


def extract_text_from_pdf(
    file_path
):

    reader = PdfReader(file_path)

    full_text = []

    for page in reader.pages:

        text = page.extract_text()

        if text:

            full_text.append(text)

    return '\n'.join(full_text)