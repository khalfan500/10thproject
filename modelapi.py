from flask import Flask
from flask import request
import pickle
import re
import psycopg2
import itertools
from sklearn.metrics import accuracy_score
app = Flask(__name__)

connection =psycopg2.connect(user='postgres', password='ko123', host='127.0.0.1', port='5432', database='postgres')

with open('model2.pickle', 'rb') as file:
    model = pickle.load(file)

with open('vectorizer2.pickle', 'rb') as file:
    vectorizer = pickle.load(file)



@app.route('/get_data', methods=['GET'])
def get_data(max_count):
    try:
        cursor = connection.cursor()
        select = "select d.text, l.number from data_input d, data_labeling l where d.id = l.id order by d.created_on limit %s"
        cursor.execute(select, (max_count,))
        data = cursor.fetchall()
        words = {}
        for row in data:
            d1 = {row[0]: row[1]}
            words.update(d1)
        return words
    except (Exception, psycopg2.Error) as error:
        print("Error :", error)


@app.route('/get_total_data_count', methods=['GET'])
def get_total_data_count():
    cursor1 = connection.cursor()
    select1 = "select count(id), number from (SELECT id as id,number as number FROM data_labeling order by created_on limit 100) s where number =1 group by number;"
    cursor1.execute(select1)
    positive_l = cursor1.fetchall()
    print("Positive Count is:")
    for row in positive_l:
        print("Count  = ", row[0], "\n")
    cursor2 = connection.cursor()
    select2 = "select count(id), number from (SELECT id as id,number as number FROM data_labeling order by created_on limit 100) s where number =0 group by number;"
    cursor2.execute(select2)
    negative_l = cursor2.fetchall()
    print("Negative Count is:")
    for row in negative_l:
        print("Count  = ", row[0], "\n")


def clean_text(text):
    text = text.lower()
    text = re.sub("@[a-z0-9_]+", ' ', text)
    text = re.sub("[^ ]+\.[^ ]+", ' ', text)
    text = re.sub("[^ ]+@[^ ]+\.[^ ]", ' ', text)
    text = re.sub("[^a-z\' ]", ' ', text)
    text = re.sub(' +', ' ', text)
    return text


result_dict = {0: 'negative', 1: 'positive'}


if __name__ == "__main__":
    app.run(debug=True, port=3000)
