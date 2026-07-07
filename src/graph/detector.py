"""
graph/detector.py
Detector de Alucinação por checagem contra base de conhecimento (grounding).

A KB (data/knowledge_base.py) é modelada como um grafo dirigido: cada
KBFact(sujeito, predicado, objeto) vira uma aresta sujeito --predicado--> objeto.
Uma afirmação (Claim) é a mesma estrutura, só que "alegada". Checar a
afirmação é perguntar ao grafo:

  1) Existe uma aresta sujeito --predicado--> objeto_alegado ?
       sim -> FATO (a KB confirma exatamente o que foi dito)

  2) Existe alguma aresta sujeito --predicado--> outro_objeto (objeto
     diferente do alegado) ?
       sim -> ERRO  (a KB conhece a resposta certa e ela não é essa —
                      é exatamente a assinatura de uma alucinação:
                      afirmação estruturalmente válida, mas semanticamente
                      incorreta)

  3) Não existe nenhuma aresta sujeito --predicado--> qualquer coisa ?
       -> SUPOSIÇÃO (a KB não cobre essa relação — não dá pra confirmar
                      nem contradizer com o que se sabe)

Essa é a mesma ideia central do enunciado (2.4): a mesma pergunta pode ter
respostas diferentes dependendo de você olhar só a alegação isolada (não dá
pra saber se é verdade) ou a alegação à luz da base de conhecimento
(dá pra classificar com evidência).
"""

from __future__ import annotations

import networkx as nx

from data.claims import Claim
from data.knowledge_base import KBFact, KNOWLEDGE_BASE


def build_kb_graph(facts: list[KBFact] = KNOWLEDGE_BASE) -> nx.MultiDiGraph:
    """Constrói o grafo da base de conhecimento: sujeito --predicado--> objeto."""
    G = nx.MultiDiGraph()
    for f in facts:
        G.add_edge(f.sujeito, f.objeto, predicado=f.predicado)
    return G


def _fatos_do_sujeito_predicado(G: nx.MultiDiGraph, sujeito: str, predicado: str) -> list[str]:
    """Retorna todos os objetos conhecidos pela KB para (sujeito, predicado)."""
    if sujeito not in G:
        return []
    objetos = []
    for _, objeto, data in G.out_edges(sujeito, data=True):
        if data.get("predicado") == predicado:
            objetos.append(objeto)
    return objetos


def classify_claim(claim: Claim, G: nx.MultiDiGraph | None = None) -> dict:
    """Confere a afirmação contra a base de conhecimento e retorna o veredito."""
    if G is None:
        G = build_kb_graph()

    objetos_conhecidos = _fatos_do_sujeito_predicado(G, claim.sujeito, claim.predicado)

    if claim.objeto_alegado in objetos_conhecidos:
        veredito = "Fato"
        motivo = (
            f"A base de conhecimento confirma: {claim.sujeito} --{claim.predicado}--> "
            f"{claim.objeto_alegado}."
        )
        evidencia = f"{claim.sujeito} --{claim.predicado}--> {claim.objeto_alegado}"

    elif objetos_conhecidos:
        veredito = "Erro"
        certo = objetos_conhecidos[0]
        motivo = (
            f"A base de conhecimento tem uma resposta diferente para "
            f"'{claim.sujeito} {claim.predicado}': é '{certo}', não "
            f"'{claim.objeto_alegado}'. Contradição factual — alucinação."
        )
        evidencia = f"{claim.sujeito} --{claim.predicado}--> {certo}  (correto)"

    else:
        veredito = "Suposição"
        motivo = (
            f"A base de conhecimento não tem nenhum fato sobre "
            f"'{claim.sujeito} {claim.predicado}'. Não dá pra confirmar nem "
            f"contradizer — a afirmação fica sem verificação."
        )
        evidencia = None

    return {
        "veredito": veredito,
        "motivo": motivo,
        "evidencia": evidencia,
        "bate_com_esperado": veredito == claim.veredito_esperado,
    }