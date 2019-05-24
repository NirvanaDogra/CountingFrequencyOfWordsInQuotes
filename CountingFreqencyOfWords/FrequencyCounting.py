import mysql.connector
from mysql.connector import Error
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import string
import webbrowser
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd

word_Count={};
puntuation=[".",";",":","!","?","/","\\",",","#","@","$","&",")","("]

def generateWordCloud(word_Count):
    text="my name is nirvan"
    wordcloud = WordCloud(background_color ='white', stopwords=None ).fit_words(word_Count)

    # Display the generated image:
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    #plt.show()
    wordcloud.to_file("wordCloud.png");



#This fuction is used to create the webpage as output
#The function take a dictionary as input and prints the key and values as output.
def createWebPage(word_Count):
    file=open("index1.html", "w+");
    str="<html>\n<style>table, th, td {border: 1px solid black;}\n.image{\nposition:relative;\nleft:30vw;\n}\n.table1{\nposition:absolute;\ntop:8vw;\n }\n</style></head>\n<div><h1>The output is as follows :</h1><img class=\"image\" src=\"wordCloud.png\"></div><br>\n<body>\n<table class=\"table1\">\n<tr><th>word</th><th>frequency</th></tr>\n"
    #append
    file.write(str)

    for words in word_Count.keys():
        val="<tr><td>%s</td><td>%s</td></tr>\n"%(words, word_Count[words]);
        print(val)
        #append
        file.write(val);

    val="</table></body></html>"
    file.write(val)
    #apend
    file.close();

    webbrowser.open('index1.html')  #Here the opeing of webpage is getting automated. The webpage should open automatically on executing this command


#this function take string as input and preprocesses it to be used for clacualtion
# As preporcessing it does the following
# 1) converts every word to lower case
# 2) Removes the puntuation
# 3) Lemmatize the word that is make it in its root form.
# 3) return the new word
def wordProcess(example_sent):
    example_sent = example_sent.lower()


    word_tokens = word_tokenize(example_sent)



    filtered_sentence="";
    for w in word_tokens:
        if not (w in puntuation):
            filtered_sentence+=(w)
    return lemmatizer.lemmatize(filtered_sentence)




#This part connects the pyhton program to MySQL
# All the word in the table1 are saved into the dictionary
try:
    connection = mysql.connector.connect(host='localhost', # TODO change hostname
                             database='words', #TODO change the database name
                             user='root', #TODO change the username
                             password='') #TODO change the password
    if connection.is_connected():
       db_Info = connection.get_server_info()
       print("Connected to MySQL database... MySQL Server version on ",db_Info)

       cursor = connection.cursor()

       sql_Query="SELECT * FROM `table 1`"  #This table contains all the words

       cursor.execute(sql_Query)
       record = cursor.fetchall()
       print("The record count", cursor.rowcount)
       for rows in record:
           word_Count[(rows[1].lower()).strip()]=0;

    print(word_Count)
except Error as e :
    print ("Error while connecting to MySQL", e)
finally:
    #closing database connection.
    if(connection.is_connected()):
        cursor.close()
        connection.close()
        print("MySQL connection is closed")

#THis remakes the connection and this times calculate the frequency of the the words in the sentence
try:
    lemmatizer = WordNetLemmatizer()
    connection = mysql.connector.connect(host='localhost',
                                         database='words',
                                         user='root',
                                         password='')
    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("Connected to MySQL database... MySQL Server version on ", db_Info)

        cursor = connection.cursor()

        sql_Query = "SELECT * FROM `table 2`"  # This table contains all the words

        cursor.execute(sql_Query)
        record = cursor.fetchall()
        print("The record count", cursor.rowcount)
        for rows in record:
            print(rows)
            for word in rows[2].split(' '):

                newVal=wordProcess(word)

                if newVal in word_Count.keys():
                    word_Count[newVal]+=1;
                    print(word)
            print("############################")
    print(word_Count)




except Error as e :
    print ("Error while connecting to MySQL", e)
finally:
    #closing database connection.
    if(connection.is_connected()):
        cursor.close()
        connection.close()
        print("MySQL connection is closed")
        print("creating a web page");
        generateWordCloud(word_Count);
        createWebPage(word_Count)