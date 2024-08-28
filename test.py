import pickle
from sklearn.feature_extraction.text import TfidfVectorizer

model = pickle.load(file=open('model.pkl','rb'))
feeling = ['not angry','happier','not happy',"i'm not happy",'noo','im not angry dont you know']

vector = pickle.load(file=open('vectorizer.pkl','rb'))
feeling2 = vector.transform(feeling)
prediction = model.predict(feeling2)
print(prediction)

