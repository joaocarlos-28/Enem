import streamlit as st
import anthropic
import re

# ── Configuração da página ──────────────────────────────────────────────────
st.set_page_config(
    page_title="CorrigeAí – Redação ENEM",
    page_icon="📝",
    layout="centered",
)

# ── CSS personalizado ───────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Merriweather:wght@400;700&family=Inter:wght@400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

h1, h2, h3 {
    font-family: 'Merriweather', serif;
}

.main-title {
    text-align: center;
    font-size: 2.6rem;
    font-weight: 700;
    color: #1a1a2e;
    margin-bottom: 0.2rem;
}

.subtitle {
    text-align: center;
    color: #555;
    font-size: 1rem;
    margin-bottom: 2rem;
}

.score-card {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    border-radius: 16px;
    padding: 2rem;
    text-align: center;
    color: white;
    margin: 1.5rem 0;
    box-shadow: 0 8px 32px rgba(26,26,46,0.18);
}

.score-number {
    font-size: 5rem;
    font-weight: 800;
    font-family: 'Merriweather', serif;
    line-height: 1;
    color: #f0c040;
}

.score-label {
    font-size: 1rem;
    opacity: 0.8;
    margin-top: 0.4rem;
}

.competencia-card {
    background: #f8f9fc;
    border-left: 4px solid #1a1a2e;
    border-radius: 8px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.8rem;
}

.competencia-title {
    font-weight: 600;
    color: #1a1a2e;
    font-size: 0.95rem;
}

.competencia-score {
    font-size: 1.4rem;
    font-weight: 700;
    color: #f0c040;
}

.stTextArea textarea {
    font-family: 'Georgia', serif;
    font-size: 1rem;
    line-height: 1.7;
    border-radius: 10px !important;
    border: 1.5px solid #dde !important;
}

.stButton > button {
    background: linear-gradient(135deg, #1a1a2e, #16213e);
    color: white;
    font-weight: 600;
    font-size: 1.05rem;
    border-radius: 10px;
    padding: 0.65rem 2rem;
    border: none;
    width: 100%;
    transition: all 0.2s;
}

.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 6px 20px rgba(26,26,46,0.25);
}

hr {
    border: none;
    border-top: 1.5px solid #eee;
    margin: 1.5rem 0;
}
</style>
""", unsafe_allow_html=True)

# ── Título ──────────────────────────────────────────────────────────────────
st.markdown('<div class="main-title">📝 CorrigeAí</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Correção de Redação no estilo ENEM com Inteligência Artificial</div>', unsafe_allow_html=True)
st.markdown("---")

# ── Formulário ──────────────────────────────────────────────────────────────
col1, col2 = st.columns([1, 2])
with col1:
    nome = st.text_input("👤 Seu nome", placeholder="Ex: Maria Silva")
with col2:
    tema = st.text_input("📌 Tema da redação (opcional)", placeholder="Ex: Desafios da educação no Brasil")

redacao = st.text_area(
    "✍️ Cole ou escreva sua redação aqui",
    height=320,
    placeholder="Escreva sua redação dissertativo-argumentativa aqui. Lembre-se: introdução, desenvolvimento (2 parágrafos) e conclusão com proposta de intervenção...",
)

# ── Botão e processamento ───────────────────────────────────────────────────
if st.button("🔍 Corrigir minha redação"):
    if not nome.strip():
        st.warning("Por favor, informe seu nome antes de continuar.")
    elif len(redacao.strip()) < 100:
        st.warning("Sua redação parece muito curta. Por favor, escreva um texto mais completo.")
    else:
        with st.spinner(f"Analisando sua redação, {nome.split()[0]}... ✨"):

            prompt = f"""Você é um corretor especialista em redações do ENEM, com profundo conhecimento das 5 competências avaliadas. 
Corrija a redação abaixo com rigor e didática, exatamente como faria um corretor oficial do ENEM.

Nome do aluno: {nome}
Tema: {tema if tema else "Não informado"}

--- REDAÇÃO ---
{redacao}
--- FIM ---

Responda OBRIGATORIAMENTE neste formato JSON (sem markdown, sem explicações fora do JSON):

