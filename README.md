# Customer Support Multi-Agent Chatbot

A Streamlit conversational chatbot that routes company-support requests to a
specialist department. It uses conversation history to understand follow-up
questions and redirects requests outside its support scope.

## Supported topics

- **IT:** computers, software, internet, VPN, accounts, email, networks, and
  technical troubleshooting
- **HR:** leave, attendance, employee policies, benefits, onboarding, and
  resignation
- **Finance:** payroll, salary, reimbursements, expenses, invoices, and tax
  documents
- **Administration:** office facilities, ID cards, transportation, parking,
  maintenance, and supplies
- **Sales:** products, pricing, quotations, discounts, availability, and
  purchases
- **Legal:** contracts, compliance, company policies, and legal documents

The chatbot is intended for company-support questions only. Unrelated requests
receive a brief redirection rather than being answered by a department agent.
The General Support agent handles only company-support questions that do not
clearly fit one of the specialist departments.

## Requirements

- Python 3.10 or later
- An OpenAI API key with access to the `gpt-4o` model

## Setup on Windows

Run these commands from the repository folder in PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Create a `.env` file in the repository root and add your API key:

```text
OPENAI_API_KEY=your_openai_api_key
```

Keep the key private and do not commit the `.env` file.

## Start the chatbot

With the virtual environment activated, run:

```powershell
python -m streamlit run app.py
```

Open the local URL printed by Streamlit in your browser. Chat messages are
stored for the current Streamlit session. Use **New conversation** in the
sidebar to clear the current chat.

## Project files

- `app.py` — Streamlit chat interface and session chat history
- `support_system.py` — context-aware routing and department response flow
- `agents.py` — department agents, router, and their support-scope rules
- `config.py` — loads and validates the OpenAI API key
- `requirements.txt` — Python dependencies
