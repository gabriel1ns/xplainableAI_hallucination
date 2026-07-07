"""
app.py
Projeto Final — Unidade 2 — Grafos e Ontologias: Da Estrutura ao Significado

Reaproveita o pipeline já existente (src/data, src/graph, src/ontology) e
adiciona a camada interativa Streamlit exigida pelo enunciado:

  Aba 1 — Grafo Estrutural : visualização + métricas do grafo puro
  Aba 2 — Grafo Semântico  : mesma visualização colorida por classe + ontologia
  Aba 3 — Comparação       : mesma pergunta (caminho mínimo), duas respostas

Rodar com:  streamlit run app.py
"""

import os
import sys

import streamlit as st
import streamlit.components.v1 as components

_ROOT = os.path.dirname(os.path.abspath(__file__))
_SRC = os.path.join(_ROOT, "src")
if _SRC not in sys.path:
    sys.path.insert(0, _SRC)

from data.nodes import NODES
from data.edges import EDGES
from data.claims import CLAIMS
from data.knowledge_base import KNOWLEDGE_BASE
from config.settings import PROJECT_TITLE, PROJECT_AUTHOR, NODE_STYLES, EDGE_STYLES
from graph.builder import build_network, build_network_plain
from graph.detector import build_kb_graph, classify_claim
from graph.semantics import (
    TIPO_PENALTY,
    build_structural_graph,
    build_semantic_graph,
    degree_table,
    average_degree,
    diameter,
    connected_components,
    max_matching,
    betweenness,
    has_cycle,
    is_bipartite,
    shortest_path,
    compare_paths,
    NOTABLE_PAIRS,
)


st.set_page_config(page_title=PROJECT_TITLE, layout="wide")

NODE_IDS = [n.id for n in NODES]
NODE_LABELS = {n.id: f"{n.id} — {n.label}" for n in NODES}
G_STRUCT = build_structural_graph(NODES, EDGES)
G_SEM = build_semantic_graph(NODES, EDGES)
G_KB = build_kb_graph(KNOWLEDGE_BASE)


def render_pyvis(net) -> None:
    """Renderiza um Network PyVis dentro do Streamlit."""
    html = net.generate_html(notebook=False)
    components.html(html, height=560, scrolling=True)


def render_legend() -> None:
    cols = st.columns(len(NODE_STYLES))
    for col, (classe, style) in zip(cols, NODE_STYLES.items()):
        with col:
            st.markdown(
                f"<span style='color:{style['color']};font-size:22px'>●</span> "
                f"**{classe}** ({style['shape']})",
                unsafe_allow_html=True,
            )
    st.caption(
        "Relações nomeadas (arestas) carregam também um **tipo semântico** "
        "(Fato / Suposição / Erro) e um **peso de confiança** [0,1] — "
        "visíveis ao passar o mouse sobre a aresta no grafo semântico."
    )


st.title(f"🧠 {PROJECT_TITLE}")
st.caption(f"Grafos e Ontologias: Da Estrutura ao Significado · {PROJECT_AUTHOR}")

tab_struct, tab_sem, tab_comp, tab_detector = st.tabs(
    ["📐 Grafo Estrutural", "🧩 Grafo Semântico", "⚖️ Comparação", "🔎 Detector de Alucinação"]
)

# ── Aba 1 — Grafo Estrutural ────────────────────────────────────────────────
with tab_struct:
    st.markdown(
        "Aqui todos os vértices e todas as arestas são tratados **como iguais** "
        "— sem tipo, sem categoria, sem contexto. Só a estrutura pura do grafo "
        f"G=(V,E), com **{G_STRUCT.number_of_nodes()} vértices** e "
        f"**{G_STRUCT.number_of_edges()} arestas**."
    )
    render_pyvis(build_network_plain(NODES, EDGES))

    st.subheader("Métricas estruturais")
    c1, c2 = st.columns(2)

    with c1:
        st.metric("Grau médio", average_degree(G_STRUCT))
        d = diameter(G_STRUCT)
        st.metric("Diâmetro (maior componente)", d if d is not None else "—")
        comps = connected_components(G_STRUCT)
        st.metric("Componentes conexas", len(comps))
        st.metric("Tem ciclo?", "Sim" if has_cycle(G_STRUCT) else "Não")
        st.metric("É bipartido?", "Sim" if is_bipartite(G_STRUCT) else "Não")

    with c2:
        st.markdown("**Vértice mais central (betweenness)**")
        st.dataframe(betweenness(G_STRUCT)[:5], hide_index=True, use_container_width=True)
        st.markdown("**Emparelhamento máximo**")
        st.write(max_matching(G_STRUCT))

    st.markdown("**Grau de cada vértice**")
    st.dataframe(degree_table(G_STRUCT), hide_index=True, use_container_width=True)

    st.markdown("**Caminho mínimo (BFS, por número de saltos)**")
    cs1, cs2 = st.columns(2)
    src = cs1.selectbox("Origem", NODE_IDS, format_func=lambda x: NODE_LABELS[x], key="struct_src")
    tgt = cs2.selectbox("Destino", NODE_IDS, index=1, format_func=lambda x: NODE_LABELS[x], key="struct_tgt")
    path, cost = shortest_path(G_STRUCT, src, tgt, weighted=False)
    if path:
        st.success(f"{' → '.join(path)}   ·   {cost} salto(s)")
    else:
        st.warning("Não existe caminho dirigido entre esses vértices.")

