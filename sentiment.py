import requests
import json


result_dict = {0: 'negative', 1: 'positive'}

URL2 = "http://127.0.0.1:3000/get_total_data_count"
response2 = requests.get(url=URL2)
dataw2 = response2.json()
print (dataw2)

URL = "http://127.0.0.1:3000/get_data"
PARAMS = {'max_count': 3}
response = requests.get(url=URL, params=PARAMS)
dataw = response.json()
print (dataw)

listwords = []
listste = []
for k, v in dataw.items():
    listwords.append(k)
    listste.append(v)
listn = []
listp = []
res = []
results = []
resultcount = {}
try:
    for t in listwords:
        text = str(request.args.get(t))
        text = clean_text(text)
        vector = vectorizer.transform([text])
        result = model.predict(vector)
        res.append([result[0]])
        results = list(itertools.chain(*res))
        if result_dict[result[0]] == 0:
            listn.append(result_dict[result[0]])
            r1 = {"negative": len(listn)}
            resultcount.update(r1)
        else:
            listp.append(result_dict[result[0]])
            r2 = {"positive": len(listp)}
            resultcount.update(r2)
    print("Accuracy:")
    print(accuracy_score(listste, results))
    print(listste)
    print(results)
    print(resultcount)
except:
    print ("Error")

