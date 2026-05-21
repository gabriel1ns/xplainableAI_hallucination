# xplainableAI_hallucination

Representação computacional do fenômeno de alucinação em modelos de linguagem (LLMs), usando grafos ponderados e ontologias OWL para distinguir Fato, Suposição e Erro Semântico.

## Como funciona

O projeto modela o domínio como um grafo dirigido G=(V,E) onde cada vértice é um conceito (LLM, Alucinação, Ontologia…) e cada aresta é uma relação semântica com um peso de confiança entre 0 e 1. A ideia central é que a alucinação aparece como uma conexão estruturalmente válida no grafo, mas semanticamente incorreta — e só é detectável quando se adiciona a camada ontológica.

A ontologia OWL DL classifica cada conexão em classes mutuamente exclusivas (`Fato`, `Suposicao`, `ErroSemantico`) e define restrições formais como "toda `Alucinacao` deve manifestar-se como algum `ErroSemantico`" e "todo `ModeloLinguagem` pode gerar `Alucinacao`". Isso torna o modelo interpretável por reasoners como HermiT no Protégé.

## Instalação

```bash
pip install -r requirements.txt
```

## Como rodar

```bash
python main.py
```

## Saídas

Geradas em `output/`:

| Arquivo | Descrição |
|---------|-----------|
| `grafo_alucinacao_ia.html` | Grafo interativo — abra no navegador |
| `alucinacao_ia_ontologia.owl` | Ontologia OWL DL — abra no Protégé |
| `sumario.json` | Estatísticas e dados completos do grafo |

## Estrutura

```
├── main.py                      # orquestrador
├── requirements.txt
└── src/
    ├── config/settings.py       # constantes, paleta visual, opções do grafo
    ├── data/
    │   ├── nodes.py             # vértices e indivíduos da ontologia
    │   └── edges.py             # arestas com relação, tipo e peso
    ├── graph/
    │   ├── builder.py           # monta a rede PyVis em memória
    │   └── visualizer.py        # salva o HTML com legenda e título
    ├── ontology/
    │   ├── schema.py            # classes, propriedades e restrições OWL
    │   └── exporter.py          # serializa para RDF/XML
    └── reports/
        └── json_exporter.py     # gera o sumário em JSON
```

## Autor

Gabriel Lins Alves do Nascimento POLI/UPE
Teoria dos Grafos