# ── Aba 2 — Grafo Semântico ──────────────────────────────────────────────────
with tab_sem:
    st.markdown(
        "Aqui a **ontologia** entra em cena: cada vértice tem uma classe, cada "
        "aresta tem uma relação nomeada, um tipo semântico e um peso de "
        "confiança. Cores por classe, espessura por confiança."
    )
    render_pyvis(build_network(NODES, EDGES))
    render_legend()

    with st.expander("Ontologia — classes, relações e regra aplicada"):
        st.markdown(
            "**Classes de vértice:** " + ", ".join(NODE_STYLES.keys())
        )
        st.markdown(
            "**Tipos de relação (aresta):** " + ", ".join(EDGE_STYLES.keys())
        )
        st.markdown("**Regra ontológica aplicada ao custo de caminho:**")
        st.latex(r"\text{peso\_semantico(aresta)} = (1 - \text{confiança}) \times \text{penalidade(tipo)}")
        st.table(
            [{"tipo": k, "penalidade": v} for k, v in TIPO_PENALTY.items()]
        )
        st.caption(
            "Arestas do tipo Suposição ou Erro Semântico custam mais para "
            "atravessar: a ontologia prioriza caminhos que passam por "
            "informação verificada (Fato), mesmo quando isso não é o caminho "
            "com menos saltos. Isso reflete diretamente a hierarquia "
            "TipoConexao → Fato | Suposição | ErroSemântico definida em "
            "`ontology/schema.py` (OWL DL, disponível em `output/*.owl` "
            "após rodar `python main.py`)."
        )

    st.subheader("Métricas semânticas")
    st.markdown("**Vértice mais central (betweenness ponderado pelo custo semântico)**")
    st.dataframe(betweenness(G_SEM, weighted=True)[:5], hide_index=True, use_container_width=True)

    st.markdown("**Caminho mínimo (Dijkstra, por custo semântico)**")
    cs1, cs2 = st.columns(2)
    src2 = cs1.selectbox("Origem", NODE_IDS, format_func=lambda x: NODE_LABELS[x], key="sem_src")
    tgt2 = cs2.selectbox("Destino", NODE_IDS, index=1, format_func=lambda x: NODE_LABELS[x], key="sem_tgt")
    path2, cost2 = shortest_path(G_SEM, src2, tgt2, weighted=True)
    if path2:
        st.success(f"{' → '.join(path2)}   ·   custo semântico = {cost2}")
    else:
        st.warning("Não existe caminho dirigido entre esses vértices.")

