import os
import pandas as pd
import mysql.connector
import numpy as np
import streamlit as st
import altair as alt
from wordcloud import WordCloud
import plotly.express as px
from mysql.connector import Error
import matplotlib.pyplot as plt

class DBoperations:

    def DBConnect(self,dbName=None):
        conn=mysql.connector.connect(host='localhost',port="3306", user='root', password="",
                            database=dbName)
        cur = conn.cursor()
        return conn, cur
    def emojiDB(self,dbName: str) -> None:
        conn, cur = DBoperations.DBConnect(self,'tweets')
        dbQuery = f"ALTER DATABASE {dbName} CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;"
        cur.execute(dbQuery)
        conn.commit()

    def createDB(self,dbName: str) -> None:
        """

        Parameters
        ----------
        dbName :
            str:
        dbName :
            str:
        dbName:str :


        Returns
        -------

        """
        conn, cur = DBoperations.DBConnect(self)
        cur.execute(f"CREATE DATABASE IF NOT EXISTS {dbName};")
        conn.commit()
        cur.close()

    def createTables(self,dbName: str) -> None:
        """

        Parameters
        ----------
        dbName :
            str:
        dbName :
            str:
        dbName:str :


        Returns
        -------

        """
        conn, cur = DBoperations.DBConnect(self,'tweets')
        sqlFile = './schema.sql'
        fd = open(sqlFile, 'r')
        readSqlFile = fd.read()
        fd.close()

        sqlCommands = readSqlFile.split(';')

        for command in sqlCommands:
            try:
                res = cur.execute(command)
            except Exception as ex:
                print("Command skipped: ", command)
                print(ex)
        conn.commit()
        cur.close()

        return

    def preprocess_df(self,df: pd.DataFrame) -> pd.DataFrame:
        """

        Parameters
        ----------
        df :
            pd.DataFrame:
        df :
            pd.DataFrame:
        df:pd.DataFrame :


        Returns
        -------

        """
        cols_2_drop = ['Unnamed: 0', 'possibly_sensitive']
        try:
            df = df.drop(columns=cols_2_drop, axis=1)
            df = df.fillna(0)
        except KeyError as e:
            print("Error:", e)

        return df


    def insert_to_tweet_table(self,dbName: str, df: pd.DataFrame, table_name: str) -> None:
        """

        Parameters
        ----------
        dbName :
            str:
        df :
            pd.DataFrame:
        table_name :
            str:
        dbName :
            str:
        df :
            pd.DataFrame:
        table_name :
            str:
        dbName:str :

        df:pd.DataFrame :

        table_name:str :


        Returns
        -------

        """
        conn, cur = DBoperations.DBConnect(self,'tweets')

        df = DBoperations.preprocess_df(self,df)

    
        for _, row in df.iterrows():
            sqlQuery = f"""INSERT INTO {table_name} (created_at, source, original_text, polarity, subjectivity, lang,
                        favorite_count, retweet_count, original_author, followers_count, friends_count,
                        hashtags, user_mentions, place)
                VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
            data = (row[0], row[1], row[2], row[3], (row[4]), (row[5]), row[6], row[7], row[8], row[9], row[10], row[11],
                    row[12], row[13])

            try:
                # Execute the SQL command
                cur.execute(sqlQuery, data)
                # Commit changes in the database
                conn.commit()
                print("Data Inserted Successfully")
            except Exception as e:
                conn.rollback()
                print("Error: ", e)
        return

    def db_execute_fetch(self,*args, many=False, tablename='', rdf=True, **kwargs) -> pd.DataFrame:
        """

        Parameters
        ----------
        *args :

        many :
            (Default value = False)
        tablename :
            (Default value = '')
        rdf :
            (Default value = True)
        **kwargs :


        Returns
        -------

        """
        connection, cursor1 = DBoperations.DBConnect(self,'tweets')
        if many:
            cursor1.executemany(*args)
        else:
            cursor1.execute(*args)

        # get column names
        field_names = [i[0] for i in cursor1.description]

        # get column values
        res = cursor1.fetchall()

        # get row count and show info
        nrow = cursor1.rowcount
        if tablename:
            print(f"{nrow} records from {tablename} table")

        cursor1.close()
        connection.close()

        # return result
        if rdf:
            return pd.DataFrame(res, columns=field_names)
        else:
            return res

st.set_page_config(page_title="Dashboard", layout="wide")
class disp:
    def loadData(self):
        query = "select * from TweetInformation"
        df =DBoperations.db_execute_fetch(self,query, dbName="tweets", rdf=True)
        return df

    def selectHashTag(self):
        df = disp.loadData(self)
        hashTags = st.multiselect("choose combaniation of hashtags", list(df['hashtags'].unique()))
        if hashTags:
            df = df[np.isin(df, hashTags).any(axis=1)]
            st.write(df)


    def barChart(self,data, title, X, Y):
        title = title.title()
        st.title(f'{title} Chart')
        msgChart = (alt.Chart(data).mark_bar().encode(alt.X(f"{X}:N", sort=alt.EncodingSortField(field=f"{Y}", op="values",
                    order='ascending')), y=f"{Y}:Q").configure_axis(
                   labelFontSize=18,titleFontSize=20).properties(height=500))
        st.altair_chart(msgChart, use_container_width=True)

    def wordCloud(self):
        df = disp.loadData(self)
        cleanText = ''
        for text in df['original_text']:
            tokens = str(text).lower().split()
            cleanText += " ".join(tokens) + " "
        wc = WordCloud(width=650, height=450, background_color='white', min_font_size=5).generate(cleanText)
        st.title("Tweet Text Word Cloud")
        st.image(wc.to_array())

    def stBarChart(self):
        df = disp.loadData(self)
        dfCount = pd.DataFrame({'Tweet_count': df.groupby(['original_author'])['original_text'].count()}).reset_index()
        dfCount["original_author"] = dfCount["original_author"].astype(str)
        dfCount = dfCount.sort_values("Tweet_count", ascending=False)
        num = st.slider("Select number of Rankings", 0, 50, 5)
        title = f"Top {num} Ranking By Number of tweets"
        disp.barChart(self,dfCount.head(num), title, "original_author", "Tweet_count")
    
    
    def stBarChart2(self):
        df = disp.loadData(self)
        dfCount1 = pd.DataFrame({'Tweet_count': df.groupby(['hashtags'])['original_text'].count()}).reset_index()
        dfCount1["hashtags"] = dfCount1["hashtags"].astype(str)
        dfCount1 = dfCount1.sort_values("Tweet_count", ascending=False)
        num1 = st.slider("Select number of Rankings", 0, 40, 5)
        title = f"Top {num1} Hashtags"
        disp.barChart(self,dfCount1.head(num1), title, "hashtags", "Tweet_count") 

    def stBarChart3(self):
        df = disp.loadData(self)
        dfCount2 = pd.DataFrame({'Tweet_count': df.groupby(['place'])['original_text'].count()}).reset_index()
        dfCount2["place"] = dfCount2["place"].astype(str)
        dfCount2= dfCount2.sort_values("Tweet_count", ascending=False)  
        num1 = st.slider("Select number of Rankings", 0, 30, 5)
        title = f"Top {num1} Locations"
        disp.barChart(self,dfCount2.head(num1), title, "place", "Tweet_count")        
    
    def text_category (self,p):
        if p > 0:
            return 'positive'
        if p < 0:
            return 'negative'
        else:
            return 'neutral'
    def Text_catagory_Pie(self):
        df = disp.loadData(self)
        score = pd.Series([disp.text_category(self,row_value) for row_value in df['polarity']])
        df= pd.concat([df, score.rename("score")], axis=1)

        labels = ['neutral', 'positive', 'negative']
        neutral_count = len(df[df['score'] == "neutral"])
        positive_count = len(df[df['score'] == "positive"])
        negative_count = len(df[df['score'] == "negative"])
        
        sizes = [neutral_count, positive_count, negative_count]
        dict = { 'Text catagory': labels,'size': sizes} 
        dfCatagoryCount = pd.DataFrame(dict)     
        dfCatagoryCount["Text catagory"] = dfCatagoryCount["Text catagory"].astype(str)
        dfCatagoryCount = dfCatagoryCount.sort_values("size", ascending=False)
        
    
        st.title(" Text Catagory pie chart")
        fig = px.pie(dfCatagoryCount, values='size', names='Text catagory', width=500, height=350)
        fig.update_traces(textposition='inside', textinfo='percent+label')
       

        colB1, colB2 = st.beta_columns([2, 1])

        with colB1:
            st.plotly_chart(fig)
        with colB2:
            st.write(dfCatagoryCount) 

    def langPie(self):
        df = disp.loadData(self)
        dfLangCount = pd.DataFrame({'Tweet_count': df.groupby(['lang'])['original_text'].count()}).reset_index()
        dfLangCount["lang"] = dfLangCount["lang"].astype(str)
        dfLangCount = dfLangCount.sort_values("Tweet_count", ascending=False)
        dfLangCount.loc[dfLangCount['Tweet_count'] < 10, 'lang'] = 'Other langs'
        st.title(" Tweets lang pie chart")
        fig = px.pie(dfLangCount, values='Tweet_count', names='lang', width=500, height=350)
        fig.update_traces(textposition='inside', textinfo='percent+label')

        colB1, colB2 = st.beta_columns([2, 1])

        with colB1:
            st.plotly_chart(fig)
        with colB2:
            st.write(dfLangCount)


          
   

         
    
if __name__ == "__main__":
    #db1 = DBoperations()
    #db1.createDB('tweets')
    #db1.emojiDB('tweets')
    #db1.createTables('tweets')

    #df = pd.read_csv('../clean_processed_tweet_data.csv')
    #db1.insert_to_tweet_table('tweets', df=df, table_name='TweetInformation')

    obj1=disp()
    st.markdown("<p style='padding:30px;text-align:center; background-color:#000000;color:#00ECB9;font-size:26px;border-radius:10px;'>Twitter Data Analysis</p>", unsafe_allow_html=True)
    st.title("Data Display")
    obj1.selectHashTag()
    st.markdown("<p style='text-align:center;padding:10px; background-color:#000000;color:#00ECB9;font-size:16px;border-radius:10px;'>Section Break</p>", unsafe_allow_html=True)
    st.title("Data Visualizations")
    obj1.wordCloud()
    with st.beta_expander("Show More Graphs"):
        obj1.stBarChart()
        obj1.stBarChart2()
        obj1.stBarChart3()
        obj1.Text_catagory_Pie()
        obj1.langPie()
      
        
   