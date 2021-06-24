import unittest
import pandas as pd
import sys, os

from pandas.core.indexing import convert_to_index_sliceable
sys.path.append(os.path.abspath(os.path.join('..')))

from clean_tweets_dataframe import Clean_Tweets

df_clean = pd.read_csv("../clean_processed_tweet_data.csv")

df = pd.read_csv("../processed_tweet_data.csv")

class Test_Clean_Tweet(unittest.TestCase):


    def setUp(self) -> pd.DataFrame:
            
        self.df = Clean_Tweets(df=df)
        self.df_clean = df_clean
        #  tweet_df = self.df.get_tweet_df()         


    def test_drop_unwanted_column(self):
        self.assertEqual(self.df.drop_unwanted_column(df)['possibly_sensitive'].values, self.df_clean['possibly_sensitive'].values)

    def test_convert_to_datetime(self):
        self.assertEqual(self.df.convert_to_datetime(df)['creat_at'].values,self.df_clean['creat_at'].values)

    def test_drop_duplicate(self):
        self.assertEqual(self.df.drop_duplicate(df)['user_mentions'].values,self.df_clean['user_mentions'].values)
    
    def test_convert_to_numbers(self):
        self.assertEqual(self.df.convert_to_numbers(df)['polarity'].values,self.df_clean['polarity'].values) 

    def test_remove_non_english_tweets(self):
        self.assertEqual(self.df.remove_non_english_tweets(df)['original_text'].values,self.df_clean['original_text'].values)

if __name__ == '__main__':
	unittest.main()

    