"""
reports/json_exporter.py
Gera um relatório JSON com estatísticas e dados completos do grafo.
"""

import json
from collections import Counter

from data.nodes import Node
from data.edges import Edge
from config.settings import PROJECT_TITLE, PROJECT_AUTHOR


def save_summary(nodes: list[Node], edges: list[Edge], output_path: str) -> None:
    """Salva o sumário analítico do grafo em JSON."""

    classe_count = Counter(n.classe for n in nodes)
    tipo_count   = Counter(e.tipo   for e in edges)
    conf_media   = round(sum(e.confianca for e in edges) / len(edges), 3) if edges else 0.0

    summary = {
        "titulo": PROJECT_TITLE,
        "autor":  PROJECT_AUTHOR,
        "grafo": {
            "vertices": len(nodes),
            "arestas":  len(edges),
            "distribuicao_vertices": dict(classe_count),
            "distribuicao_arestas":  dict(tipo_count),
            "confianca_media":       conf_media,
            "confianca_min":         min(e.confianca for e in edges),
            "confianca_max":         max(e.confianca for e in edges),
        },
        "nos": [
            {"id": n.id, "label": n.label, "classe": n.classe, "descricao": n.descricao}
            for n in nodes
        ],
        "arestas": [
            {
                "de":        e.source,
                "para":      e.target,
                "relacao":   e.relacao,
                "confianca": e.confianca,
                "tipo":      e.tipo,
            }
            for e in edges
        ],
    }

    with open(output_path, "w", encoding="utf-8") as fh:
        json.dump(summary, fh, ensure_ascii=False, indent=2)

    print(f"[JSON] {output_path}  (conf. média: {conf_media})")
