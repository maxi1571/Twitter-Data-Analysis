import json
import pandas as pd
from textblob import TextBlob

def read_json(json_file: str)->list:
    """
    json file reader to open and read json files into a list
    Args:
    -----
    json_file: str - path of a json file
    
    Returns
    -------
    length of the json file and a list of json
    """

    tweets_data = []
    for tweets in open(json_file,'r'):
        tweets_data.append(json.loads(tweets))
    

    return len(tweets_data), tweets_data

class TweetDfExtractor:
    """
    this function will parse tweets json into a pandas dataframe
    
    Return
    ------
    dataframe
    """
    def __init__(self, tweets_list):
        
        self.tweets_list = tweets_list

    # an example function
    def find_statuses_count(self)->list:
        statuses_count = [x['user']['statuses_count'] if 'statuses_count' in x else '' for x in self.tweet_list]
        return statuses_count
        
    def find_full_text(self)->list:
        try:
            text = [x['extended_tweet']['full_text'] for x in self.tweets_list]
        except KeyError:
            text = None
        return text
    def find_sentiments(self, text)->list:
        try:
            polaritys = []
            subjectivitys = []
            for x in text:
                sentimentes = TextBlob(x)
                polaritys.append(sentimentes.sentiment.polarity)
                subjectivitys.append(sentimentes.sentiment.subjectivity)
        except TypeError:
            polaritys = None
            subjectivitys = None
        return polaritys, subjectivitys

    def find_created_time(self)->list:
        try:
            created_at = [x['created_at'] for x in self.tweets_list]
        except KeyError:
            created_at = None
        return created_at

    def find_source(self)->list:
        try:
            source = [x['source'] for x in self.tweets_list]
        except KeyError:
            source = None
        return source

    def find_screen_name(self)->list:
        try:
            screen_name = [x['screen_name'] for x in self.tweets_list]
        except KeyError:
            screen_name = None
        return screen_name
    def find_followers_count(self)->list:
        try:
            followers_count = [x['user']['followers_count'] for x in self.tweets_list]
        except KeyError:
            followers_count = None
        return followers_count
    def find_friends_count(self)->list:
        try:
            friends_count = [x['user']['friends_count'] for x in self.tweets_list]
        except KeyError:
            friends_count = None
    def is_sensitive(self)->list:
        try:
            is_sensitive = [x['possibly_sensitive'] for x in self.tweets_list]
        except KeyError:
            is_sensitive = None

        return is_sensitive

    def find_favourite_count(self)->list:
        try:
            favorites_count = [x['retweeted_status']['favorite_count'] for x in self.tweets_list]
        except KeyError:
            favorites_count = None
        return favorites_count
    def find_retweet_count(self)->list:
        try:
            retweet_count =  [x['retweeted_status']['retweet_count'] for x in self.tweets_list]
        except KeyError:
            retweet_count = None
        return retweet_count
    def find_hashtags(self)->list:
        try:
            hashtags =  [x['extended_tweet']['entities']['hashtags'] for x in self.tweets_list]
        except KeyError:
            hashtags = None 
        return hashtags
    def find_mentions(self)->list:
        try:
            mentions = [x['extended_tweet']['entities']['user_mentions']['name'] if 'extented_tweet' in x else '' for x in self.tweets_list]
        except TypeError:
            mentions = None
        return mentions

    def find_location(self)->list:
        try:
            location = self.tweets_list['user']['location']
        except TypeError:
            location = ''
        
        return location

    
        
        
    def get_tweet_df(self, save=False)->pd.DataFrame:
        """required column to be generated you should be creative and add more features"""
        
        columns = ['created_at', 'source', 'original_text','polarity','subjectivity', 'lang', 'favorite_count', 'retweet_count', 
            'original_author', 'followers_count','friends_count','possibly_sensitive', 'hashtags', 'user_mentions', 'place']
        
        created_at = self.find_created_time()
        source = self.find_source()
        text = self.find_full_text()
        polarity, subjectivity = self.find_sentiments(text)
        #polarity, subjectivity = 1,2
        #lang = self.find_lang()
        lang = "what"
        fav_count = self.find_favourite_count()
        retweet_count = self.find_retweet_count()
        screen_name = self.find_screen_name()
        follower_count = self.find_followers_count()
        friends_count = self.find_friends_count()
        sensitivity = self.is_sensitive()
        hashtags = self.find_hashtags()
        mentions = self.find_mentions()
        #mentions = "do"
        location = self.find_location()
        data = zip(created_at, source, text, polarity, subjectivity, lang, fav_count, retweet_count, screen_name, follower_count, friends_count, sensitivity, hashtags, mentions, location)
        df = pd.DataFrame(data=data, columns=columns)

        if save:
            df.to_csv('processed_tweet_data.csv', index=False)
            print('File Successfully Saved.!!!')
        
        return df

                
if __name__ == "__main__":
    # required column to be generated you should be creative and add more features
    columns = ['created_at', 'source', 'original_text','clean_text', 'sentiment','polarity','subjectivity', 'lang', 'favorite_count', 'retweet_count', 
    'original_author', 'screen_count', 'followers_count','friends_count','possibly_sensitive', 'hashtags', 'user_mentions', 'place', 'place_coord_boundaries']
    _, tweet_list = read_json("./data/covid19.json")
    tweet = TweetDfExtractor(tweet_list)
    tweet_df = tweet.get_tweet_df() 

    # use all defined functions to generate a dataframe with the specified columns above

    