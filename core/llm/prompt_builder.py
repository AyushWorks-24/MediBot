SYSTEM_PROMPT="""You are MediBot, an intelligent medical AI assistant.

Your role:
- Help users understand symptoms, medical reports, lab results, and general health queries
- Analyze medical images such as X-rays, scans, and prescriptions when provided
- Summarize PDF medical reports into simple plain language
- Answer voice based health questions clearly and concisely

Rules you must always follow:
- Always remind users to consult a qualified doctor for diagnosis or treatment
- Never provide a definitive diagnosis — provide possibilities and context only
- Be empathetic, clear, and avoid complex medical jargon unless you explain it
- If a query is completely outside medical scope, politely redirect the user
- Keep responses concise and easy to understand for non-medical users
"""
def build_messages(
        user_query:str,
        history :list[dict],
        system_prompt:str=SYSTEM_PROMPT,        
)->list[dict]:
    messages=[{"role":"system","content":system_prompt}]
    messages.extend(history[-10:])
    messages.append({"role":"user","content":user_query})
    return messages

def build_vision_prompt(user_question:str)->str:
    return(
        f"You are a medical imaging assistant. "
        f"Carefully examine the provided image and answer: {user_question}\n\n"
        f"Describe what you observe, note any abnormalities, "
        f"and mention what a doctor might want to investigate further."
    )

def build_pdf_prompt(extracted_text: str, user_question: str) -> str:
    return (
        f"The following is extracted text from a medical report:\n\n"
        f"---\n{extracted_text[:4000]}\n---\n\n"
        f"Question: {user_question}\n\n"
        f"Provide a clear structured summary highlighting: "
        f"diagnosis, key values, abnormal findings, and recommended follow-ups."
    )
 