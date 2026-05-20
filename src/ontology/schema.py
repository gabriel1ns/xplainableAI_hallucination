"""
ontology/schema.py
Define toda a estrutura OWL: classes, hierarquia,
object properties, data properties e indivíduos.

Retorna um rdflib.Graph populado e pronto para serialização.
"""

from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import RDF, RDFS, OWL, XSD

from config.settings import ONTOLOGY_IRI, ONTOLOGY_BASE, PROJECT_AUTHOR, PROJECT_DESC
from data.nodes import INDIVIDUALS


# ── Classes ────────────────────────────────────────────────────────────────────
_CLASSES: list[tuple[str, str]] = [
    ("Entidade",          "Classe raiz da ontologia"),
    ("ConceituoIA",       "Conceitos fundamentais de Inteligência Artificial"),
    ("TipoConexao",       "Classificação semântica de uma aresta do grafo"),
    ("Fato",              "Informação verificada e verdadeira"),
    ("Suposicao",         "Conexão plausível, não verificada"),
    ("ErroSemantico",     "Conexão estruturalmente válida, semanticamente incorreta"),
    ("Alucinacao",        "Subconjunto de erro: resposta plausível mas incorreta"),
    ("PropagacaoDeErro",  "Disseminação de alucinações pelo sistema"),
    ("SistemaIA",         "Sistema de Inteligência Artificial"),
    ("ModeloLinguagem",   "LLM — modelo baseado em padrões estatísticos"),
    ("Grafo",             "Estrutura matemática G=(V,E)"),
    ("Ontologia",         "Camada semântica do sistema"),
    ("CamadaSemantica",   "Integração entre grafo e ontologia"),
    ("ConexaoGrafo",      "Aresta do grafo com peso de confiança"),
    ("Vertice",           "Nó do grafo representando conceito ou entidade"),
    ("Aresta",            "Relação entre dois vértices"),
    ("PesoConfianca",     "Valor numérico [0,1] que expressa certeza de uma aresta"),
]

# ── Hierarquia subClassOf ──────────────────────────────────────────────────────
_HIERARCHY: list[tuple[str, str]] = [
    ("ConceituoIA",      "Entidade"),
    ("TipoConexao",      "Entidade"),
    ("Fato",             "TipoConexao"),
    ("Suposicao",        "TipoConexao"),
    ("ErroSemantico",    "TipoConexao"),
    ("Alucinacao",       "ErroSemantico"),
    ("PropagacaoDeErro", "ErroSemantico"),
    ("SistemaIA",        "ConceituoIA"),
    ("ModeloLinguagem",  "SistemaIA"),
    ("Grafo",            "ConceituoIA"),
    ("Ontologia",        "ConceituoIA"),
    ("CamadaSemantica",  "ConceituoIA"),
    ("ConexaoGrafo",     "ConceituoIA"),
    ("Vertice",          "ConexaoGrafo"),
    ("Aresta",           "ConexaoGrafo"),
    ("PesoConfianca",    "ConceituoIA"),
]

# ── Object Properties ─────────────────────────────────────────────────────────
# (nome, domain, range, comentário)
_OBJ_PROPS: list[tuple[str, str, str, str]] = [
    ("temConexao",       "SistemaIA",      "ConexaoGrafo",   "Sistema possui uma conexão no grafo"),
    ("instanciaDE",      "ModeloLinguagem","SistemaIA",       "LLM é instância de SistemaIA"),
    ("operaCom",         "SistemaIA",      "ConceituoIA",    "Sistema opera com um conceito"),
    ("podeGerar",        "SistemaIA",      "TipoConexao",    "Sistema pode gerar um tipo de conexão"),
    ("causaAlucinacao",  "ConceituoIA",    "Alucinacao",     "Causa que origina a alucinação"),
    ("manifestaComo",    "Alucinacao",     "ErroSemantico",  "Alucinação se manifesta como erro"),
    ("levadA",           "Alucinacao",     "PropagacaoDeErro","Alucinação leva à propagação"),
    ("integra",          "Grafo",          "CamadaSemantica","Grafo integra camada semântica"),
    ("fornece",          "Ontologia",      "CamadaSemantica","Ontologia fornece semântica"),
    ("classifica",       "Ontologia",      "TipoConexao",    "Ontologia classifica conexões"),
    ("permite",          "CamadaSemantica","ConceituoIA",    "Camada semântica permite inferências"),
    ("produz",           "CamadaSemantica","SistemaIA",      "Camada semântica produz sistema interpretável"),
    ("reduz",            "TipoConexao",    "ConceituoIA",    "Tipo de conexão reduz alguma propriedade"),
    ("compromete",       "TipoConexao",    "ConceituoIA",    "Tipo de conexão compromete propriedade"),
    ("temPesoConfianca", "Aresta",         "PesoConfianca",  "Aresta possui peso de confiança"),
]

