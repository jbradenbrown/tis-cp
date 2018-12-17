import spacy
import networkx as nx
from tqdm import tqdm
from itertools import combinations

def get_tags(corpus, model):
    nlp = model
    entities = lambda a: list(set([(ent.text,ent.label_) for ent in nlp(a).ents if ent.label_ in ["COMPANY","FIGURE","COUNTRY"]]))
    tags = [entities(article) for article in tqdm(corpus)]
    return tags

def make_graph(tags):
    graph = nx.Graph()
    all_entities = sum(tags, [])
    
    for entity, label in all_entities:
        if entity not in graph.nodes:
            graph.add_node(entity, tags={"COMPANY":0,"FIGURE":0,"COUNTRY":0})
        graph.nodes[entity]["tags"][label] = graph.nodes[entity]["tags"][label] + 1

    for tag_list in tags:
        edges = combinations(map(lambda t: t[0], tag_list), 2)
        for edge in edges:
            if not graph.has_edge(*edge):
                graph.add_edge(*edge, weight=0)
            graph.edges[edge]["weight"] = graph.edges[edge]["weight"] + 1

    return graph
