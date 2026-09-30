import os
import time

from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
mock_ai = os.getenv("MOCK_AI", "false").lower() == "true"

client = None

if not mock_ai:
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in .env file")

    client = genai.Client(api_key=api_key)


def generate_legal_document(document_type, details):

    # ---------------------------------
    # MOCK AI MODE
    # ---------------------------------
    if mock_ai:
        return f"""{document_type.upper()}

NON-DISCLOSURE AGREEMENT

PARTIES
-------

This agreement is entered into based on the following information:

{details}

1. PURPOSE
----------

The parties intend to protect confidential information shared between them
for the purpose described in the provided details.

2. CONFIDENTIAL INFORMATION
---------------------------

Confidential information includes business, technical, commercial,
financial, and other information identified by the parties as confidential.

3. CONFIDENTIALITY OBLIGATION
-----------------------------

The receiving party shall use reasonable care to protect confidential
information and shall not disclose such information to unauthorized persons.

4. CONFIDENTIALITY PERIOD
-------------------------

The confidentiality period shall be based on the period specified by the
parties in the provided details.

5. RETURN OF INFORMATION
------------------------

Upon request, confidential materials should be returned or securely
disposed of, subject to applicable legal requirements.

6. GOVERNING LAW
----------------

[TO BE COMPLETED]

7. SIGNATURES
-------------

Party A: [NAME]

Signature: ______________________

Date: [DATE]


Party B: [NAME]

Signature: ______________________

Date: [DATE]


IMPORTANT NOTICE
----------------

This is an AI-generated draft for informational purposes only.
It should be reviewed and customized by a qualified legal professional
before being relied upon or used.
"""

    # ---------------------------------
    # REAL GEMINI MODE
    # ---------------------------------

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
        model=os.getenv("GEMINI_MODEL", "gemini-3.8-flash"),
        input=prompt,
        background=True
    )

    print(f"Background interaction started: {interaction.id}")
    print(f"Initial status: {interaction.status}")

    while True:

        result = client.interactions.get(interaction.id)

        print(f"Current status: {result.status}")

        if result.status == "completed":
            return result.output_text

        if result.status == "failed":
            raise RuntimeError(
                f"Gemini interaction failed: {result.error}"
            )

        time.sleep(5)