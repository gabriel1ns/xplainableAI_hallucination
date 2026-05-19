"""
data/nodes.py
Definição dos vértices do grafo e dos indivíduos da ontologia.

Cada nó é uma dataclass com:
  id          – identificador único (sem espaços)
  label       – rótulo legível
  classe      – classe semântica (Fato | Suposição | Erro | Conceito)
  descricao   – descrição textual para tooltip e ontologia
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Node:
    id: str
    label: str
    classe: str
    descricao: str


NODES: list[Node] = [
    Node("IA",         "Inteligência Artificial",    "Conceito",
         "Sistema computacional baseado em padrões estatísticos"),
    Node("LLM",        "Modelo de Linguagem (LLM)",  "Conceito",
         "Modelo que gera texto por probabilidade"),
    Node("ALUCINACAO", "Alucinação",                 "Erro",
         "Resposta plausível, porém incorreta ou inexistente"),
    Node("PADRAO_EST", "Padrão Estatístico",         "Conceito",
         "Base de inferência dos LLMs"),
    Node("GRAFO",      "Grafo G=(V,E)",              "Conceito",
         "Estrutura matemática para representar conexões"),
    Node("ONTOLOGIA",  "Ontologia",                  "Conceito",
         "Camada semântica que atribui significado"),
    Node("FATO",       "Fato",                       "Fato",
         "Informação verificada e verdadeira"),
    Node("SUPOSICAO",  "Suposição",                  "Suposição",
         "Conexão plausível mas não verificada"),
    Node("ERRO_SEM",   "Erro Semântico",             "Erro",
         "Conexão estruturalmente válida, semanticamente incorreta"),
    Node("CONFIANCA",  "Peso de Confiança",          "Conceito",
         "Nível de certeza atribuído a uma aresta"),
    Node("CAMADA_SEM", "Camada Semântica",           "Conceito",
         "Integração entre grafo e ontologia"),
    Node("PROP_ERRO",  "Propagação de Erro",         "Erro",
         "Disseminação de informações incorretas no sistema"),
    Node("INTERP",     "Modelo Interpretável",       "Fato",
         "Sistema confiável com distinção fato/erro"),
    Node("CLASSIF",    "Classificação de Conexões",  "Fato",
         "Processo de categorizar relações do grafo"),
    Node("AMB",        "Ambiguidade",                "Erro",
         "Falta de clareza semântica nas respostas"),
    Node("CONF_IA",    "Confiabilidade da IA",       "Conceito",
         "Grau de precisão e veracidade do sistema"),
]

@dataclass(frozen=True)
class Individual:
    name: str
    owl_class: str
    descricao: str


INDIVIDUALS: list[Individual] = [
    Individual("GPT4",              "ModeloLinguagem",   "GPT-4 da OpenAI"),
    Individual("Claude3",           "ModeloLinguagem",   "Claude 3 da Anthropic"),
    Individual("Gemini",            "ModeloLinguagem",   "Gemini do Google"),
    Individual("GrafoConhecimento", "Grafo",             "Grafo G=(V,E) do domínio de IA"),
    Individual("OntologiaAI",       "Ontologia",         "Ontologia deste projeto"),
    Individual("CamadaIntegrada",   "CamadaSemantica",   "Integração grafo+ontologia"),
    Individual("FatoVerificado1",   "Fato",              "LLMs operam por padrão estatístico"),
    Individual("Suposicao1",        "Suposicao",         "O modelo compreende o texto"),
    Individual("AlucinacaoEx1",     "Alucinacao",        "Citação falsa de autor inexistente"),
    Individual("AlucinacaoEx2",     "Alucinacao",        "Data histórica incorreta"),
    Individual("PropErro1",         "PropagacaoDeErro",  "Alucinação aceita como fato em pipeline"),
    Individual("PesoAlto",          "PesoConfianca",     "Peso 0.95 — alta confiança"),
    Individual("PesoBaixo",         "PesoConfianca",     "Peso 0.40 — baixa confiança"),
]
