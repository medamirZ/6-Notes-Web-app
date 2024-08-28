from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score,mean_squared_error
import pandas as pd
import pickle

data = pd.read_csv('sentiments/Emotions.csv')
x_data = data['content']
y_data = data['sentiment']

#converting sentiments to classes


#splitting data
x_train,x_test,y_train,y_test = train_test_split(x_data,y_data,random_state=42)
#init the TF-IDF vectorizer
vectorizer = TfidfVectorizer()
#transform the text data to numeric data and fit it (model learn)

x_train_vect = vectorizer.fit_transform(x_train)
x_test_vect = vectorizer.transform(x_test)



model = RandomForestClassifier(n_estimators=120,random_state=42)
model.fit(x_train_vect,y_train)
prediction = model.predict(x_test_vect)
cn = ["im heart broken"]
content = vectorizer.transform(cn)
prediction2 = model.predict(content)
print(f'content : {content}\nsentiment : {prediction2}')
accuracy = accuracy_score(prediction,y_test)
print(f'Accuracy : {accuracy*100:.2f}%')
pickle.dump(model,open('model.pkl','wb'))
pickle.dump(vectorizer,open('vectorizer.pkl','wb'))

#this model trained to a small to medium datasets givven an accuracy of 78%
