import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file")

client = genai.Client(api_key=api_key)


def generate_legal_document(document_type, details):

    prompt = f"""
You are an AI legal document drafting assistant.

Create a structured draft legal document based on the information provided.

Document Type:
{document_type}

User Details:
{details}

Requirements:
1. Use clear and professional legal-document formatting.
2. Include appropriate headings and sections.
3. Do not invent important personal or legal facts.
4. Use placeholders such as [NAME], [DATE], or [ADDRESS] when information is missing.
5. Keep the document easy for the user to review and edit.
6. Add a short note at the end saying that the document should be reviewed by a qualified legal professional before use.

Generate only the document draft.
"""

    interaction = client.interactions.create(
        model="gemini-3.8-flash",
        input=prompt,
        timeout=30
    )

    return interaction.output_text