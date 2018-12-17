from parse_articles import *
from predict_associations import *
import json
from random import shuffle
import spacy

nlp = spacy.load('company-model')

articles = json.load(open("articles.json","r"))
articles = list(set(list(map(lambda a: a['text'], articles))))
shuffle(articles)
test_corpus = articles[:100]
tags = get_tags(test_corpus, nlp)
tagged_corpus = list(zip(test_corpus, tags))
graph = make_graph(tags)
associations = predict_associations(get_tags([articles[501]],nlp)[0], graph)
maybe_associated = suggest_associated(articles[501], tagged_corpus, graph, nlp)
