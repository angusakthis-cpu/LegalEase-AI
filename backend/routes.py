from fastapi import APIRouter
from fastapi.responses import Response
from pydantic import BaseModel
from io import BytesIO

from backend.ai_core.gemini_generator import generate_legal_document
from backend.document_utils.docx_generator import create_docx_file
from backend.document_utils.pdf_generator import create_pdf_file


router = APIRouter()


class DocumentRequest(BaseModel):
    document_type: str
    details: str


class DocxRequest(BaseModel):
    document: str


class PdfRequest(BaseModel):
    document: str


@router.post("/generate-document")
def generate_document(request: DocumentRequest):

    document = generate_legal_document(
        request.document_type,
        request.details
    )

    return {
        "success": True,
        "document_type": request.document_type,
        "document": document
    }


@router.post("/download-docx")
def download_docx(request: DocxRequest):

    doc = create_docx_file(request.document)

    output = BytesIO()
    doc.save(output)

    return Response(
        content=output.getvalue(),
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={
            "Content-Disposition": 'attachment; filename="LegalEase_Document.docx"'
        }
    )


@router.post("/download-pdf")
def download_pdf(request: PdfRequest):

    pdf_data = create_pdf_file(request.document)

    return Response(
        content=pdf_data,
        media_type="application/pdf",
        headers={
            "Content-Disposition": 'attachment; filename="LegalEase_Document.pdf"'
        }
    )