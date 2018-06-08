# term_eval #

term_eval is a tool for evaluating bilingual term alignment or translation systems.

term_eval was used for experiments published in the following paper:

J. Liu, E. Morin, and S. Peña Saldarriaga,  Towards a unified framework for bilingual terminology extraction of single-word and multi-word terms. Proceedings of COLING 2018.

**Please cite this paper** if you use term_eval or the wind energy reference list.

term_eval uses a JSON representation of gold standard reference lists, and a tabular format for evaluated results. As long as you can provide data in the expected format, you can use term_eval for similar tasks and different language pairs.

### Installation ###

term_eval is a standalone tool that requires python3 to be executed.

### How do I use term_eval? ###

In a CLI type the following command in the term_eval directory:

```console
me@localhost:~$ term_eval.py data/en-it.test-artetxe2016.json samples/en-it.results-liuetal2018.tsv
```
This will reproduce our results presented in our paper for the english italian single general word task


### Wind energy corpus ###

* Wind energy corpus can be found here : http://www.lina.univ-nantes.fr/?Reference-Term-Lists-of-TTC.html
* Corresponding reference list can be found in the ```data``` directory
* Sample evaluation file can be found in the ```samples``` directory

Note that we only put a sample file (we only put top 10 candidates and the source terms are not complete) to show how the result looks like, how the system aligns MWT of variable length, it is not meant to have the same result in our paper. 

## Contact information

````shell
Jingshu Liu
jingshu[at]dictanova.com
````
