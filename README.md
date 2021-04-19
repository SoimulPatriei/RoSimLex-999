## The RoSimLex-999 data and code
This is the data and the code for the paper "Evaluating computational models of similarity against a human-rated dataset." \
The code has been tested on **Mac OS X** and **Linux**.

### Prerequisites
1. **Python** 3.6.10 or higher. We recommend installing the [Anaconda](https://www.anaconda.com/products/individual) distribution. 
In any case, you have to have NumPy and SciPy installed.
2. If you want to reproduce the corpus-based results you need to install more things (see below).

### Data
1. If you prefer the data in spreadsheet format, you can download it from here: [RoSimlex-999 Data](https://docs.google.com/spreadsheets/d/1QFNIVBmoLonLhr0mRO_jeTciIExD0X4Wa06XWAX5T5U/edit?usp=sharing)
2. You can find the data in text format under the "Data" directory. 
  - *RoSimlex-Maximal.txt*  contains the original Simlex-999 set, the Romanian mappings, 
the human scores, and the scores computed from corpora embeddings and the semantic networks.
  - *RoSimlex-Common.txt*  is the common set described in the paper

### Compute the correlation coefficients

After running the following script, the results are in the "results_corr.txt" file.
  - python correlations.py --scores Data/RoSimLex-Final.txt --results results_corr.txt

### Reproduce the similarity scores for the Semantic Networks
1. For Princeton Wordnet, you have to install [NLTK](https://www.nltk.org/)
2. For the Romanian Wordnet, you have to install [RoWordNet](https://github.com/dumitrescustefan/RoWordNet)
3. Run the script "wordnet_correlations.py." The results are already stored under "Results/Wordnet_Similarities" for your convenience.
  - python wordnet_correlations.py
  
### Reproduce the similarity scores for Corpora
1. Install the [Gensim library](https://radimrehurek.com/gensim/) 
2. Download the following word embeddings:
   - The CoRoLa embeddings with configurations (300_20 and 400_5) from [here](http://89.38.230.23/word_embeddings/index.php)
   - The Romanian CoNLL_2017 embbedings from [here](http://vectors.nlpl.eu/repository/), position 64.
   - The FastText Romanian embeddings from [here](https://fasttext.cc/docs/en/crawl-vectors.html)
   - Place all the models in a directory called "Embeddings" with the following subdirectories
      - CONLL2017_Word2vec. Inside this directory, place "model.bin" representing the Romanian CoNLL_2017 embeddings
      - Corola. Inside this directory place  "corola.300.20.vec" and "corola.400.5.vec" representing the CoRoLa embeddings with configurations (300_20 and 400_5)
      - Facebook. Inside this directory, place "cc.ro.300.bin" representing the FastText Romanian embeddings
   - Run the script "corpus-cosine_embeddings.py." The results are already stored under "Results/Corpus_Similarities" for your convenience.
      - python corpus-cosine_embeddings.py

### Contact
   1. If you have questions or comments regarding the code, write to **Eduard Barbu** (eduard dot barbu at yahoo dot com)
   2. If you have questions or comments regarding the data, write to **Verginica Barbu Mititlelu** (vergi at racai dot ro)
