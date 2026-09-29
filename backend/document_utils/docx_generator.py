from docx import Document


def create_docx_file(document):
    doc = Document()

    for line in document.splitlines():

        line = line.strip()

        if not line:
            doc.add_paragraph()
            continue

        if line.startswith("#"):
            heading = line.lstrip("#").strip()
            doc.add_heading(heading, level=1)

        else:
            doc.add_paragraph(line)

    return doc