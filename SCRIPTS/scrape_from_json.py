import json
import sys
import pandas as pd 

import matplotlib.pyplot as plt
import seaborn as sns

def filter_post(filename):
    '''
    Extracts post data from json file, keeping desired columns
    '''
    raw_json = pd.read_json(path_or_buf=filename+".jsonl", lines=True, encoding="utf-8-sig")
    selected_data = ['selftext', 'created_utc', 'ups', 'subreddit', 'link_flair_text','title']
        #selftext       - main body text
        #created_utc    - post creation time
        #ups            - number of upvotes
        #subreddit      - subreddit
        #link_flair_text - flair info
        #tile           - post title
    clean_json = raw_json[selected_data]
    clean_json = clean_json.rename(columns = {'link_flair:text': 'flair'})
    return clean_json

def filter_comment(filename):
    '''
    Extracts comment data from json file, keeping desired columns
    '''
    raw_json = pd.read_json(path_or_buf=filename+".jsonl", lines=True, encoding="utf-8-sig")
    selected_data = ['body', 'created_utc', 'ups', 'subreddit']
        #body           - main body text
        #created_utc    - post creation time
        #ups            - number of upvotes
        #subreddit      - subreddit

    clean_json = raw_json[selected_data]
    clean_json = clean_json.rename(columns = {'body': 'text'})
    return clean_json

def main():
    #Extracting all data source files
    dem_post = filter_post('../DATA/r_democrats_posts')
    dem_comment = filter_comment('../DATA/r_democrats_comments')
    rep_post = filter_post('../DATA/r_Republican_posts')
    rep_comment = filter_comment('../DATA/r_Republican_comments')
    poldis_post = filter_post('../DATA/r_PoliticalDiscussion_posts')
    poldis_comment = filter_comment('../DATA/r_PoliticalDiscussion_comments')

    #Combine all posts and all comments together
    all_post = pd.concat([dem_post, rep_post, poldis_post], ignore_index = True)
    all_comment = pd.concat([dem_comment, rep_comment, poldis_comment], ignore_index = True)

    #Remove any missing comments, clear the selftext of posts if removed
    all_comment = all_comment[all_comment['text'] != '[removed]']
    all_post.loc[all_post['selftext'] == '[removed]', 'selftext'] = ''

    #Combine "Title" and "selftext" fields of post to form "text" which is contains all textual content
    all_post['text'] = all_post['title'] + ' ' + all_post['selftext']

    #drop any remaining missing
    all_comment = all_comment.dropna(subset=['text'])
    all_post = all_post.dropna(subset=['text'])

    #Writing to cleaned CSV files
    all_post.to_csv("../DATA/cleaned_posts.csv", index = False, encoding="utf-8-sig")
    all_comment.to_csv("../DATA/cleaned_comments.csv", index = False, encoding="utf-8-sig")

if __name__ == "__main__":
    main()



testing_filtercomments = filter_comment("../DATA/r_Republican_comments")

print(testing_filtercomments)

