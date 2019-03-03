#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import argparse
import pytz
from jira import JIRA
from collections import Counter
from datetime import datetime
from wordcloud import WordCloud
from janome.tokenizer import Tokenizer
from pprint import pprint

# path to mac font
font_path = "/System/Library/Fonts/ヒラギノ明朝 ProN.ttc"

def valid_date(s):
    try:
        return datetime.strptime(s, '%Y-%m-%d')
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(s)
        raise argparse.ArgumentTypeError(msg)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='WordCloud of ical')
    parser.add_argument('-j', '--jira-url',
        help='JIRA url',
        default=os.environ.get('JIRA_URL', None),
        type=str)
    parser.add_argument('-ju', '--jira-user',
        help='JIRA user',
        default=os.environ.get('JIRA_USER', None),
        type=str)
    parser.add_argument('-jp', '--jira-passwd',
        help='JIRA password',
        default=os.environ.get('JIRA_PASSWORD', None),
        type=str)
    parser.add_argument('-jql', '--jira-ql',
        help='JIRA QL to filter tickets',
        default=os.environ.get('JIRA_QL', None),
        type=str)
    parser.add_argument('-f', '--frm',
        help='Parse tickets from this date. Please specify in %%Y-%%m-%%d format.',
        type=valid_date, required=True)
    parser.add_argument('-t', '--to',
        help='Parse tickets until this date. Please specify in %%Y-%%m-%%d format.',
        type=valid_date, required=True)
    parser.add_argument('-tz', '--timezone',
        help='Timezone to find jira tickets',
        default='UTC',
        type=str)
    parser.add_argument('-wd', '--width',
        help='Width of wordcloud image',
        default=1000,
        type=int)
    parser.add_argument('-ht', '--height',
        help='Height of wordcloud image',
        default=680,
        type=int)
    parser.add_argument('-o', '--output-path',
        help='wordcloud output file path',
        default=os.path.expanduser('~/Desktop/jira2wordcloud.png'),
        type=str)

    args = parser.parse_args()

    jc = JIRA(server=args.jira_url, auth=(args.jira_user, args.jira_passwd))

    tz = pytz.timezone(args.timezone)
    from_dt = tz.localize(args.frm)
    to_dt = tz.localize(args.to)

    tkr = Tokenizer()
    words = []

    tickets = jc.search_issues(
        '{} AND updatedDate >= "{}" AND updatedDate <= "{}"'
        .format(args.jira_ql, from_dt.strftime('%Y/%m/%d'), to_dt.strftime('%Y/%m/%d')),
        maxResults=250)
    for ticket in tickets:
        title = ticket.fields.summary
        for tkn in tkr.tokenize(title):
            ps = tkn.part_of_speech
            #print(tkn.surface, tkn.part_of_speech)
            if ps.startswith('名詞') or ps.startswith('動詞'):
                # remove noise
                if all([ ng not in ps for ng in ['接尾', '非自立', '自立']]):
                    words.append(tkn.surface)

    wordcloud = WordCloud(
        background_color="white",
        font_path=font_path,
        width=args.width,
        height=args.height).generate(' '.join(words))

    path_split = os.path.splitext(args.output_path)
    suffix = "_{}_{}{}".format(
        from_dt.strftime('%Y-%m-%d'),
        to_dt.strftime('%Y-%m-%d'),
        path_split[1])
    output_path = path_split[0] + suffix
    wordcloud.to_file(output_path)
