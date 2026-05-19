"""
graph/visualizer.py
Salva o Network em HTML e injeta título + legenda visual.
Responsabilidade única: renderização e escrita de arquivo.
"""

from pyvis.network import Network

from config.settings import PROJECT_TITLE


_LEGEND_HTML = """
<div style="position:fixed;bottom:20px;left:20px;background:#161b22;
            border:1px solid #30363d;border-radius:8px;padding:14px 18px;
            color:#e6edf3;font-family:monospace;font-size:13px;
            z-index:9999;line-height:2">
  <b style="font-size:15px">Legenda</b><br>
  <span style="color:#3498db">●</span> Conceito &nbsp;
  <span style="color:#2ecc71">●</span> Fato &nbsp;
  <span style="color:#f39c12">◆</span> Suposição &nbsp;
  <span style="color:#e74c3c">▲</span> Erro<br>
  <span style="border-bottom:2px solid #2ecc71;display:inline-block;width:30px"></span> Fato &nbsp;
  <span style="border-bottom:2px dashed #f39c12;display:inline-block;width:30px"></span> Suposição /
  <span style="color:#e74c3c">- -</span> Erro<br>
  <small>Espessura = confiança da aresta</small>
</div>
"""


def _title_bar(n_nodes: int, n_edges: int) -> str:
    return f"""
<div style="position:fixed;top:0;left:0;right:0;
            background:linear-gradient(90deg,#0d1117,#161b22);
            border-bottom:1px solid #30363d;padding:12px 24px;z-index:9999;
            font-family:monospace;color:#58a6ff;font-size:16px;
            font-weight:bold;letter-spacing:1px;">
  🧠 {PROJECT_TITLE} — Grafo de Conhecimento &nbsp;
  <span style="font-size:11px;color:#8b949e;font-weight:normal">
    Vértices: {n_nodes} &nbsp;|&nbsp; Arestas: {n_edges}
    &nbsp;|&nbsp; Hover para detalhes
  </span>
</div>
"""


def save_graph(net: Network, output_path: str) -> None:
    """Salva o grafo como HTML interativo com título e legenda."""

    n_nodes = len(net.nodes)
    n_edges = len(net.edges)

    net.save_graph(output_path)

    with open(output_path, "r", encoding="utf-8") as fh:
        html = fh.read()

    injection = _title_bar(n_nodes, n_edges) + _LEGEND_HTML
    html = html.replace("<body>", "<body>" + injection, 1)

    with open(output_path, "w", encoding="utf-8") as fh:
        fh.write(html)

    print(f"[PyVis] {output_path}  ({n_nodes} vértices, {n_edges} arestas)")
