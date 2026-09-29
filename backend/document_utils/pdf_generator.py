from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors
from io import BytesIO


def create_pdf_file(document):
    output = BytesIO()

    pdf = SimpleDocTemplate(
        output,
        pagesize=A4,
        rightMargin=50,
        leftMargin=50,
        topMargin=50,
        bottomMargin=50
    )

    styles = getSampleStyleSheet()

    title_style = styles["Title"]
    title_style.alignment = TA_CENTER

    body_style = styles["BodyText"]
    body_style.leading = 16

    story = []

    for line in document.splitlines():

        line = line.strip()

        if not line:
            story.append(Spacer(1, 10))
            continue

        if line.startswith("#"):
            heading = line.lstrip("#").strip()

            story.append(
                Paragraph(
                    heading,
                    styles["Heading1"]
                )
            )

            story.append(Spacer(1, 8))

        else:
            safe_line = (
                line
                .replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
            )

            story.append(
                Paragraph(
                    safe_line,
                    body_style
                )
            )

            story.append(Spacer(1, 5))

    pdf.build(story)

    output.seek(0)

    return output.getvalue()