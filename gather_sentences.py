import argparse
import itertools
from collections import defaultdict

import pandas as pd
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
    filtered_sentences = utils.filter_sentences(list(set(all_sentences)),
                                                keywords)
    return all_sentences, filtered_sentences


def main(args):
    pattern_df = pd.read_csv(args.pattern_tsv, sep="\t")
    procecss_df = pd.read_csv(args.process_tsv, sep="\t")

    patterns = pattern_df.PATTERN.tolist()
    processes = procecss_df.PROCESS.tolist()

    stop_words = set(stopwords.words('english'))
    google = Google(args.api_key, args.cse_id)

    all_data = defaultdict(lambda: defaultdict(tuple))
    for item in itertools.product(processes, patterns):
        process, pattern = item
        query = pattern.replace('<process name>', process)
        keywords = filter(lambda x: x not in stop_words,
                          map(lambda x: x.strip(),
                              filter(bool, query.split("*"))))
        all_sentences, filtered_sentences = search(google, query, keywords)
        all_data[process][pattern] = (query, all_sentences, filtered_sentences)

    filtered_list = []
    all_list = []
    for process, p_data in all_data.iteritems():
        for pattern, data in p_data.iteritems():
            query, all_sentences, filtered_sentences = data
            if len(filtered_sentences) >= 1:
                for sentence in filtered_sentences:
                    filtered_list.append([process, pattern, query, sentence])
            if len(all_sentences) >= 1:
                for sentence in all_sentences:
                    all_list.append([process, pattern, query, sentence])

    filtered_df = pd.DataFrame(filtered_list)
    all_df = pd.DataFrame(all_list)
    filtered_df.columns = ['PROCESS', 'PATTERN', 'QUERY', 'FILTERED_SENTENCE']
    all_df.columns = ['PROCESS', 'PATTERN', 'QUERY', 'SENTENCE']
    filtered_df.to_csv("output/filtered_sentences.tsv", sep="\t", index=False)
    all_df.to_csv("output/all_sentences.tsv", sep="\t", index=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Google Search to acquire'
                                                 'sentences on processes.')
    parser.add_argument('--api_key', help='Google Developer API Key')
    parser.add_argument('--cse_id', help='Google Custom Search Engine ID')
    parser.add_argument('--pattern_tsv', help='tsv file containing patterns.')
    parser.add_argument('--process_tsv', help='tsv file containing processes.')

    args = parser.parse_args()
    main(args)
