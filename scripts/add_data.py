import os
import pandas as pd
import mysql.connector
from mysql.connector import Error

class DB:

    def DBConnect(self, dbName=None):
        conn=mysql.connector.connect(host='localhost',port="3306", user='root', password="",
                            database=dbName)
        cur = conn.cursor()
        return conn, cur
    def emojiDB(self, dbName: str) -> None:
        conn, cur = DB.DBConnect(self,dbName)
        dbQuery = f"ALTER DATABASE {dbName} CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;"
        cur.execute(dbQuery)
        conn.commit()

    def createDB(self, dbName: str) -> None:
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
        conn, cur = DB.DBConnect(self)
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
        conn, cur = DB.DBConnect(self,dbName)
        sqlFile = '../schema.sql'
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

    def preprocess_df(self, df: pd.DataFrame) -> pd.DataFrame:
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


    def insert_to_tweet_table(self, dbName: str, df: pd.DataFrame, table_name: str) -> None:
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
        conn, cur = DB.DBConnect(self,dbName)

        df = DB.preprocess_df(self,df)

    
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
                # Commit your changes in the database
                conn.commit()
                print("Data Inserted Successfully")
            except Exception as e:
                conn.rollback()
                print("Error: ", e)
        return

    def db_execute_fetch(self, *args, many=False, tablename='', rdf=True, **kwargs) -> pd.DataFrame:
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
        connection, cursor1 = DB.DBConnect(self,**kwargs)
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
            print(f"{nrow} recrods fetched from {tablename} table")

        cursor1.close()
        connection.close()

        # return result
        if rdf:
            return pd.DataFrame(res, columns=field_names)
        else:
            return res


if __name__ == "__main__":
    MY_db = DB()
    #MY_db.createDB(dbName='tweets')
    #MY_db.emojiDB(dbName='tweets')
    #MY_db.createTables(dbName='tweets')

    df = pd.read_csv('../data/clean_processed_tweet_data.csv')
    MY_db.insert_to_tweet_table(dbName='tweets', df=df, table_name='TweetInformation')