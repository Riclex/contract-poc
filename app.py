import streamlit as st
from docxtpl import DocxTemplate
import os
import tempfile
import subprocess
import streamlit as st
from datetime import datetime

# Configuration
ENABLE_PDF_CONVERSION = False  # Set to True if LibreOffice is available
TEMPLATE = "contract_template (1).docx"

# Page configuration
st.set_page_config(
    page_title="Contract Generator", 
    page_icon="📄", 
    layout="centered"
)

# Styling improvements
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        background-color: #0066cc;
        color: white;
    }
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📄 Demo: Gerador de contractos – SANO DIA (SU), SA")
st.markdown("Preencha os detalhes abaixo para gerar um contrato pronto para assinar (DOCX or PDF).")

# Template validation
if not os.path.exists(TEMPLATE):
    st.error(f"❌ **Erro Crítico:** Ficheiro modelo '{TEMPLATE}' não encontrado!")
    st.info("📋 Por favor, coloque o ficheiro 'contract_template.docx' no mesmo diretório que este script.")
    st.stop()
    
# Input form
with st.form("contract_form"):
    st.subheader("Dados da Entidade Empregadora")
    col1, col2 = st.columns(2)
    with col1:
        employer_name = st.text_input(
            "Nome da Empresa *", 
            placeholder="Sociedade Agricola, SA"
        )
        employer_nif = st.text_input(
            "NIF *", 
            placeholder="123456789"
        )
    with col2:
        employer_address = st.text_input(
            "Morada *", 
            placeholder="Luanda, Angola"
        )
        representative_name = st.text_input(
            "Nome do Representante *", 
            placeholder="João Silva"
        )
        
    st.divider()
    st.subheader("Dados do Trabalhador")
    col1, col2 = st.columns(2)
    with col1:
        employee_name = st.text_input("Nome Completo *", placeholder="Maria Santos")
        employee_id = st.text_input("Número do BI *", placeholder="000000000LA000")
        employee_address = st.text_input("Morada *", placeholder="Luanda, Viana")
        
    with col2:
        employee_id_issue_date = st.text_input(
            "Data de Emissão do BI *", 
            placeholder="01/01/2020"
        )
        employee_id_expiry = st.text_input(
            "Data de Validade do BI *", 
            placeholder="01/01/2030"
        )
        iban = st.text_input("IBAN *", placeholder="AO06 0000 0000 0000 0000 0000 0")

    st.divider()
    st.subheader("Detalhes do Contrato")
    
    col1, col2 = st.columns(2)
    with col1:
        job_title = st.text_input("Cargo *", placeholder="Assistente de Produção")
        start_date = st.text_input(
            "Data de Início *", 
            placeholder="11 de Junho de 2024"
        )
        salary = st.text_input("Salário (valor) *", placeholder="AOA 115.000,00")
        work_hours = st.text_input(
            "Horário de Trabalho", 
            value="54 horas por semana"
        )
    
    with col2:
        salary_number = st.text_input(
            "Salário (por extenso) *", 
            placeholder="Cento e Quinze Mil Kwanzas"
        )
        bank_name = st.text_input(
            "Banco", 
            placeholder="Banco Angolano de Investimento"
        )
        annual_vacation_days = st.text_input("Dias de Férias Anuais", value="22")
        trial_period_days = st.text_input("Período de Experiência (dias)", value="60")
   
    contract_date_local = st.text_input(
        "Local e Data do Contrato *", 
        placeholder="Luanda, aos 23 de Setembro de 2025"
        )

    st.divider()
    submitted = st.form_submit_button("🚀 Gerar Contrato", use_container_width=True)

