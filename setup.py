from setuptools import setup

setup(
    name='reggie',
    version='1.0',
    py_modules=['parse_articles', 'reggie', 'predict_associations'],
    install_requires=[
        'click',
        'spacy',
        'networkx',
        'dill'
    ],
    entry_points='''
        [console_scripts]
        reggie=reggie:cli
    ''',
)
