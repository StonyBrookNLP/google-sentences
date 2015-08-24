__author__ = 'chetannaik'


def is_valid_sentence(sentence, tokens):
    # Sentence has just one full-stop.
    if sentence.count('.') != 1:
        return False

    # Sentence doesn't have the following symbols.
    if any(symbol in sentence for symbol in ['?', '_', '<']):
        return False

    # Sentence length lies in the following range.
    if len(sentence) < 20:
        return False

    # Sentence does not have ALL CAPS tokens of length 2 or greater.
    if sum(map(lambda x: len(x) >= 2 and x.isupper(), tokens)):
        return False

    # Sentence does not have 2 or more tokens which end with "tion".
    if sentence.endswith("..."):
        return False

    # Sentence does not start with capital letter character.
    if not sentence[0].isupper():
        return False

    return True