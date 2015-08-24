import argparse
import sys

from googleapiclient.errors import HttpError

import utils

from google_search import Google

__author__ = 'chetannaik'


def main(args):
    google = Google(args.api_key, args.cse_id)

    queries = ["\"contour plowing is the *\""]
    if args.query:
        queries = [args.query]

    for q in queries:
        print "Searching \"%s\"" % (q)
        all_sentences = []
        for start in xrange(1, 70, 10):
            print "Searching page", start
            try:
                result = google.search(q, start=start)
                sentences = utils.get_sentences(result)
                all_sentences.extend(sentences)
            except HttpError as e:
                print "ERROR: {}".format(e)
                break
                # sys.exit()
        if args.keyword:
            keyword = [args.keyword]
        else:
            keyword = None
        filtered_sentences = utils.filter_sentences(list(set(all_sentences)), keyword)
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
    parser.add_argument('--keyword', help='Optional filter keyword.')

    args = parser.parse_args()
    main(args)
