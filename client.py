import argparse
import sys

from googleapiclient.errors import HttpError
from nltk.corpus import stopwords

import utils

from google_search import Google

__author__ = 'chetannaik'


def search(google, query, keywords):
    print "\nSearching \"%s\"" % (query)    
    all_sentences = []
    for start in xrange(1, 31, 10):
        print (start / 10) + 1,
        try:
            result = google.search(query, start=start)
            sentences = utils.get_sentences(result)
            all_sentences.extend(sentences)
        except HttpError as e:
            print "\nERROR: {}\n".format(e)
            break
            # sys.exit()
    print "\nFiltering sentences using", keywords
    filtered_sentences = utils.filter_sentences(list(set(all_sentences)),
                                                keywords)
    return all_sentences, filtered_sentences


def main(args):
    stop_words = set(stopwords.words('english'))
    google = Google(args.api_key, args.cse_id)
    query = args.query
    keywords = filter(lambda x: x not in stop_words, map(lambda x: x.strip(), filter(bool, query.split("*"))))
    all_sentences, filtered_sentences = search(google, query, keywords)

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
    parser.add_argument('--query', help='Optional query paramater.')

    args = parser.parse_args()
    main(args)
