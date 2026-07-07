"""
data/edges.py
Definição das arestas do grafo.

Cada aresta é uma dataclass com:
  source    – id do nó de origem
  target    – id do nó de destino
  relacao   – nome da relação semântica
  confianca – peso [0.0, 1.0]
  tipo      – classe semântica da aresta (Fato | Suposição | Erro)
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Edge:
    source: str
    target: str
    relacao: str
    confianca: float
    tipo: str


EDGES: list[Edge] = [
    Edge("IA",         "LLM",        "instancia",        0.95, "Fato"),
    Edge("LLM",        "PADRAO_EST", "opera_com",        0.95, "Fato"),
    Edge("LLM",        "ALUCINACAO", "pode_gerar",       0.90, "Fato"),
    Edge("LLM",        "FATO",       "pode_confirmar",   0.90, "Fato"),
    Edge("LLM",        "SUPOSICAO",  "pode_assumir",     0.65, "Suposição"),
    Edge("PADRAO_EST", "ALUCINACAO", "causa",            0.85, "Fato"),
    Edge("ALUCINACAO", "ERRO_SEM",   "manifesta_como",   0.90, "Fato"),
    Edge("ALUCINACAO", "PROP_ERRO",  "leva_a",           0.80, "Fato"),
    Edge("ALUCINACAO", "AMB",        "gera",             0.75, "Fato"),
    Edge("GRAFO",      "CONFIANCA",  "contem",           0.95, "Fato"),
    Edge("GRAFO",      "CAMADA_SEM", "integra",          0.90, "Fato"),
    Edge("ONTOLOGIA",  "CAMADA_SEM", "fornece",          0.95, "Fato"),
    Edge("ONTOLOGIA",  "FATO",       "classifica",       0.95, "Fato"),
    Edge("ONTOLOGIA",  "SUPOSICAO",  "classifica",       0.95, "Fato"),
    Edge("ONTOLOGIA",  "ERRO_SEM",   "classifica",       0.95, "Fato"),
    Edge("CAMADA_SEM", "CLASSIF",    "permite",          0.90, "Fato"),
    Edge("CAMADA_SEM", "INTERP",     "produz",           0.88, "Fato"),
    Edge("CLASSIF",    "CONF_IA",    "aumenta",          0.85, "Fato"),
    Edge("INTERP",     "CONF_IA",    "melhora",          0.90, "Fato"),
    Edge("CONFIANCA",  "SUPOSICAO",  "representa",       0.70, "Suposição"),
    Edge("PROP_ERRO",  "CONF_IA",    "reduz",            0.80, "Fato"),
    Edge("AMB",        "CONF_IA",    "compromete",       0.75, "Fato"),
    Edge("SUPOSICAO",  "ALUCINACAO", "pode_se_tornar",   0.60, "Suposição"),
    Edge("FATO",       "INTERP",     "sustenta",         0.95, "Fato"),
]