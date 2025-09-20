# Nome do arquivo: app.py

import streamlit as st
import pandas as pd
import numpy as np
import openai # Importa a biblioteca da OpenAI
import os # Para acessar variáveis de ambiente
from dotenv import load_dotenv # Para carregar o arquivo .env

# Carrega as variáveis do arquivo .env (sua chave de API)
load_dotenv()

# --- CONFIGURAÇÃO DA CHAVE DE API ---
# Pega a chave de API do ambiente. O Streamlit Cloud usará os "Secrets".
openai.api_key = os.getenv("OPENAI_API_KEY")

# --- FUNÇÃO PARA CHAMAR A IA ---
# Esta função encapsula a chamada para a OpenAI, tornando o código mais limpo.
def gerar_atividade_ia(aluno, habilidade, pontos_fortes):
    """
    Usa a API da OpenAI para gerar uma atividade pedagógica personalizada.
    """
    # Este é o "prompt", a instrução que damos para a IA.
    # Quanto mais detalhado, melhor a resposta.
    prompt_detalhado = f"""
    Aja como um especialista em psicopedagogia e educação inclusiva.

    Sua tarefa é criar uma atividade pedagógica detalhada, criativa e eficaz para o seguinte perfil de aluno:
    - **Aluno:** {aluno}
    - **Habilidade da BNCC a ser trabalhada:** {habilidade}
    - **Pontos Fortes e Interesses do Aluno:** {pontos_fortes}

    A atividade deve ser:
    1.  **Lúdica e Engajadora:** Use os interesses do aluno como tema central.
    2.  **Adaptada:** Inclua sugestões claras de adaptação para as necessidades específicas do aluno (mencionadas no perfil).
    3.  **Estruturada:** Apresente a atividade com "Objetivo", "Materiais Necessários" e "Passo a Passo".
    4.  **Inclusiva:** Foco no reforço positivo e na celebração do progresso.

    Retorne a resposta formatada em Markdown, pronta para ser exibida.
    """

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",  # Modelo de IA que vamos usar
            messages=[
                {"role": "system", "content": "Você é um assistente especialista em educação inclusiva."},
                {"role": "user", "content": prompt_detalhado}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Ocorreu um erro ao conectar com a API da OpenAI: {e}"


# --- O restante do código da interface (Sidebar, Dashboard) permanece o mesmo ---

# --- BARRA LATERAL (SIDEBAR) ---
with st.sidebar:
    st.title("🎓 EduInclusiva")
    
    pagina_selecionada = st.radio(
        "Navegue pela Plataforma",
        ["Dashboard", "Pedagógico IA", "Colaboração Multidisciplinar"],
        captions=["Visão Geral do Progresso", "Geração de Atividades com IA", "Comunicação da Equipe"]
    )
    
    st.success("Aplicação criada com Streamlit e hospedada na Streamlit Community Cloud.")
    st.info("Navegue pelas páginas para ver as funcionalidades.")

# --- PÁGINA: DASHBOARD ---
if pagina_selecionada == "Dashboard":
    st.header("Dashboard de Gestão", divider='rainbow')

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="Total de Alunos", value="1,247", delta="+12%")
    with col2:
        st.metric(label="PEIs Ativos", value="342", delta="+8%")
    with col3:
        st.metric(label="Atividades Realizadas", value="2,156", delta="+23%")
    with col4:
        st.metric(label="Taxa de Evolução Média", value="87%", delta="+5%")

    st.subheader("Evolução Geral dos Alunos")
    
    chart_data = pd.DataFrame(
        {
            "Progresso (%)": [65, 70, 75, 78, 82, 87],
        },
        index=['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho']
    )
    st.line_chart(chart_data)

# --- PÁGINA: PEDAGÓGICO IA ---
elif pagina_selecionada == "Pedagógico IA":
    st.header("🧠 Pedagógico Inteligente", divider='rainbow')
    st.write("Gere atividades personalizadas com IA, alinhadas à BNCC e às necessidades de cada aluno.")

    with st.form("pedagogico_form"):
        st.subheader("Configuração da Atividade")
        
        aluno_selecionado = st.selectbox(
            "Selecione o Aluno",
            ["João Silva Santos - TEA Nível 1 (3º Ano)", "Maria Santos - TDAH (4º Ano)", "Pedro Costa - Dislexia (2º Ano)"]
        )
        
        habilidade_bncc = st.text_input("Habilidade da BNCC", "EF03MA01: Ler, escrever e comparar números naturais...")

        pontos_fortes = st.text_area("Pontos Fortes do Aluno (interesses, habilidades, etc.)", "Excelente memória visual, grande interesse por dinossauros, bom em atividades de montar.")
        
        submitted = st.form_submit_button("🤖 Gerar Atividade com IA")
        if submitted:
            if not openai.api_key:
                st.error("Chave de API da OpenAI não configurada. Por favor, adicione-a nos segredos da aplicação.")
            else:
                with st.spinner('Aguarde... Nossa IA está elaborando a melhor atividade para o perfil selecionado...'):
                    # Chamada real para a função da IA
                    resposta_ia = gerar_atividade_ia(aluno_selecionado, habilidade_bncc, pontos_fortes)
                    st.success("Atividade gerada com sucesso!")
                    st.balloons()
                    # Exibe a resposta formatada da IA
                    st.markdown(resposta_ia)

# --- PÁGINA: COLABORAÇÃO ---
elif pagina_selecionada == "Colaboração Multidisciplinar":
    st.header("👥 Colaboração Multidisciplinar", divider='rainbow')
    st.write("Um espaço para a equipe trocar informações e registrar o progresso de forma unificada.")

    st.text_input("Digite sua mensagem para a equipe...", key="chat_input", placeholder="Use @ para mencionar um colega...")
    st.button("Enviar Mensagem")

    st.subheader("Últimas Atualizações")
    st.info("Dra. Paula (Psicóloga): João demonstrou ótima interação na sessão de hoje. Recomendo atividade em grupo.", icon="👩‍⚕️")
    st.warning("Carlos (Fonoaudiólogo): Notei uma pequena dificuldade com dígrafos. Vamos focar nisso na próxima semana.", icon="🗣️")
