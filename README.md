\# ⚖️ LegalEase AI



AI-Powered Legal Document Generator



LegalEase AI is an AI-powered application that helps users generate structured draft legal documents from basic user-provided information.



The application uses a Streamlit frontend, FastAPI backend, Gemini AI for document generation, and document utilities for TXT, DOCX, and PDF downloads.



\---



\## 🚀 Features



\- Generate draft legal documents using AI

\- Select different document types

\- Provide custom document details

\- Review and edit generated documents

\- Download documents as:

&#x20; - TXT

&#x20; - DOCX

&#x20; - PDF

\- FastAPI REST API

\- Streamlit user interface

\- Gemini AI integration

\- Environment-variable based API key configuration



\---



\## 📄 Supported Documents



Currently supported document types:



\- Non-Disclosure Agreement (NDA)

\- Employment Contract

\- Residential Lease Agreement



\---



\## 🏗️ System Architecture



```text

User

&#x20; │

&#x20; ▼

Streamlit Frontend

&#x20; │

&#x20; ▼

FastAPI Backend

&#x20; │

&#x20; ├── Gemini AI

&#x20; │

&#x20; └── Document Utilities

&#x20;       ├── TXT

&#x20;       ├── DOCX

&#x20;       └── PDF

