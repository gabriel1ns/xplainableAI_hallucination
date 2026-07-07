"""
data/claims.py
Afirmações pré-cadastradas para o Detector de Alucinação (aba 4 do app).

Cada Claim é uma frase atribuída a um LLM, já decomposta na mesma forma
(sujeito, predicado, objeto_alegado) usada em data/knowledge_base.py — é
essa decomposição que permite comparar a afirmação com a base de fatos.

`veredito_esperado` existe só pra você conferir, ao rodar o app, se a
lógica do detector (graph/detector.py) concorda com o gabarito.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Claim:
    id: str
    modelo: str
    texto: str
    sujeito: str
    predicado: str
    objeto_alegado: str
    veredito_esperado: str  # Fato | Erro | Suposição


CLAIMS: list[Claim] = [
    Claim(
        "C1", "GPT4",
        "O GPT-4 foi desenvolvido pela OpenAI.",
        "GPT-4", "desenvolvido_por", "OpenAI",
        veredito_esperado="Fato",
    ),
    Claim(
        "C2", "Claude3",
        "O Claude 3 foi desenvolvido pelo Google.",
        "Claude 3", "desenvolvido_por", "Google",
        veredito_esperado="Erro",
    ),
    Claim(
        "C3", "Gemini",
        "O Gemini foi desenvolvido pela Microsoft.",
        "Gemini", "desenvolvido_por", "Microsoft",
        veredito_esperado="Erro",
    ),
    Claim(
        "C4", "GPT4",
        "O GPT-4 usa arquitetura transformer.",
        "GPT-4", "usa_arquitetura", "transformer",
        veredito_esperado="Fato",
    ),
    Claim(
        "C5", "Claude3",
        "O Claude 3 tem 500 bilhões de parâmetros.",
        "Claude 3", "numero_parametros", "500 bilhões",
        veredito_esperado="Suposição",
    ),
    Claim(
        "C6", "Gemini",
        "O Gemini foi lançado originalmente em 1998.",
        "Gemini", "lancado_em", "1998",
        veredito_esperado="Suposição",
    ),
    Claim(
        "C7", "Geral",
        "Um LLM pode gerar alucinação.",
        "LLM", "pode_gerar", "alucinação",
        veredito_esperado="Fato",
    ),
]