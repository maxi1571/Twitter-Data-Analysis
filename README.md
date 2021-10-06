# Twitter Data Sentiment Analysis and Topic Modeling

## Abstract
* The project focuses on using sentiment and topic analysis on a Twitter dataset to generate a 
  dashboard that is able to do sentiments predictions on different texts.

* The dataset used is a bulk json file. The wanted data was extracted and cleaned.
  Polarity and text was selected to perform sentiment analysis. Machine learning model was trained on the dataset to classify text to positive, negative and neutral. Accuracy metrics are used to check for prediction accuracy.

## Data

* The data is collected using the keywords:

      "COVID19 Africa"
      "COVID19 Vaccination Africa"
      "Sars-Cov2 Mutation Africa"

* The length of data collected is around 6225 rows and was saved in a json format.


## Methodology

### Data Extraction and Cleaning

* Data set was provided as a json file. The json file contains different keys to find specific
  keywords to contain in the dataset. Using python the json file was read and 19 different columns with 6225 rows were built by selecting specific keywords.
* The retrieved data was saved in a csv file.
* The retrieved data was cleaned using pandas methods and some additional preprocessing took place.
* For topic modeling nltk is used to further clean and remove stopwords.Model building.


### MOdel Building

* From the cleaned data set ‘original_text’ and ‘polarity’ was used to train the model.
* Using sklearn train test split the cleaned data was splitted for training.
* SGD classifier was used to train the train data.
* Accuracy metrics is used to check how well the mode is doing.
* Gensim model is used for topic modeling.


### Code Testing

* Unittesting was created for data extraction and data cleaning python scripts to
  test the code. Travis CI was used to automate the testing of the scripts every time change took place in the code.


### Data Loading to Database

* An SQL database Tweet was created. A database schema was created for 14 columns to be inserted
  in the database.
* Data was inserted to the SQL database and was displayed by using xampp UI.


### Web App

* Using streamlit library a web app was created in order to visualization our dataset
* Tweet SQL database was connected to the web app
* Data set visualization was performed in the web app for multiple analysis made upon the data.


## Running the Web App

### Steps
            * First download the requirments by running the command "pip install -r requirements.txt" on
            terminal.
            * Create an SQL database using the schema.sql provide.
            * Specify your SQL database on add_data.py to your version and specify the port number.
            * run add_data.py
            * Then run web_app.py using the command "streamlit run web_app.py"
            * It will open a localhost
            * It will open a dashboard which you can manipulate the data and see different data version visulization


## Result Conclusion

* So far the trained model was tested using unseen data and an accuracy of 97% was found for
  sentiment analysis. 
* On topic modeling a Perplexity of -5.307 and coherence Score of 0.43 was achieved.
* Sience the project is time constrained the data set used initially was not clean so refining
  took time.
* The web app displays a good analysis of the data by giving multiple visualizations of the
  dataset and also easy selection for analysing the data base on hashtags mentioned on the tweet data.
* From the word cloud the most occuring work in the tweet is covid19
