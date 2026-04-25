import streamlit as st
from groq import Groq
import json
import re

# ── Configuração da página ──────────────────────────────────────────────────
st.set_page_config(
    page_title="CorrigeAí – Redação ENEM",
    page_icon="📝",
    layout="wide",
)

# ── CSS personalizado ───────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&family=Playfair+Display:wght@700;900&display=swap');

/* Reset e base */
html, body, [class*="css"] {
    font-family: 'Nunito', sans-serif;
    background-color: #f0f4ff;
}

/* Esconde elementos padrão do Streamlit */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 3rem 3rem 3rem !important; max-width: 1100px; }

/* ── HERO HEADER ── */
.hero {
    background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 50%, #a855f7 100%);
    border-radius: 24px;
    padding: 2.5rem 3rem;
    margin-bottom: 2rem;
    color: white;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 220px; height: 220px;
    background: rgba(255,255,255,0.07);
    border-radius: 50%;
}
.hero::after {
    content: '';
    position: absolute;
    bottom: -40px; left: 40px;
    width: 150px; height: 150px;
    background: rgba(255,255,255,0.05);
    border-radius: 50%;
}
.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: 3rem;
    font-weight: 900;
    margin: 0 0 0.3rem 0;
    letter-spacing: -1px;
}
.hero-sub {
    font-size: 1.1rem;
    opacity: 0.85;
    font-weight: 600;
    margin: 0;
}
.hero-badges {
    display: flex;
    gap: 0.6rem;
    margin-top: 1.2rem;
    flex-wrap: wrap;
}
.badge {
    background: rgba(255,255,255,0.18);
    border: 1px solid rgba(255,255,255,0.3);
    border-radius: 20px;
    padding: 0.3rem 0.9rem;
    font-size: 0.82rem;
    font-weight: 700;
    backdrop-filter: blur(4px);
}

