import click
from random import shuffle
from parse_articles import *
from predict_associations import *
import spacy
import json
import dill as pickle

@click.group()
def cli():
    pass

@cli.command()
@click.argument('articles_path',nargs=1, type=click.Path(exists=True))
@click.argument('output',nargs=1)
def init(articles_path, output):

    nlp = spacy.load('company-model')

    with open(articles_path,'r') as f:
        articles = json.load(f)
        articles = list(set(list(map(lambda x: x['text'], articles))))
        tags = get_tags(articles, nlp)
        graph = make_graph(tags)

    with open(output,'wb') as f:
        pickle.dump({'articles':articles,'tags':tags,'graph':graph}, f)
        print("Wrote data file to " + output)

@cli.command()
@click.argument('data_file_path', type=click.Path(exists=True))
@click.argument('article_path', type=click.Path(exists=True))
def tag(data_file_path, article_path):
    
    with open(data_file_path,'rb') as f:
        data = pickle.load(f)
        #nlp = spacy.blank('en').from_bytes(data['model'])
        nlp = spacy.load('company-model')

    with open(article_path,'r') as f:
        text = f.read().replace('\n',' ')

    tags = get_tags([text], nlp)
    for t in tags:
        print(t)

@cli.command()
@click.argument('data_file_path', type=click.Path(exists=True))
@click.argument('article_path', type=click.Path(exists=True))
def suggest(data_file_path, article_path):

    with open(data_file_path,'rb') as f:
        data = pickle.load(f)
        tagged_corpus = list(zip(data['articles'], data['tags']))
        graph = data['graph']
        #model = data['model']
        model = spacy.load('company-model')

    with open(article_path, 'r') as f:
        text = f.read().replace('\n',' ')

    suggestions = suggest_associated(text,tagged_corpus,graph,model)
    for s in suggestions:
        print(s)

@cli.command()
@click.argument('data_file_path', type=click.Path(exists=True))
@click.argument('article_path', type=click.Path(exists=True))
def related_entities(data_file_path, article_path):

    with open(data_file_path,'rb') as f:
        data = pickle.load(f)
        graph = data['graph']
        #nlp = data['model']
        nlp = spacy.load('company-model')

    with open(article_path,'r') as f:
        text = f.read().replace('\n',' ')

    associations = predict_associations(get_tags([text], nlp)[0], graph)
    for a, v in sorted(associations.items(), key=lambda x:x[1], reverse=True):
        print(a)

@cli.command()
@click.argument('articles_path', type=click.Path(exists=True))
@click.argument('output_path')
def random(articles_path, output_path):

    with open(articles_path,'r') as f:
        articles = json.load(f)
        articles = list(set(list(map(lambda l: l['text'], articles))))
        shuffle(articles)
        article = articles[0]

    with open(output_path,'w') as f:
        f.write(article)

    print("Random article has been placed at " + output_path)

if __name__ == '__main__':
    cli()
