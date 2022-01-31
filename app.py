from flask import Flask, render_template, request
import re
import string

import joblib
pipeline = joblib.load('pipeline.sav')
pipeline1 = joblib.load('pipeline1.sav')
pipeline2 = joblib.load('pipeline2.sav')
pipeline3 = joblib.load('pipeline3.sav')


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api', methods=['POST'])
def proccess():
    text = request.form['box']
    text = text.lower()
    text = re.sub('\[.*?\]', '', text)
    text = re.sub("\\W"," ",text) 
    text = re.sub('https?://\S+|www\.\S+', '', text)
    text = re.sub('<.*?>+', '', text)
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\n', '', text)
    query = re.sub('\w*\d\w*', '', text)   
    pred = pipeline.predict([query])
    pred1 = pipeline1.predict([query])
    pred2 = pipeline2.predict([query])
    pred3 = pipeline3.predict([query])
    dic = {1:'real',0:'fake'}
    return render_template('index.html', pre=("the news is predicted by Logistic Regression ="+dic[pred[0]]),
                           pre1=("the news is predicted by Decision Tree Classifier ="+dic[pred1[0]]),
                           pre2=("the news is predicted by Gradient Boosting Classifier ="+dic[pred2[0]]),
                           pre3=("the news is predicted by Random Forest Classifier ="+dic[pred3[0]]))
                                                                


if __name__=="__main__":
    app.run()

