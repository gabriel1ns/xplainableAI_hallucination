"""
graph/builder.py
Monta o objeto Network do PyVis a partir de nós e arestas.
Não sabe nada de arquivo — só constrói a rede em memória.
"""

from pyvis.network import Network

from config.settings import (
    GRAPH_BG, GRAPH_FONT, GRAPH_HEIGHT, GRAPH_WIDTH,
    NODE_STYLES, EDGE_STYLES, PHYSICS_OPTIONS,
)
from data.nodes import Node
from data.edges import Edge


def build_network(nodes: list[Node], edges: list[Edge]) -> Network:
    """Retorna um Network PyVis configurado e pronto para salvar."""

    net = Network(
        height=GRAPH_HEIGHT,
        width=GRAPH_WIDTH,
        bgcolor=GRAPH_BG,
        font_color=GRAPH_FONT,
        directed=True,
        notebook=False,
    )
    net.set_options(PHYSICS_OPTIONS)

    for node in nodes:
        style = NODE_STYLES[node.classe]
        net.add_node(
            node.id,
            label=node.label,
            title=f"<b>{node.label}</b><br><i>Classe: {node.classe}</i><br>{node.descricao}",
            color=style["color"],
            shape=style["shape"],
            size=style["size"],
            font={"color": "#ffffff", "size": 13, "face": "monospace"},
            borderWidth=2,
            borderWidthSelected=5,
        )

    for edge in edges:
        es = EDGE_STYLES.get(edge.tipo, EDGE_STYLES["Fato"])
        net.add_edge(
            edge.source,
            edge.target,
            title=f"<b>{edge.relacao}</b><br>Confiança: {edge.confianca:.0%}<br>Tipo: {edge.tipo}",
            label=edge.relacao,
            color=es["color"],
            dashes=es["dashes"],
            width=max(1.5, edge.confianca * 5),
            font={"color": "#aaaaaa", "size": 10, "align": "middle"},
        )

    return net


def build_network_plain(nodes: list[Node], edges: list[Edge]) -> Network:
    """Retorna a MESMA rede, mas sem nenhuma informação semântica aplicada:
    todos os vértices e todas as arestas usam o mesmo estilo, exatamente
    como pede a visão 'Grafo Estrutural' do Projeto Final (2.2) — sem tipo,
    sem categoria, sem contexto."""

    net = Network(
        height=GRAPH_HEIGHT,
        width=GRAPH_WIDTH,
        bgcolor=GRAPH_BG,
        font_color=GRAPH_FONT,
        directed=True,
        notebook=False,
    )
    net.set_options(PHYSICS_OPTIONS)

    for node in nodes:
        net.add_node(
            node.id,
            label=node.label,
            title=node.label,
            color="#6e7681",
            shape="dot",
            size=22,
            font={"color": "#ffffff", "size": 13, "face": "monospace"},
            borderWidth=1,
        )

    for edge in edges:
        net.add_edge(
            edge.source,
            edge.target,
            title=f"{edge.source} -> {edge.target}",
            color="#6e7681",
            dashes=False,
            width=1.5,
            font={"color": "#8b949e", "size": 9, "align": "middle"},
        )

    return net