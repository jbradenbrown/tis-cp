github.com/jbradenbrown/tis-cp

The easiest way to use my project is through the cli that I've built. This is accessible by creating a virtual environment (not required, but recommended), and installing with pip while in the directory containing setup.py:
    pip install -e .

To save time, I've included a prebuilt data file. If you want to build your own, either use the provided articles.json file, or create a new articles file that is a list of objects with a text attribute in json format and run:
    reggie init <articles_path> <data_file_path>

tag, suggest, and related_entities all output to stdout, to make things more readable use less or pipe the output to a file. All formatting has been removed from the articles, so they are not the prettiest.

To get a random article from a json articles list, run:
    reggie random <articles_path> <output_path>

This has already been done, and an article has been placed at example.txt

To see the tags which are generated for an example, run:
    reggie tag <data_file_path> <article_path>

To see a list of 10 suggested *related* articles, run:
    reggie suggest <data_file_path> <article_path>

To see which entities reggie is associating with an article, run:
    reggie related_entities <data_file_path> <article_path>
