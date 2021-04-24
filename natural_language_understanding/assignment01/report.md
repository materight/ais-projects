# Natural Language Understanding - Report Assignment 1 
Student: **Destro Matteo (221222)**

## Exercise 1
**Extract a path of dependency relations from the ROOT to a token.** \
Implemented in function `get_paths(sentence)`:
- **Input:** a sentence (string).
- **Output:** a list of lists. Each list at index `i` represents the path from the `ROOT` to token `i` (i.e. the token in position i in the parsed sentence). Each item of these lists is a dependency relation between two tokens.

It parses a sentence and extracts dependency relations from the `ROOT` to each one of the tokens by exploiting the `ancestors` property of the `Token` object. For each ancestor, it extracts its dependency relation type. The resulting list is then reversed to start from the `ROOT`. Therefore first element of the path to a token will always be `ROOT`, while the last element will be the dependency relation that connects that specific token.

## Exercise 2
**Extract subtree of a dependents given a token.** \
Implemented in function `get_subtrees(sentence)`:
- **Input:** a sentence (string).
- **Output:** a list of lists. Each list at index `i` contains the subtree of token `i` in the sentence.

It parses a sentence in input and extracts the subtrees of each token by using the `subtree` property of the `Token` object. Each token in the subtree is converted to a string.

## Exercise 3
**Check if a given list of tokens (segment of a sentence) forms a subtree.** \
Implemented in function `is_subtree(sentence, subtree)`:
- **Input:** a sentence (string) and a subtree (*ordered* list of strings, where each string is a token).
- **Output:** True/False.

It parses a sentence and search for a correspondence between the given `subtree` list and the subtrees of each token in the sentence. By doing this, the function is able to detect if the input `subtree` is a valid subtree present in the parsed sentence. 

## Exercise 4
**Identify head of a span, given its tokens.** \
Implemented in function `get_head(span)`:
- **Input:** a span (string). It assumes that the input is a single span.
- **Output:** a `Token` object representing the head of the span.

It parses a span and extracts its head by exploiting the `root` property of the `Span` object. The `Span` object is obtained from the `sents` property of the parsed document, that contains all the spans parsed. Since we assume that the input contains a single sentence, it is safe to simply return the root of the first span.

## Exercise 5
**Extract sentence subject, direct object and indirect object spans.** \
Implemented in function `extract_deps(span)`:
- **Input:** a sentence (string).
- **Output:** a dict of lists. The dict will have 3 keys (`"nsubj"`, `"dobj"`, `"iobj"`), with one list each. The items of the lists are the extracted corresponding spans (strings).

It parses a sentence and extracts all the subject (`nsubj`), direct object (`dobj`) and indirect object (`dative`) spans using the `dep_` property of `Token`. It searches for all the tokens that have a dependency relation of either `nsubj`, `dobj` or `dative` and it extracts their subtrees. Each extracted subtree is then concatenated into a span and added to the corresponding result list inside the dictionary. Please note that indirect object relations are represented by the `dative` keyword, since the `iobj` keyword has ben deprecated in the latest versions of spaCy.