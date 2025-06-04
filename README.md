# Agente de Perguntas para CSVs (com Gemini)

Este projeto permite que você envie um arquivo ZIP contendo um ou mais arquivos CSV e faça perguntas em linguagem natural sobre os dados, utilizando inteligência artificial (Gemini, do Google).

## Funcionalidades

- Upload de arquivos ZIP contendo múltiplos CSVs.
- Seleção de qual CSV deseja consultar.
- Perguntas em português sobre os dados do CSV.
- Respostas geradas por IA (modelo Gemini).
- Interface web simples via Streamlit.

## Pré-requisitos

- Python 3.8 ou superior
- Conta Google Cloud com acesso à API Gemini (Google Generative AI)
- Chave de API válida (GOOGLE_API_KEY)

## Instalação

1. **Clone o repositório:**

   ```sh
   git clone <URL_DO_REPOSITORIO>
   cd agent
   ```

2. **Crie um ambiente virtual (opcional, mas recomendado):**

   ```sh
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

3. **Instale as dependências:**

   ```sh
   pip install -r requirements.txt
   ```

4. **Configure sua chave de API:**

   - Crie um arquivo `.env` na raiz do projeto (caso não exista).
   - Adicione sua chave da API Gemini:
     ```
     GOOGLE_API_KEY="SUA_CHAVE_AQUI"
     ```

## Como usar

1. **Execute o aplicativo:**

   ```sh
   streamlit run main.py
   ```

2. **No navegador:**
   - Acesse o endereço exibido no terminal (geralmente http://localhost:8501).
   - Envie um arquivo ZIP contendo um ou mais arquivos CSV.
   - Selecione o CSV desejado.
   - Faça perguntas em português sobre os dados do arquivo.

## Observações

- O arquivo ZIP deve conter apenas arquivos CSV (outros arquivos serão ignorados).
- O processamento e análise dos dados é feito localmente, mas as perguntas são respondidas via IA na nuvem (Google Gemini).
- O projeto foi desenvolvido para ser simples e acessível, mesmo para quem não tem experiência em programação.

## Exemplo de uso

1. Prepare um arquivo ZIP com seus CSVs.
2. Faça upload na interface.
3. Pergunte, por exemplo:
   - "Qual a média da coluna idade?"
   - "Quantos registros existem para o estado de São Paulo?"

## Suporte

Em caso de dúvidas ou problemas, abra uma issue no repositório ou entre em contato com o responsável pelo projeto.

---

**Divirta-se explorando seus dados com IA!**