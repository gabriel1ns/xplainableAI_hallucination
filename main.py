"""
main.py
Orquestrador do projeto — chama cada módulo em sequência.
Não contém lógica de negócio: só coordena.
"""

import os
import sys


_ROOT = os.path.dirname(os.path.abspath(__file__))
_SRC  = os.path.join(_ROOT, "src")
if _SRC not in sys.path:
    sys.path.insert(0, _SRC)

import importlib, types

def _alias_ontologhy():
    """Cria o alias 'ontology' apontando para 'ontologhy' se necessário."""
    try:
        import ontology  # já existe com nome certo? ok
    except ModuleNotFoundError:
        try:
            import ontology as _mod
            sys.modules["ontology"] = _mod
            # aliases para os submódulos também
            import ontology.schema   as _schema
            import ontology.exporter as _exporter
            sys.modules["ontology.schema"]   = _schema
            sys.modules["ontology.exporter"] = _exporter
            print("[aviso] pasta 'ontologhy' detectada — alias 'ontology' criado automaticamente.")
            print("        Renomeie a pasta para 'ontology' para remover este aviso.\n")
        except ModuleNotFoundError:
            pass 

_alias_ontologhy()

from config.settings import (
    OUTPUT_DIR,
    GRAPH_HTML_FILE,
    ONTOLOGY_OWL_FILE,
    SUMMARY_JSON_FILE,
)
from data.nodes import NODES
from data.edges import EDGES
from graph.builder         import build_network
from graph.visualizer      import save_graph
from ontology.schema       import build_ontology
from ontology.exporter     import save_ontology
from reports.json_exporter import save_summary


def main() -> None:
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    net = build_network(NODES, EDGES)
    save_graph(net, os.path.join(OUTPUT_DIR, GRAPH_HTML_FILE))

    owl_graph = build_ontology()
    save_ontology(owl_graph, os.path.join(OUTPUT_DIR, ONTOLOGY_OWL_FILE))

    save_summary(NODES, EDGES, os.path.join(OUTPUT_DIR, SUMMARY_JSON_FILE))

    print("\nPipeline completo. Arquivos em ./" + OUTPUT_DIR + "/")


if __name__ == "__main__":
    main()