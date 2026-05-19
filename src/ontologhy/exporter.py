"""
ontology/exporter.py
Serializa um rdflib.Graph para arquivo OWL/RDF-XML.
Responsabilidade única: I/O de ontologia.
"""

from rdflib import Graph
from rdflib.namespace import OWL, RDF


def save_ontology(g: Graph, output_path: str) -> None:
    """Serializa o grafo RDF como RDF/XML (.owl)."""
    g.serialize(destination=output_path, format="xml")

    n_classes = sum(1 for _ in g.subjects(RDF.type, OWL.Class))
    n_obj     = sum(1 for _ in g.subjects(RDF.type, OWL.ObjectProperty))
    n_data    = sum(1 for _ in g.subjects(RDF.type, OWL.DatatypeProperty))
    n_ind     = sum(1 for _ in g.subjects(RDF.type, OWL.NamedIndividual))
    n_triples = len(g)

    print(
        f"[OWL]  {output_path}\n"
        f"       Classes: {n_classes}  |  ObjectProp: {n_obj}  "
        f"|  DataProp: {n_data}  |  Indivíduos: {n_ind}  |  Triplas: {n_triples}"
    )
