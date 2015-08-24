import argparse
import sys

from googleapiclient.errors import HttpError
from nltk.tokenize import word_tokenize, sent_tokenize

import utils

from google_search import Google

__author__ = 'chetannaik'


def get_sentences(result):
    sentences = []
    for item in result[u'items']:
        snippet = item[u'snippet'].replace('\n', '').encode('ascii', 'ignore')
        sentences.extend(sent_tokenize(snippet))
    return list(set(sentences))


def filter_sentences(sentences):
    filtered_sentences = []
    for sentence in sentences:
        tokens = word_tokenize(sentence)
        if utils.is_valid_sentence(sentence, tokens):
            filtered_sentences.append(sentence)
    return filtered_sentences


def main(args):
    google = Google(args.api_key, args.cse_id)

    queries = ["\"contour plowing *\""]

    for q in queries:
        print "Searching \"%s\"" % (q)
        all_sentences = []
        for start in xrange(1, 70, 10):
            print "Searching page", start
            try:
                result = google.search(q, start=start)
                sentences = get_sentences(result)
                all_sentences.extend(sentences)
            except HttpError as e:
                print "ERROR: {}".format(e)
                break
                # sys.exit()
        filtered_sentences = filter_sentences(list(set(all_sentences)))
        print "\nRAW SENTENCES:"
        for x in all_sentences:
            print "- ", x
        print "\nFILTERED SENTENCES:"
        for x in filtered_sentences:
            print "- ", x
        print "\n"
        print "Found", len(filtered_sentences), "sentences"


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Google Search to acquire'
                                                 'sentences on processes.')
    parser.add_argument('--api_key', help='Google Developer API Key')
    parser.add_argument('--cse_id', help='Google Custom Search Engine ID')
    parser.add_argument('--input_file', help='Input file with list of search'
                                             'queries')
    parser.add_argument('--output_file', help='Out file with results.')

    args = parser.parse_args()
    main(args)
