import streamlit as st
from docxtpl import DocxTemplate
import os
import tempfile
import subprocess

TEMPLATE = "contract_template(1).docx"

st.set_page_config(page_title="Contract Generator", page_icon="📄", layout="centered")

st.title("📄 Demo: Gerador de contractos – SANO DIA (SU), SA")
st.markdown("Fill in the details below to generate a ready-to-sign contract (DOCX or PDF).")

# Input form
with st.form("contract_form"):
    st.subheader("Employer Details")
    employer_name = st.text_input("Employer Name", "SANO DIA (SU), SA")
    employer_nif = st.text_input("Employer NIF", "123456789")
    employer_address = st.text_input("Employer Address", "Luanda, Angola")
    representative_name = st.text_input("Representative Name", "João Silva")

    st.subheader("Employee Details")
    employee_name = st.text_input("Employee Name")
    employee_id = st.text_input("Employee ID")
    employee_id_issue_date = st.text_input("ID Issue Date (dd/mm/yyyy)")
    employee_id_expiry = st.text_input("ID Expiry Date (dd/mm/yyyy)")
    employee_address = st.text_input("Employee Address")

    st.subheader("Contract Details")
    job_title = st.text_input("Job Title", "Assistente de Produção")
    start_date = st.text_input("Start Date", "11 de Junho de 2024")
    salary = st.text_input("Salary", "AOA 115.000,00")
    salary_number = st.text_input("Salary (por extenso)", "Cento e Quinze Mil Kwanzas")
    bank_name = st.text_input("Bank Name", "Banco Angolano de Investimento")
    iban = st.text_input("IBAN")

    work_hours = st.text_input("Work Hours", "54 horas por semana")
    annual_vacation_days = st.text_input("Vacation Days", "22")
    trial_period_days = st.text_input("Trial Period (days)", "60")
    contract_date_local = st.text_input("Contract Date & Location", "Luanda, aos 23 de Setembro de 2025")

    submitted = st.form_submit_button("Generate Contract")

if submitted:
    context = {
        "employer_name": employer_name,
        "employer_nif": employer_nif,
        "employer_address": employer_address,
        "representative_name": representative_name,
        "employee_name": employee_name,
        "employee_id": employee_id,
        "employee_id_issue_date": employee_id_issue_date,
        "employee_id_expiry": employee_id_expiry,
        "employee_address": employee_address,
        "job_title": job_title,
        "start_date": start_date,
        "salary": salary,
        "salary_number": salary_number,
        "bank_name": bank_name,
        "iban": iban,
        "work_hours": work_hours,
        "annual_vacation_days": annual_vacation_days,
        "trial_period_days": trial_period_days,
        "contract_date_local": contract_date_local,
        "governing_law": "Lei Geral do Trabalho, Lei n.º 12/23",
        "signature_employer": "___________________",
        "signature_employee": "___________________"
    }

    # Temporary directory for file generation
    with tempfile.TemporaryDirectory() as tmpdir:
        tpl = DocxTemplate(TEMPLATE)
        tpl.render(context)
        docx_path = os.path.join(tmpdir, f"CONTRACT_{employee_name or 'employee'}.docx")
        tpl.save(docx_path)

        # PDF conversion (optional, requires LibreOffice in Streamlit Cloud)
        pdf_path = None
        try:
            subprocess.run([
                "libreoffice", "--headless", "--convert-to", "pdf",
                "--outdir", tmpdir, docx_path
            ], check=True)
            pdf_path = docx_path.replace(".docx", ".pdf")
        except Exception:
            pass

        # Download buttons
        with open(docx_path, "rb") as f:
            st.download_button("⬇️ Download DOCX", f, file_name=os.path.basename(docx_path))

        if pdf_path and os.path.exists(pdf_path):
            with open(pdf_path, "rb") as f:
                st.download_button("⬇️ Download PDF", f, file_name=os.path.basename(pdf_path))