# ── Aba 3 — Comparação ───────────────────────────────────────────────────────
with tab_comp:
    st.markdown(
        "Mesma pergunta — **qual o caminho mínimo entre X e Y?** — respondida "
        "duas vezes: uma vez pela estrutura pura, outra vez pela ontologia."
    )

    cs1, cs2 = st.columns(2)
    src3 = cs1.selectbox("Origem", NODE_IDS, format_func=lambda x: NODE_LABELS[x], key="cmp_src", index=NODE_IDS.index("GRAFO"))
    tgt3 = cs2.selectbox("Destino", NODE_IDS, format_func=lambda x: NODE_LABELS[x], key="cmp_tgt", index=NODE_IDS.index("CONF_IA"))

    result = compare_paths(G_STRUCT, G_SEM, src3, tgt3)

    colA, colB = st.columns(2)
    with colA:
        st.markdown("#### 📐 Sem ontologia")
        if result["struct_path"]:
            st.info(f"{' → '.join(result['struct_path'])}\n\n**{result['struct_cost']} salto(s)**")
        else:
            st.warning("Sem caminho.")
    with colB:
        st.markdown("#### 🧩 Com ontologia")
        if result["sem_path"]:
            st.success(f"{' → '.join(result['sem_path'])}\n\n**custo semântico = {result['sem_cost']}**")
        else:
            st.warning("Sem caminho.")

    if result["diferente"]:
        st.markdown(
            "🔎 **A ontologia mudou a resposta.** O grafo estrutural escolheria "
            "um caminho que a ontologia evita, por passar por uma aresta menos "
            "confiável (tipo Suposição/Erro ou confiança baixa) — mesmo que "
            "estruturalmente pareça equivalente ou mais curto."
        )
    else:
        st.markdown(
            "Para este par, os dois caminhos coincidem — não há aresta de "
            "baixa confiança na rota mais curta. Veja abaixo os pares onde a "
            "diferença aparece."
        )

    st.divider()
    st.subheader("Casos notáveis (diferença demonstrada)")
    for s, t, explicacao in NOTABLE_PAIRS:
        r = compare_paths(G_STRUCT, G_SEM, s, t)
        with st.container(border=True):
            st.markdown(f"**{s} → {t}**")
            c1, c2 = st.columns(2)
            c1.write(f"Sem ontologia: `{' → '.join(r['struct_path'])}` ({r['struct_cost']} saltos)")
            c2.write(f"Com ontologia: `{' → '.join(r['sem_path'])}` (custo {r['sem_cost']})")
            st.caption(explicacao)

# ── Aba 4 — Detector de Alucinação ──────────────────────────────────────────
with tab_detector:
    st.markdown(
        "Escolha uma afirmação atribuída a um LLM. O sistema confere a "
        "afirmação contra uma **base de conhecimento** (um pequeno grafo de "
        "fatos verificados, `sujeito --predicado--> objeto`) e decide:\n\n"
        "- a KB **confirma** exatamente isso → 🟢 **Fato**\n"
        "- a KB tem uma resposta **diferente** pra mesma pergunta → 🔴 **Erro** "
        "(alucinação — a afirmação é estruturalmente uma frase válida, mas "
        "contradiz o que se sabe)\n"
        "- a KB **não cobre** essa relação → 🟡 **Suposição** (não dá pra "
        "confirmar nem negar)"
    )

    with st.expander("Ver a base de conhecimento completa"):
        st.dataframe(
            [{"sujeito": f.sujeito, "predicado": f.predicado, "objeto": f.objeto} for f in KNOWLEDGE_BASE],
            hide_index=True, use_container_width=True,
        )

    claim_ids = [c.id for c in CLAIMS]
    claim_labels = {c.id: f"[{c.modelo}] {c.texto}" for c in CLAIMS}
    chosen_id = st.selectbox(
        "Afirmação a avaliar", claim_ids, format_func=lambda x: claim_labels[x]
    )
    claim = next(c for c in CLAIMS if c.id == chosen_id)

    with st.container(border=True):
        st.markdown(f"**Modelo que gerou a afirmação:** {claim.modelo}")
        st.markdown(f"**Texto:** {claim.texto}")
        st.code(f"{claim.sujeito}  --{claim.predicado}-->  {claim.objeto_alegado}", language=None)

    resultado = classify_claim(claim, G_KB)
    veredito = resultado["veredito"]
    cor = {"Fato": "🟢", "Suposição": "🟡", "Erro": "🔴"}[veredito]

    st.subheader(f"Veredito: {cor} {veredito}")
    st.write(resultado["motivo"])
    if resultado["evidencia"]:
        st.code(resultado["evidencia"], language=None)

    if not resultado["bate_com_esperado"]:
        st.warning(
            f"(Gabarito interno esperava '{claim.veredito_esperado}' — "
            "confira os fatos cadastrados se isso te surpreendeu.)"
        )

st.divider()
st.caption(
    "Teoria dos Grafos · Prof. Cleyton Rodrigues · Escola Politécnica de Pernambuco. "
    "Pipeline original (HTML estático + OWL) continua disponível via `python main.py`."
)