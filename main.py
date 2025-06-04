import streamlit as st  # Biblioteca para criar interfaces web simples em Python
import os  # Biblioteca para interagir com o sistema operacional
from dotenv import load_dotenv  # Carrega variáveis de ambiente do arquivo .env
import zipfile  # Para manipular arquivos ZIP
import tempfile  # Para criar diretórios temporários
from langchain_google_genai import ChatGoogleGenerativeAI  # Integração com o modelo Gemini do Google
from langchain_experimental.agents.agent_toolkits import create_csv_agent  # Cria agentes para CSVs
from langchain.agents.agent_types import AgentType  # Tipos de agentes disponíveis

# Função para limpar o diretório temporário criado durante o uso do app
def cleanup_temp_dir(temp_dir_obj):
    if temp_dir_obj:
        try:
            temp_dir_obj.cleanup()
        except Exception as e:
            st.warning(f"Não foi possível limpar o diretório temporário: {e}")

def main():
    load_dotenv()  # Carrega as variáveis do arquivo .env

    # Verifica se a chave da API do Google está definida
    if os.getenv("GOOGLE_API_KEY") is None or os.getenv("GOOGLE_API_KEY") == "":
        st.error("GOOGLE_API_KEY não está definida. Por favor, adicione-a ao seu arquivo .env.")
        st.stop()

    st.set_page_config(page_title="Pergunte aos seus CSVs (ZIP)")
    st.header("Pergunte aos seus CSVs 📈 (a partir de um arquivo ZIP)")

    # Inicializa variáveis de estado da sessão do Streamlit
    if "csv_file_paths" not in st.session_state:
        st.session_state.csv_file_paths = []
    if "temp_dir_obj" not in st.session_state:
        st.session_state.temp_dir_obj = None
    if "processed_zip_name" not in st.session_state:
        st.session_state.processed_zip_name = None
    if "agent" not in st.session_state:
        st.session_state.agent = None

    # Componente para upload do arquivo ZIP
    uploaded_file = st.file_uploader("Envie um arquivo ZIP contendo arquivos CSV", type="zip")

    if uploaded_file is not None:
        # Se um novo ZIP for enviado ou nenhum arquivo foi processado ainda
        if st.session_state.processed_zip_name != uploaded_file.name:
            st.info(f"Processando {uploaded_file.name}...")

            # Limpa o diretório temporário antigo, se existir
            if st.session_state.temp_dir_obj:
                cleanup_temp_dir(st.session_state.temp_dir_obj)
                st.session_state.temp_dir_obj = None

            try:
                # Cria um novo diretório temporário
                st.session_state.temp_dir_obj = tempfile.TemporaryDirectory()
                temp_dir_path = st.session_state.temp_dir_obj.name

                extracted_csv_paths = []
                with zipfile.ZipFile(uploaded_file, 'r') as zip_ref:
                    for member in zip_ref.namelist():
                        if member.endswith('.csv') and not member.startswith('__MACOSX'):
                            target_path = os.path.join(temp_dir_path, member)
                            os.makedirs(os.path.dirname(target_path), exist_ok=True)
                            zip_ref.extract(member, temp_dir_path)
                            extracted_csv_paths.append(target_path)

                st.session_state.csv_file_paths = extracted_csv_paths
                st.session_state.processed_zip_name = uploaded_file.name
                st.session_state.agent = None  # Reseta o agente ao carregar novos CSVs

                if not st.session_state.csv_file_paths:
                    st.warning("Nenhum arquivo CSV encontrado no ZIP enviado.")
                else:
                    st.success(f"{len(st.session_state.csv_file_paths)} arquivo(s) CSV extraído(s) com sucesso.")

            except zipfile.BadZipFile:
                st.error("Arquivo ZIP inválido. Por favor, envie um arquivo ZIP válido.")
                st.session_state.csv_file_paths = []
                st.session_state.processed_zip_name = None
            except Exception as e:
                st.error(f"Ocorreu um erro: {e}")
                st.session_state.csv_file_paths = []
                st.session_state.processed_zip_name = None
            st.rerun()  # Atualiza a interface

    if st.session_state.csv_file_paths:
        csv_file_options = {os.path.basename(path): path for path in st.session_state.csv_file_paths}

        if not csv_file_options:
            st.warning("Nenhum arquivo CSV disponível para seleção.")
            return

        selected_csv_name = st.selectbox(
            "Selecione um arquivo CSV para fazer perguntas:",
            options=list(csv_file_options.keys())
        )

        if selected_csv_name:
            selected_csv_path = csv_file_options[selected_csv_name]

            # Inicializa o modelo de linguagem (Gemini)
            try:
                llm = ChatGoogleGenerativeAI(
                    model="gemini-2.5-flash-preview-05-20",
                    temperature=0.1,
                    convert_system_message_to_human=True
                )
            except Exception as e:
                st.error(f"Falha ao inicializar o Gemini LLM: {e}. Verifique sua chave de API e conexão.")
                return

            # Cria ou recupera o agente para o CSV selecionado
            if st.session_state.agent is None or st.session_state.get("current_agent_csv") != selected_csv_path:
                with st.spinner(f"Preparando agente para {selected_csv_name}..."):
                    try:
                        st.session_state.agent = create_csv_agent(
                            llm,
                            selected_csv_path,
                            verbose=True,
                            agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
                            handle_parsing_errors=True,
                            allow_dangerous_code=True
                        )
                        st.session_state.current_agent_csv = selected_csv_path
                        st.success(f"Agente pronto para {selected_csv_name}!")
                    except Exception as e:
                        st.error(f"Erro ao criar agente para {selected_csv_name}: {e}")
                        st.session_state.agent = None
                        return

            if st.session_state.agent:
                user_question = st.text_input(f"Faça uma pergunta sobre '{selected_csv_name}':")

                if user_question:
                    with st.spinner("Pensando..."):
                        try:
                            response = st.session_state.agent.run(user_question)
                            st.write(response)
                        except Exception as e:
                            st.error(f"Erro durante a consulta: {e}")
                            st.info("O agente pode ter encontrado um problema. Tente reformular sua pergunta ou selecione outro CSV.")
    else:
        st.info("Por favor, envie um arquivo ZIP contendo arquivos CSV para começar.")

if __name__ == "__main__":
    main()