# Process form submission
if submitted:
    # Validate required fields
    required_fields = {
        "Nome da Empresa": employer_name,
        "NIF": employer_nif,
        "Morada da Empresa": employer_address,
        "Nome do Representante": representative_name,
        "Nome do Trabalhador": employee_name,
        "Número do BI": employee_id,
        "Data de Emissão do BI": employee_id_issue_date,
        "Data de Validade do BI": employee_id_expiry,
        "Morada do Trabalhador": employee_address,
        "Cargo": job_title,
        "Data de Início": start_date,
        "Salário": salary,
        "Salário por extenso": salary_number,
        "IBAN": iban,
        "Local e Data do Contrato": contract_date_local
    }
    
    missing_fields = [name for name, value in required_fields.items() if not value.strip()]
    
    if missing_fields:
        st.error(f"⚠️ **Campos obrigatórios em falta:** {', '.join(missing_fields)}")
    else:
        # Prepare context for template
        context = {
            "employer_name": employer_name.strip(),
            "employer_nif": employer_nif.strip(),
            "employer_address": employer_address.strip(),
            "representative_name": representative_name.strip(),
            "employee_name": employee_name.strip(),
            "employee_id": employee_id.strip(),
            "employee_id_issue_date": employee_id_issue_date.strip(),
            "employee_id_expiry": employee_id_expiry.strip(),
            "employee_address": employee_address.strip(),
            "job_title": job_title.strip(),
            "start_date": start_date.strip(),
            "salary": salary.strip(),
            "salary_number": salary_number.strip(),
            "bank_name": bank_name.strip(),
            "iban": iban.strip(),
            "work_hours": work_hours.strip(),
            "annual_vacation_days": annual_vacation_days.strip(),
            "trial_period_days": trial_period_days.strip(),
            "contract_date_local": contract_date_local.strip(),
            "governing_law": "Lei Geral do Trabalho, Lei n.º 12/23",
            "signature_employer": "___________________",
            "signature_employee": "___________________"
        }
        
        try:
            # Generate contract
            with tempfile.TemporaryDirectory() as tmpdir:
                # Load and render template
                tpl = DocxTemplate(TEMPLATE)
                tpl.render(context)
                
                # Save DOCX
                docx_filename = f"CONTRATO_{employee_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.docx"
                docx_path = os.path.join(tmpdir, docx_filename)
                tpl.save(docx_path)
                
                st.success("✅ **Contrato gerado com sucesso!**")
                
                # DOCX download
                with open(docx_path, "rb") as f:
                    st.download_button(
                        label="📥 Descarregar DOCX",
                        data=f,
                        file_name=docx_filename,
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        use_container_width=True
                    )
                
                # PDF conversion (optional)
                if ENABLE_PDF_CONVERSION:
                    try:
                        subprocess.run([
                            "libreoffice", "--headless", "--convert-to", "pdf",
                            "--outdir", tmpdir, docx_path
                        ], check=True, timeout=30)
                        
                        pdf_filename = docx_filename.replace(".docx", ".pdf")
                        pdf_path = os.path.join(tmpdir, pdf_filename)
                        
                        if os.path.exists(pdf_path):
                            with open(pdf_path, "rb") as f:
                                st.download_button(
                                    label="📥 Descarregar PDF",
                                    data=f,
                                    file_name=pdf_filename,
                                    mime="application/pdf",
                                    use_container_width=True
                                )
                    except subprocess.TimeoutExpired:
                        st.warning("⏱️ A conversão para PDF demorou demasiado tempo.")
                    except Exception as e:
                        st.warning(f"⚠️ Não foi possível gerar PDF: {str(e)}")
                
                # Display summary
                with st.expander("📊 Resumo do Contrato"):
                    st.markdown(f"""
                    - **Trabalhador:** {employee_name}
                    - **Cargo:** {job_title}
                    - **Salário:** {salary} ({salary_number})
                    - **Data de Início:** {start_date}
                    - **Gerado em:** {datetime.now().strftime('%d/%m/%Y às %H:%M')}
                    """)
        
        except Exception as e:
            st.error(f"❌ **Erro ao processar contrato:** {str(e)}")
            st.info("💡 Verifique se o ficheiro de modelo está correto e tente novamente.")

# Footer
st.divider()
st.caption("🔒 Todos os dados são processados localmente e não são armazenados.")
st.caption("⚠️ Campos marcados com * são obrigatórios.")




