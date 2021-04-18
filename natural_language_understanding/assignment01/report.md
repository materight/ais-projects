# Natural Language Understanding - Report Assignment 1 
Student: **Destro Matteo (221222)**

## Exercise 1
**Extract a path of dependency relations from the ROOT to a token.** \
Implemented in function `get_paths(sentence)`, it parses a sentence and extracts dependency relations from the `ROOT` to each one of the tokens by exploiting the `ancestors` property of the `Token` object. For each ancestor, it extracts its dependency relation type. The resulting list is then reversed to start from the `ROOT`. Therefore first element of the path to a token will always be `ROOT`, while the last element will be the dependency relation that connects that specific token.
- **Input:** a sentence (string).
- **Output:** a list of lists. Each list at index `i` represents the path from the `ROOT` to token `i` (i.e. the token in position i in the parsed sentence). Each item of these lists is a dependency relation between two tokens.

## Exercise 2
**Extract subtree of a dependents given a token.** \
Implemented in function `get_subtrees(sentence)`, it parses a sentence and extracts the subtrees of each token by using the `subtree` property of the Token object.
- **Input:** a sentence (string).
- **Output:** a list of lists. Each list at index `i` contains the subtree of token `i` in the sentence.

## Exercise 3
**Check if a given list of tokens (segment of a sentence) forms a subtree.** \
Implemented in function `is_subtree(sentence, subtree)`, it parses a sentence and checks a correspondence between the given `subtree` list and the subtrees of each token in the sentence. By doing this, it is able to check for a correspondence between all the possible subtrees of the tokens in `sentence` and the `subtree` variable in input.
- **Input:** a sentence (string) and a subtree (*ordered* list of strings, where each string is a token).
- **Output:** True/False.

## Exercise 4
**Identify head of a span, given its tokens.** \
Implemented in function `get_head(span)`, it parses a span and extracts its head by exploiting the `root` property of the Span object.
- **Input:** a span (string). It assumes that the input is a single span.
- **Output:** a Token object representing the head of the span.

## Exercise 5
**Extract sentence subject, direct object and indirect object spans.** \
Implemented in function `extract_deps(span)`, it parses a sentence and extracts all the subject (`nsubj`), direct object (`dobj`) and indirect object (`iobj`) spans using the `dep_` property of `Token`. It searches for all the tokens that have a dependency relation of either `nsubj`, `dobj` or `iobj` and it extracts their subtrees. Each extracted subtree is then concatenated into a span and added to the corresponding result list inside the dictionary.
- **Input:** a sentence (string).
- **Output:** a dict of lists. The dict will have 3 keys (`"nsubj"`, `"dobj"`, `"iobj"`), with one list each. The items of the lists are the extracted corresponding spans (strings).