{{
  "nota_final": <número de 0 a 1000, múltiplo de 40>,
  "competencias": [
    {{"numero": 1, "nome": "Domínio da norma culta", "nota": <0-200>, "comentario": "<análise detalhada>"}},
    {{"numero": 2, "nome": "Compreensão da proposta e aplicação de conceitos", "nota": <0-200>, "comentario": "<análise detalhada>"}},
    {{"numero": 3, "nome": "Seleção e organização das informações", "nota": <0-200>, "comentario": "<análise detalhada>"}},
    {{"numero": 4, "nome": "Construção da argumentação", "nota": <0-200>, "comentario": "<análise detalhada>"}},
    {{"numero": 5, "nome": "Proposta de intervenção", "nota": <0-200>, "comentario": "<análise detalhada>"}}
  ],
  "erros_ortografia": ["<erro1>", "<erro2>"],
  "erros_pontuacao": ["<erro1>", "<erro2>"],
  "pontos_positivos": ["<ponto1>", "<ponto2>", "<ponto3>"],
  "sugestoes_melhoria": ["<sugestão1>", "<sugestão2>", "<sugestão3>"],
  "parecer_geral": "<parecer completo e encorajador de 3-4 frases>"
}}"""

            try:
                client = anthropic.Anthropic()
                message = client.messages.create(
                    model="claude-sonnet-4-20250514",
                    max_tokens=2000,
                    messages=[{"role": "user", "content": prompt}],
                )

                raw = message.content[0].text.strip()
                # Remove possíveis marcadores de código
                raw = re.sub(r"^```json\s*", "", raw)
                raw = re.sub(r"```$", "", raw).strip()

                import json
                resultado = json.loads(raw)

                # ── Nota Final ──────────────────────────────────────────────
                nota = resultado.get("nota_final", 0)
                if nota >= 800:
                    emoji_nivel = "🏆"
                    nivel = "Excelente"
                elif nota >= 600:
                    emoji_nivel = "⭐"
                    nivel = "Bom"
                elif nota >= 400:
                    emoji_nivel = "📈"
                    nivel = "Regular"
                else:
                    emoji_nivel = "💪"
                    nivel = "Precisa melhorar"

                st.markdown(f"""
                <div class="score-card">
                    <div style="font-size:1rem; opacity:0.75; margin-bottom:0.5rem">Olá, {nome.split()[0]}! Sua nota foi:</div>
                    <div class="score-number">{nota}</div>
                    <div class="score-label">de 1000 pontos &nbsp;·&nbsp; {emoji_nivel} {nivel}</div>
                </div>
                """, unsafe_allow_html=True)

                # ── Competências ────────────────────────────────────────────
                st.markdown("### 📊 Desempenho por Competência")
                for comp in resultado.get("competencias", []):
                    n = comp.get("nota", 0)
                    cor = "#27ae60" if n >= 160 else "#f39c12" if n >= 100 else "#e74c3c"
                    st.markdown(f"""
                    <div class="competencia-card">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <div class="competencia-title">C{comp['numero']} – {comp['nome']}</div>
                            <div class="competencia-score" style="color:{cor}">{n}/200</div>
                        </div>
                        <div style="font-size:0.88rem; color:#555; margin-top:0.4rem">{comp['comentario']}</div>
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown("---")

                # ── Erros ───────────────────────────────────────────────────
                col_a, col_b = st.columns(2)
                with col_a:
                    st.markdown("### 🔴 Erros de Ortografia")
                    erros_ort = resultado.get("erros_ortografia", [])
                    if erros_ort:
                        for e in erros_ort:
                            st.markdown(f"- {e}")
                    else:
                        st.success("Nenhum erro de ortografia encontrado! ✅")

                with col_b:
                    st.markdown("### 🟠 Erros de Pontuação")
                    erros_pont = resultado.get("erros_pontuacao", [])
                    if erros_pont:
                        for e in erros_pont:
                            st.markdown(f"- {e}")
                    else:
                        st.success("Nenhum erro de pontuação encontrado! ✅")

                st.markdown("---")

                # ── Positivos e Sugestões ───────────────────────────────────
                col_c, col_d = st.columns(2)
                with col_c:
                    st.markdown("### ✅ Pontos Positivos")
                    for p in resultado.get("pontos_positivos", []):
                        st.markdown(f"- {p}")

                with col_d:
                    st.markdown("### 💡 Sugestões de Melhoria")
                    for s in resultado.get("sugestoes_melhoria", []):
                        st.markdown(f"- {s}")

                st.markdown("---")

                # ── Parecer Geral ───────────────────────────────────────────
                st.markdown("### 📋 Parecer Geral do Corretor")
                st.info(resultado.get("parecer_geral", ""))

            except json.JSONDecodeError:
                st.error("Erro ao processar a resposta da IA. Tente novamente.")
            except Exception as e:
                st.error(f"Ocorreu um erro: {e}")

# ── Rodapé ──────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<div style='text-align:center; color:#aaa; font-size:0.82rem'>CorrigeAí · Powered by Claude AI · Apenas para fins educacionais</div>",
    unsafe_allow_html=True,
)
