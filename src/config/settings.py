"""
config/settings.py
Constantes globais do projeto.
"""

PROJECT_TITLE  = "Alucinação da Inteligência Artificial"
PROJECT_AUTHOR = "Gabriel Lins Alves do Nascimento"
PROJECT_DESC   = (
    "Representação estrutural e semântica do fenômeno de alucinação "
    "em Modelos de Linguagem, via grafos e ontologias."
)
OUTPUT_DIR        = "output"
GRAPH_HTML_FILE   = "grafo_alucinacao_ia.html"
ONTOLOGY_OWL_FILE = "alucinacao_ia_ontologia.owl"
SUMMARY_JSON_FILE = "sumario.json"


ONTOLOGY_IRI  = "http://www.semanticweb.org/gabriel/ontologies/alucinacao_ia"
ONTOLOGY_BASE = ONTOLOGY_IRI + "#"

GRAPH_HEIGHT = "750px"
GRAPH_WIDTH  = "100%"
GRAPH_BG     = "#0d1117"
GRAPH_FONT   = "#e6edf3"

NODE_STYLES: dict[str, dict] = {
    "Fato":      {"color": "#2ecc71", "shape": "ellipse",  "size": 28},
    "Suposição": {"color": "#f39c12", "shape": "diamond",  "size": 26},
    "Erro":      {"color": "#e74c3c", "shape": "triangle", "size": 30},
    "Conceito":  {"color": "#3498db", "shape": "dot",      "size": 24},
}

EDGE_STYLES: dict[str, dict] = {
    "Fato":      {"color": "#2ecc71", "dashes": False},
    "Suposição": {"color": "#f39c12", "dashes": True},
    "Erro":      {"color": "#e74c3c", "dashes": True},
}


PHYSICS_OPTIONS = """
{
  "nodes": {
    "borderWidth": 2,
    "borderWidthSelected": 4,
    "shadow": { "enabled": true, "size": 10, "x": 3, "y": 3 }
  },
  "edges": {
    "arrows": { "to": { "enabled": true, "scaleFactor": 0.8 } },
    "smooth": { "type": "dynamic" },
    "shadow": { "enabled": true }
  },
  "physics": {
    "forceAtlas2Based": {
      "gravitationalConstant": -80,
      "centralGravity": 0.01,
      "springLength": 180,
      "springConstant": 0.06
    },
    "solver": "forceAtlas2Based",
    "stabilization": { "iterations": 200 }
  },
  "interaction": {
    "hover": true,
    "tooltipDelay": 100,
    "navigationButtons": true,
    "keyboard": true
  }
}
"""
