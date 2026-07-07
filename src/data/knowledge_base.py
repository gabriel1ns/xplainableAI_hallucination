"""
data/knowledge_base.py
Base de conhecimento factual do domínio, representada como triplas
(sujeito, predicado, objeto) — ou seja, ela É um grafo dirigido.

Essa é a fonte da verdade contra a qual o Detector de Alucinação (aba 4 do
app) confere cada afirmação. Uma afirmação é decomposta na mesma forma
(sujeito, predicado, objeto) e comparada:

  - existe (sujeito, predicado, objeto_igual) na KB  -> Fato
  - existe (sujeito, predicado, objeto_diferente)     -> Erro (contradição
    factual = a assinatura clássica de uma alucinação)
  - não existe nenhuma tripla com esse (sujeito, predicado) na KB
    -> Suposição (a KB não cobre isso, não dá pra confirmar nem negar)

Fatos abaixo são verificáveis publicamente (desenvolvedor, arquitetura,
natureza do modelo). Mantidos simples de propósito — o objetivo é a lógica
de checagem, não uma KB exaustiva.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class KBFact:
    sujeito: str
    predicado: str
    objeto: str


KNOWLEDGE_BASE: list[KBFact] = [
    KBFact("GPT-4",    "desenvolvido_por", "OpenAI"),
    KBFact("Claude 3", "desenvolvido_por", "Anthropic"),
    KBFact("Gemini",   "desenvolvido_por", "Google"),

    KBFact("GPT-4",    "tipo", "modelo de linguagem"),
    KBFact("Claude 3", "tipo", "modelo de linguagem"),
    KBFact("Gemini",   "tipo", "modelo de linguagem"),

    KBFact("GPT-4",    "usa_arquitetura", "transformer"),
    KBFact("Claude 3", "usa_arquitetura", "transformer"),
    KBFact("Gemini",   "usa_arquitetura", "transformer"),

    KBFact("LLM",        "baseia_se_em", "padrão estatístico"),
    KBFact("LLM",        "pode_gerar",   "alucinação"),
    KBFact("Alucinação", "definida_como","resposta plausível porém incorreta"),
]