/* ── STEPS ── */
.steps-row {
    display: flex;
    gap: 1rem;
    margin-bottom: 2rem;
}
.step-card {
    flex: 1;
    background: white;
    border-radius: 16px;
    padding: 1.2rem;
    text-align: center;
    box-shadow: 0 2px 12px rgba(79,70,229,0.08);
    border: 2px solid transparent;
    transition: all 0.2s;
}
.step-card:hover {
    border-color: #4f46e5;
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(79,70,229,0.15);
}
.step-num {
    width: 36px; height: 36px;
    background: linear-gradient(135deg, #4f46e5, #7c3aed);
    color: white;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-weight: 900; font-size: 1rem;
    margin: 0 auto 0.6rem auto;
}
.step-title { font-weight: 800; color: #1e1b4b; font-size: 0.9rem; }
.step-desc { font-size: 0.78rem; color: #6b7280; margin-top: 0.2rem; }

/* ── FORM CARD ── */
.form-card {
    background: white;
    border-radius: 20px;
    padding: 2rem;
    box-shadow: 0 4px 24px rgba(79,70,229,0.08);
    margin-bottom: 1.5rem;
}
.form-section-title {
    font-weight: 800;
    color: #1e1b4b;
    font-size: 1.1rem;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

/* ── INPUTS ── */
.stTextInput input {
    border-radius: 12px !important;
    border: 2px solid #e5e7eb !important;
    font-family: 'Nunito', sans-serif !important;
    font-size: 0.95rem !important;
    padding: 0.6rem 1rem !important;
    transition: border-color 0.2s !important;
}
.stTextInput input:focus {
    border-color: #4f46e5 !important;
    box-shadow: 0 0 0 3px rgba(79,70,229,0.1) !important;
}
.stTextArea textarea {
    border-radius: 12px !important;
    border: 2px solid #e5e7eb !important;
    font-family: 'Georgia', serif !important;
    font-size: 1rem !important;
    line-height: 1.8 !important;
    transition: border-color 0.2s !important;
}
.stTextArea textarea:focus {
    border-color: #4f46e5 !important;
    box-shadow: 0 0 0 3px rgba(79,70,229,0.1) !important;
}

/* ── BOTÃO ── */
.stButton > button {
    background: linear-gradient(135deg, #4f46e5, #7c3aed) !important;
    color: white !important;
    font-family: 'Nunito', sans-serif !important;
    font-weight: 800 !important;
    font-size: 1.1rem !important;
    border-radius: 14px !important;
    padding: 0.75rem 2.5rem !important;
    border: none !important;
    width: 100% !important;
    transition: all 0.2s !important;
    letter-spacing: 0.3px !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 28px rgba(79,70,229,0.4) !important;
}

/* ── SCORE CARD ── */
.score-hero {
    background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 60%, #a855f7 100%);
    border-radius: 24px;
    padding: 2.5rem;
    text-align: center;
    color: white;
    margin: 1.5rem 0;
    position: relative;
    overflow: hidden;
}
.score-hero::before {
    content: '';
    position: absolute;
    top: -50px; right: -50px;
    width: 180px; height: 180px;
    background: rgba(255,255,255,0.06);
    border-radius: 50%;
}
.score-greeting {
    font-size: 1rem;
    opacity: 0.8;
    font-weight: 600;
    margin-bottom: 0.5rem;
}
.score-number {
    font-family: 'Playfair Display', serif;
    font-size: 6rem;
    font-weight: 900;
    line-height: 1;
    color: #fde68a;
    text-shadow: 0 4px 20px rgba(0,0,0,0.2);
}
.score-max { font-size: 1.4rem; opacity: 0.7; font-weight: 600; }
.score-nivel {
    display: inline-block;
    background: rgba(255,255,255,0.2);
    border: 1px solid rgba(255,255,255,0.35);
    border-radius: 20px;
    padding: 0.4rem 1.2rem;
    margin-top: 0.8rem;
    font-weight: 800;
    font-size: 1rem;
}

/* ── BARRA DE PROGRESSO CUSTOMIZADA ── */
.progress-wrap {
    background: white;
    border-radius: 20px;
    padding: 1.8rem 2rem;
    box-shadow: 0 4px 20px rgba(79,70,229,0.08);
    margin-bottom: 1rem;
}
.prog-title {
    font-weight: 900;
    color: #1e1b4b;
    font-size: 1.1rem;
    margin-bottom: 1.4rem;
}
.comp-row {
    margin-bottom: 1.2rem;
}
.comp-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.4rem;
}
.comp-name {
    font-weight: 700;
    color: #374151;
    font-size: 0.88rem;
}
.comp-score-badge {
    font-weight: 800;
    font-size: 0.9rem;
    padding: 0.15rem 0.7rem;
    border-radius: 10px;
}
.comp-bar-bg {
    background: #f3f4f6;
    border-radius: 10px;
    height: 10px;
    overflow: hidden;
}
.comp-bar-fill {
    height: 10px;
    border-radius: 10px;
    transition: width 0.8s ease;
}
.comp-comment {
    font-size: 0.8rem;
    color: #6b7280;
    margin-top: 0.4rem;
    line-height: 1.5;
}

/* ── CARDS DE ANÁLISE ── */
.analysis-card {
    background: white;
    border-radius: 18px;
    padding: 1.5rem;
    box-shadow: 0 4px 20px rgba(0,0,0,0.06);
    height: 100%;
}
.analysis-card-title {
    font-weight: 900;
    font-size: 1rem;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.item-pill {
    display: flex;
    align-items: flex-start;
    gap: 0.6rem;
    padding: 0.6rem 0.8rem;
    border-radius: 10px;
    margin-bottom: 0.5rem;
    font-size: 0.87rem;
    line-height: 1.5;
    font-weight: 600;
}
.pill-erro-ort  { background: #fef2f2; color: #991b1b; border-left: 3px solid #ef4444; }
.pill-erro-pont { background: #fff7ed; color: #9a3412; border-left: 3px solid #f97316; }
.pill-positivo  { background: #f0fdf4; color: #166534; border-left: 3px solid #22c55e; }
.pill-sugestao  { background: #eff6ff; color: #1e40af; border-left: 3px solid #3b82f6; }

/* ── PARECER GERAL ── */
.parecer-card {
    background: linear-gradient(135deg, #f0f9ff, #e0f2fe);
    border-radius: 18px;
    padding: 1.8rem 2rem;
    border-left: 5px solid #0ea5e9;
    margin-top: 1rem;
}
.parecer-title {
    font-weight: 900;
    color: #0c4a6e;
    font-size: 1.05rem;
    margin-bottom: 0.8rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.parecer-text {
    color: #0369a1;
    font-size: 0.97rem;
    line-height: 1.8;
    font-weight: 600;
}

/* ── DICAS ── */
.dica-box {
    background: linear-gradient(135deg, #faf5ff, #f3e8ff);
    border-radius: 16px;
    padding: 1.2rem 1.5rem;
    border-left: 4px solid #a855f7;
    margin-top: 1.5rem;
    font-size: 0.88rem;
    color: #6b21a8;
    font-weight: 600;
}

/* ── EMPTY STATE ── */
.empty-state {
    text-align: center;
    padding: 1.5rem;
    color: #9ca3af;
    font-size: 0.88rem;
    font-weight: 600;
}

/* ── RODAPÉ ── */
.footer {
    text-align: center;
    color: #9ca3af;
    font-size: 0.82rem;
    margin-top: 2.5rem;
    padding-top: 1.5rem;
    border-top: 1px solid #e5e7eb;
    font-weight: 600;
}

/* Labels do Streamlit */
.stTextInput label, .stTextArea label {
    font-family: 'Nunito', sans-serif !important;
    font-weight: 700 !important;
    color: #374151 !important;
    font-size: 0.9rem !important;
}
</style>
""", unsafe_allow_html=True)

# ── HERO HEADER ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-title">📝 CorrigeAí</div>
    <p class="hero-sub">Corrija sua redação do ENEM com Inteligência Artificial — gratuito e instantâneo</p>
    <div class="hero-badges">
        <span class="badge">✦ 5 Competências ENEM</span>
        <span class="badge">✦ Nota de 0 a 1000</span>
        <span class="badge">✦ Erros de ortografia e pontuação</span>
        <span class="badge">✦ Sugestões personalizadas</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ── STEPS ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="steps-row">
    <div class="step-card">
        <div class="step-num">1</div>
        <div class="step-title">Identifique-se</div>
        <div class="step-desc">Informe seu nome e o tema da redação</div>
    </div>
    <div class="step-card">
        <div class="step-num">2</div>
        <div class="step-title">Cole sua redação</div>
        <div class="step-desc">Insira seu texto dissertativo-argumentativo</div>
    </div>
    <div class="step-card">
        <div class="step-num">3</div>
        <div class="step-title">Clique em corrigir</div>
        <div class="step-desc">A IA analisa segundo os critérios do ENEM</div>
    </div>
    <div class="step-card">
        <div class="step-num">4</div>
        <div class="step-title">Veja o resultado</div>
        <div class="step-desc">Nota, erros, pontos fortes e sugestões</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── FORMULÁRIO ───────────────────────────────────────────────────────────────
st.markdown('<div class="form-card">', unsafe_allow_html=True)
st.markdown('<div class="form-section-title">👤 Suas informações</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    nome = st.text_input("Nome completo", placeholder="Ex: Maria Silva")
with col2:
    tema = st.text_input("Tema da redação (opcional)", placeholder="Ex: Desafios da educação no Brasil")

st.markdown('<div class="form-section-title" style="margin-top:1.2rem">✍️ Sua redação</div>', unsafe_allow_html=True)

redacao = st.text_area(
    "Texto dissertativo-argumentativo",
    height=300,
    placeholder="Escreva ou cole sua redação aqui...\n\nLembre-se da estrutura:\n→ Introdução: apresente o tema e sua tese\n→ Desenvolvimento 1: 1º argumento com repertório\n→ Desenvolvimento 2: 2º argumento aprofundado\n→ Conclusão: proposta de intervenção detalhada",
)

# Contador de palavras
palavras = len(redacao.strip().split()) if redacao.strip() else 0
chars = len(redacao.strip())
col_w1, col_w2, col_w3 = st.columns([1,1,4])
with col_w1:
    st.caption(f"📝 **{palavras}** palavras")
with col_w2:
    st.caption(f"🔤 **{chars}** caracteres")

st.markdown('</div>', unsafe_allow_html=True)

st.markdown("""
<div class="dica-box">
    💡 <strong>Dica ENEM:</strong> Uma boa redação tem entre 25 e 30 linhas (aproximadamente 400 a 500 palavras).
    Certifique-se de incluir uma proposta de intervenção com agente, ação, meio, finalidade e detalhamento.
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── BOTÃO E PROCESSAMENTO ────────────────────────────────────────────────────
if st.button("🔍 Corrigir minha redação agora"):
    if not nome.strip():
        st.warning("⚠️ Por favor, informe seu nome antes de continuar.")
    elif len(redacao.strip()) < 100:
        st.warning("⚠️ Sua redação parece muito curta. Escreva um texto mais completo para uma análise precisa.")
    else:
        with st.spinner(f"🤖 Analisando sua redação, {nome.split()[0]}... Isso pode levar alguns segundos."):

            prompt = f"""Você é um corretor especialista em redações do ENEM, com profundo conhecimento das 5 competências avaliadas.
Corrija a redação abaixo com rigor e didática, exatamente como faria um corretor oficial do ENEM.

Nome do aluno: {nome}
Tema: {tema if tema else "Não informado"}

--- REDAÇÃO ---
{redacao}
--- FIM ---

Responda OBRIGATORIAMENTE apenas com um objeto JSON válido, sem nenhum texto antes ou depois, sem markdown, sem blocos de código:

{{
  "nota_final": <número de 0 a 1000, múltiplo de 40>,
  "competencias": [
    {{"numero": 1, "nome": "Domínio da norma culta", "nota": <0-200>, "comentario": "<análise detalhada>"}},
    {{"numero": 2, "nome": "Compreensão da proposta", "nota": <0-200>, "comentario": "<análise detalhada>"}},
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
                client = Groq(api_key=st.secrets["GROQ_API_KEY"])
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "Você é um corretor especialista em redações do ENEM. Responda sempre e somente com JSON válido, sem texto adicional."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.3,
                    max_tokens=2000,
                )

                raw = response.choices[0].message.content.strip()
                raw = re.sub(r"^```json\s*", "", raw)
                raw = re.sub(r"^```\s*", "", raw)
                raw = re.sub(r"```$", "", raw).strip()
                resultado = json.loads(raw)

                # ── NOTA FINAL ───────────────────────────────────────────────
                nota = resultado.get("nota_final", 0)
                pct = nota / 1000 * 100

                if nota >= 900:
                    nivel = "🏆 Nota Excelente!"
                    cor_nivel = "#fde68a"
                elif nota >= 800:
                    nivel = "⭐ Muito Bom!"
                    cor_nivel = "#fde68a"
                elif nota >= 600:
                    nivel = "👍 Bom desempenho"
                    cor_nivel = "#fde68a"
                elif nota >= 400:
                    nivel = "📈 Desempenho Regular"
                    cor_nivel = "#fde68a"
                else:
                    nivel = "💪 Continue praticando!"
                    cor_nivel = "#fde68a"

                st.markdown(f"""
                <div class="score-hero">
                    <div class="score-greeting">Resultado de {nome.split()[0]} 🎉</div>
                    <div class="score-number">{nota}</div>
                    <div class="score-max">pontos de 1000</div>
                    <div class="score-nivel">{nivel}</div>
                </div>
                """, unsafe_allow_html=True)

                # ── BARRA DE PROGRESSO GERAL ─────────────────────────────────
                st.progress(nota / 1000)

                st.markdown("<br>", unsafe_allow_html=True)

                # ── COMPETÊNCIAS COM BARRAS VISUAIS ──────────────────────────
                competencias = resultado.get("competencias", [])
                st.markdown('<div class="progress-wrap"><div class="prog-title">📊 Desempenho por Competência</div>', unsafe_allow_html=True)

                for comp in competencias:
                    n = comp.get("nota", 0)
                    pct_comp = int((n / 200) * 100)

                    if n >= 160:
                        cor_bar = "#22c55e"
                        cor_badge_bg = "#f0fdf4"
                        cor_badge_txt = "#166534"
                    elif n >= 100:
                        cor_bar = "#f59e0b"
                        cor_badge_bg = "#fffbeb"
                        cor_badge_txt = "#92400e"
                    else:
                        cor_bar = "#ef4444"
                        cor_badge_bg = "#fef2f2"
                        cor_badge_txt = "#991b1b"

                    st.markdown(f"""
                    <div class="comp-row">
                        <div class="comp-header">
                            <span class="comp-name">C{comp['numero']} — {comp['nome']}</span>
                            <span class="comp-score-badge" style="background:{cor_badge_bg}; color:{cor_badge_txt}">
                                {n}/200
                            </span>
                        </div>
                        <div class="comp-bar-bg">
                            <div class="comp-bar-fill" style="width:{pct_comp}%; background:{cor_bar};"></div>
                        </div>
                        <div class="comp-comment">{comp['comentario']}</div>
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown('</div>', unsafe_allow_html=True)

                st.markdown("<br>", unsafe_allow_html=True)

                # ── 4 CARDS DE ANÁLISE ───────────────────────────────────────
                col_a, col_b = st.columns(2)

                with col_a:
                    erros_ort = resultado.get("erros_ortografia", [])
                    st.markdown('<div class="analysis-card">', unsafe_allow_html=True)
                    st.markdown('<div class="analysis-card-title" style="color:#dc2626">🔴 Erros de Ortografia</div>', unsafe_allow_html=True)
                    if erros_ort:
                        for e in erros_ort:
                            st.markdown(f'<div class="item-pill pill-erro-ort">✕ {e}</div>', unsafe_allow_html=True)
                    else:
                        st.markdown('<div class="empty-state">✅ Nenhum erro encontrado!</div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)

                with col_b:
                    erros_pont = resultado.get("erros_pontuacao", [])
                    st.markdown('<div class="analysis-card">', unsafe_allow_html=True)
                    st.markdown('<div class="analysis-card-title" style="color:#ea580c">🟠 Erros de Pontuação</div>', unsafe_allow_html=True)
                    if erros_pont:
                        for e in erros_pont:
                            st.markdown(f'<div class="item-pill pill-erro-pont">✕ {e}</div>', unsafe_allow_html=True)
                    else:
                        st.markdown('<div class="empty-state">✅ Nenhum erro encontrado!</div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)

                st.markdown("<br>", unsafe_allow_html=True)

                col_c, col_d = st.columns(2)

                with col_c:
                    pontos = resultado.get("pontos_positivos")