# ── Data Properties ───────────────────────────────────────────────────────────
# (nome, domain, xsd_type, comentário)
_DATA_PROPS: list[tuple[str, str, URIRef, str]] = [
    ("valorConfianca",  "PesoConfianca", XSD.float,   "Valor numérico de confiança [0.0, 1.0]"),
    ("nomeConceito",    "ConceituoIA",   XSD.string,  "Nome do conceito"),
    ("descricao",       "Entidade",      XSD.string,  "Descrição textual da entidade"),
    ("ehVerificado",    "TipoConexao",   XSD.boolean, "Indica se a conexão foi verificada"),
    ("grauAmbiguidade", "ErroSemantico", XSD.float,   "Grau de ambiguidade [0.0, 1.0]"),
]

# ── Relações entre indivíduos ─────────────────────────────────────────────────
_IND_RELATIONS: list[tuple[str, str, str]] = [
    ("GPT4",             "podeGerar",   "AlucinacaoEx1"),
    ("Claude3",          "podeGerar",   "AlucinacaoEx2"),
    ("GrafoConhecimento","integra",     "CamadaIntegrada"),
    ("OntologiaAI",      "fornece",     "CamadaIntegrada"),
    ("OntologiaAI",      "classifica",  "FatoVerificado1"),
    ("OntologiaAI",      "classifica",  "Suposicao1"),
    ("AlucinacaoEx1",    "levadA",      "PropErro1"),
    ("AlucinacaoEx1",    "manifestaComo","AlucinacaoEx1"),
]


def build_ontology() -> Graph:
    """Constrói e retorna o grafo RDF com toda a ontologia OWL."""

    g = Graph()
    BASE = Namespace(ONTOLOGY_BASE)
    g.bind("",    BASE)
    g.bind("owl", OWL)
    g.bind("rdf", RDF)
    g.bind("rdfs", RDFS)
    g.bind("xsd", XSD)

    # Declaração da ontologia
    onto = URIRef(ONTOLOGY_IRI)
    g.add((onto, RDF.type,     OWL.Ontology))
    g.add((onto, RDFS.label,   Literal("Alucinação da Inteligência Artificial", lang="pt")))
    g.add((onto, RDFS.comment, Literal(PROJECT_DESC, lang="pt")))
    g.add((onto, URIRef("http://purl.org/dc/elements/1.1/creator"), Literal(PROJECT_AUTHOR)))

    # Classes
    class_uris: dict[str, URIRef] = {}
    for cname, cdesc in _CLASSES:
        uri = BASE[cname]
        g.add((uri, RDF.type,     OWL.Class))
        g.add((uri, RDFS.label,   Literal(cname, lang="pt")))
        g.add((uri, RDFS.comment, Literal(cdesc, lang="pt")))
        class_uris[cname] = uri

    # Hierarquia
    for child, parent in _HIERARCHY:
        g.add((class_uris[child], RDFS.subClassOf, class_uris[parent]))

    # Object Properties
    for pname, domain, range_, comment in _OBJ_PROPS:
        uri = BASE[pname]
        g.add((uri, RDF.type,     OWL.ObjectProperty))
        g.add((uri, RDFS.label,   Literal(pname, lang="pt")))
        g.add((uri, RDFS.comment, Literal(comment, lang="pt")))
        g.add((uri, RDFS.domain,  class_uris[domain]))
        g.add((uri, RDFS.range,   class_uris[range_]))

    # Data Properties
    for pname, domain, range_, comment in _DATA_PROPS:
        uri = BASE[pname]
        g.add((uri, RDF.type,     OWL.DatatypeProperty))
        g.add((uri, RDFS.label,   Literal(pname, lang="pt")))
        g.add((uri, RDFS.comment, Literal(comment, lang="pt")))
        g.add((uri, RDFS.domain,  class_uris[domain]))
        g.add((uri, RDFS.range,   range_))

    # Indivíduos
    for ind in INDIVIDUALS:
        uri = BASE[ind.name]
        g.add((uri, RDF.type,     class_uris[ind.owl_class]))
        g.add((uri, RDF.type,     OWL.NamedIndividual))
        g.add((uri, RDFS.label,   Literal(ind.name, lang="pt")))
        g.add((uri, RDFS.comment, Literal(ind.descricao, lang="pt")))

    # Relações entre indivíduos
    for subj, prop, obj_ in _IND_RELATIONS:
        g.add((BASE[subj], BASE[prop], BASE[obj_]))

    # Valores de data properties
    g.add((BASE["PesoAlto"],        BASE["valorConfianca"],  Literal(0.95, datatype=XSD.float)))
    g.add((BASE["PesoBaixo"],       BASE["valorConfianca"],  Literal(0.40, datatype=XSD.float)))
    g.add((BASE["AlucinacaoEx1"],   BASE["ehVerificado"],    Literal(False, datatype=XSD.boolean)))
    g.add((BASE["FatoVerificado1"], BASE["ehVerificado"],    Literal(True,  datatype=XSD.boolean)))
    g.add((BASE["AlucinacaoEx1"],   BASE["grauAmbiguidade"], Literal(0.85,  datatype=XSD.float)))

    return g
