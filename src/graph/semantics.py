"""
graph/semantics.py
Camada de análise para o Projeto Final (Unidade 2).

Constrói duas visões do mesmo grafo G=(V,E):

  - grafo estrutural : todos os vértices e arestas tratados como iguais
                        (sem tipo, sem peso semântico -> BFS por número de saltos)
  - grafo semântico   : usa a ontologia para atribuir um "custo de confiabilidade"
                        a cada aresta -> Dijkstra por peso semântico

Regra ontológica (2.3 do enunciado):
  Toda aresta cuja classe semântica (TipoConexao) é Suposição ou ErroSemântico
  recebe uma penalidade multiplicativa no cálculo de caminhos. A ideia é que
  informação não verificada (Suposição) ou incorreta (ErroSemântico) não deve
  ser preferida na propagação de conhecimento, mesmo quando estruturalmente
  é o caminho com menos saltos.

  peso_semantico(aresta) = (1 - confianca) * PENALIDADE[tipo]

  PENALIDADE = {"Fato": 1.0, "Suposição": 1.8, "Erro": 2.5}

Isso não é ad-hoc: espelha a hierarquia OWL já definida em ontology/schema.py
(TipoConexao -> Fato | Suposicao | ErroSemantico), só que expressa como peso
numérico em vez de axioma DL, para uso rápido em NetworkX/Streamlit.
"""

from __future__ import annotations

import networkx as nx

from data.nodes import Node
from data.edges import Edge


TIPO_PENALTY: dict[str, float] = {
    "Fato": 1.0,
    "Suposição": 1.8,
    "Erro": 2.5,
}


def semantic_weight(edge: Edge) -> float:
    """Custo de uma aresta na visão semântica: quanto maior, menos confiável."""
    penalty = TIPO_PENALTY.get(edge.tipo, TIPO_PENALTY["Fato"])
    return round(max(1 - edge.confianca, 0.01) * penalty, 4)


def build_structural_graph(nodes: list[Node], edges: list[Edge]) -> nx.DiGraph:
    """Grafo puro: todo vértice e toda aresta tem peso 1 (sem semântica)."""
    G = nx.DiGraph()
    for n in nodes:
        G.add_node(n.id, label=n.label)
    for e in edges:
        G.add_edge(e.source, e.target, weight=1)
    return G


def build_semantic_graph(nodes: list[Node], edges: list[Edge]) -> nx.DiGraph:
    """Grafo com ontologia: vértices carregam classe, arestas carregam
    relação nomeada, tipo semântico e peso de confiabilidade."""
    G = nx.DiGraph()
    for n in nodes:
        G.add_node(n.id, label=n.label, classe=n.classe)
    for e in edges:
        G.add_edge(
            e.source, e.target,
            relacao=e.relacao,
            tipo=e.tipo,
            confianca=e.confianca,
            weight=semantic_weight(e),
        )
    return G


# ── Métricas estruturais (grafo puro) ───────────────────────────────────────

def degree_table(G: nx.DiGraph) -> list[dict]:
    return [
        {"vertice": n, "grau_entrada": G.in_degree(n), "grau_saida": G.out_degree(n),
         "grau_total": G.in_degree(n) + G.out_degree(n)}
        for n in G.nodes()
    ]


def average_degree(G: nx.DiGraph) -> float:
    n = G.number_of_nodes()
    if n == 0:
        return 0.0
    return round(sum(d for _, d in G.degree()) / n, 3)


def diameter(G: nx.DiGraph) -> int | None:
    """Diâmetro sobre o maior componente (grafo tratado como não-dirigido,
    pois o grafo dirigido original não é fortemente conexo)."""
    UG = G.to_undirected()
    if UG.number_of_nodes() == 0:
        return None
    largest_cc = max(nx.connected_components(UG), key=len)
    sub = UG.subgraph(largest_cc)
    if sub.number_of_nodes() < 2:
        return 0
    return nx.diameter(sub)


def connected_components(G: nx.DiGraph) -> list[list[str]]:
    UG = G.to_undirected()
    return [sorted(c) for c in nx.connected_components(UG)]


def max_matching(G: nx.DiGraph) -> list[tuple[str, str]]:
    UG = G.to_undirected()
    matching = nx.max_weight_matching(UG, maxcardinality=True)
    return sorted(tuple(sorted(pair)) for pair in matching)


def betweenness(G: nx.DiGraph, weighted: bool = False) -> list[dict]:
    kwargs = {"weight": "weight"} if weighted else {}
    bc = nx.betweenness_centrality(G, **kwargs)
    ranked = sorted(bc.items(), key=lambda kv: kv[1], reverse=True)
    return [{"vertice": v, "centralidade": round(c, 4)} for v, c in ranked]


def has_cycle(G: nx.DiGraph) -> bool:
    return not nx.is_directed_acyclic_graph(G)


def is_bipartite(G: nx.DiGraph) -> bool:
    UG = G.to_undirected()
    return nx.is_bipartite(UG)


def shortest_path(G: nx.DiGraph, source: str, target: str, weighted: bool = False):
    """Retorna (caminho, custo) ou (None, None) se não houver caminho."""
    try:
        if weighted:
            path = nx.shortest_path(G, source, target, weight="weight")
            cost = nx.shortest_path_length(G, source, target, weight="weight")
        else:
            path = nx.shortest_path(G, source, target)
            cost = len(path) - 1
        return path, round(cost, 4) if isinstance(cost, float) else cost
    except (nx.NetworkXNoPath, nx.NodeNotFound):
        return None, None


# ── Casos notáveis pré-computados (para a aba de Comparação) ───────────────

NOTABLE_PAIRS: list[tuple[str, str, str]] = [
    ("ONTOLOGIA", "INTERP",
     "A ontologia desempata a favor do caminho que passa pela classe Fato, "
     "mais confiável, em vez do caminho de mesmo tamanho via Camada Semântica."),
    ("GRAFO", "CONF_IA",
     "Entre duas rotas de mesmo número de saltos, a ontologia prefere a que "
     "acumula menos penalidade de tipo/confiança ao longo do caminho."),
]


def compare_paths(G_struct: nx.DiGraph, G_sem: nx.DiGraph, source: str, target: str) -> dict:
    struct_path, struct_cost = shortest_path(G_struct, source, target, weighted=False)
    sem_path, sem_cost = shortest_path(G_sem, source, target, weighted=True)
    return {
        "source": source,
        "target": target,
        "struct_path": struct_path,
        "struct_cost": struct_cost,
        "sem_path": sem_path,
        "sem_cost": sem_cost,
        "diferente": struct_path != sem_path,
    }