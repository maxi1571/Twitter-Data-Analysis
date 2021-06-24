import unittest
import pandas as pd
import sys, os
from pandas.core.indexing import convert_to_index_sliceable
sys.path.append(os.path.abspath(os.path.join('..')))

from clean_tweets_dataframe import Clean_Tweets

df = pd.read_csv("../processed_tweet_data.csv")
columns = ['created_at', 'source', 'original_text','clean_text', 'sentiment','polarity','subjectivity', 'lang', 'favorite_count', 'retweet_count', 
    'original_author', 'screen_count', 'followers_count','friends_count','possibly_sensitive', 'hashtags', 'user_mentions', 'place', 'place_coord_boundaries']

class Test_Clean_Tweet(unittest.TestCase):


    def setUp(self) -> pd.DataFrame:
            
        self.df = Clean_Tweets(df=df)
        #  tweet_df = self.df.get_tweet_df()         


    def test_drop_unwanted_column(self):
        self.assertEqual(self.df.drop_unwanted_column(df).columns, columns)

    def test_convert_to_datetime(self):
        self.assertEqual(self.df.convert_to_datetime(df)['creat_at'],[])

    def test_drop_duplicate(self):
        self.assertEqual(self.df.drop_duplicate(df),[])
    
    def test_convert_to_numbers(self):
        self.assertEqual(type(self.df.convert_to_numbers(df)['polarity'][0]),int) 

    def test_remove_non_english_tweets(self):
        self.assertEqual(self.df.remove_non_english_tweets(df)['lang'][50],'eng')

if __name__ == '__main__':
	unittest.main()

    