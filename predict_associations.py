import networkx as nx
import spacy
from itertools import groupby
from parse_articles import *
from math import log

def predict_associations(article_tags, graph):
    similar = []
    for tag, label in article_tags:
        if tag in graph.nodes:
            total = sum([v for _,v in graph.nodes[tag]['tags'].items()])
            neighbors = {n:(v['weight']/total) * 1/(1+log(1.5*len(graph[n]))) for n, v in graph[tag].items()}
            similar.append(neighbors)

    grouped = groupby(sorted(sum(list(map(lambda d: list(d.items()), similar)),[]), key=lambda x: x[0]), key=lambda x: x[0])
    means = list(map(lambda x: (x[0], sum(list(map(lambda l: l[1], x[1])))/len(article_tags)), grouped))

    return dict(means)

def suggest_associated(text, tagged_corpus, graph, model):
    article_tags = get_tags([text], model)[0]
    associations = predict_associations(article_tags, graph)
    scores = [sum([associations[tag] for tag, label in tags if tag in associations]) for _, tags in tagged_corpus]
    scored_corpus = [(score, text) for score, (text,_) in zip(scores, tagged_corpus)]
    return sorted(scored_corpus, key=lambda t: t[0])[-10:]
