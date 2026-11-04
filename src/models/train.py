import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import LinearSVC
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score, f1_score, classification_report, confusion_matrix

train = pd.read_csv("data/processed/train.csv").dropna()
test = pd.read_csv("data/processed/test.csv").dropna()

# vectoriseur TF-IDF
tfidf = TfidfVectorizer(max_features=10000, ngram_range=(1, 2), min_df=2)
X_train = tfidf.fit_transform(train["text"])
X_test = tfidf.transform(test["text"])
y_train, y_test = train["label"], test["label"]

# modèle de Logistic Regression
lr = LogisticRegression(max_iter=1000).fit(X_train, y_train)
print("LogReg accuracy :", accuracy_score(y_test, lr.predict(X_test)))

# autres algorithmes (Random Forest, SVM)
rf = RandomForestClassifier(n_estimators=100, n_jobs=-1, random_state=42).fit(X_train, y_train)
print("RandomForest accuracy :", accuracy_score(y_test, rf.predict(X_test)))
print("RandomForest f1-score :", f1_score(y_test, rf.predict(X_test), average="macro"))
print("RandomForest matrice de confusion :\n", confusion_matrix(y_test, rf.predict(X_test)))

svm = LinearSVC().fit(X_train, y_train)
print("SVM accuracy :", accuracy_score(y_test, svm.predict(X_test)))
print("SVM f1-score :", f1_score(y_test, svm.predict(X_test), average="macro"))
print("SVM matrice de confusion :\n", confusion_matrix(y_test, svm.predict(X_test)))

# optimiser les hyperparamètres avec GridSearchCV
grid = GridSearchCV(LogisticRegression(max_iter=1000), {"C": [1, 10, 30, 100]}, cv=3, scoring="f1_macro")
grid.fit(X_train, y_train)
best = grid.best_estimator_
print("Meilleur C :", grid.best_params_)

# metrique pour chaque modèle
print("Logistic Regression optimal report:")
print(classification_report(y_test, best.predict(X_test)))
print("Random Forest classification report:")
print(classification_report(y_test, rf.predict(X_test)))
print("SVM classification report:")
print(classification_report(y_test, svm.predict(X_test)))

# métriques appropriées (accuracy, F1-score, matrice de confusion)
y_pred = best.predict(X_test)
print("Best Model classification report:")
print(classification_report(y_test, y_pred))
print("Best Model confusion matrix:")
print(confusion_matrix(y_test, y_pred))

# sauvegarder le meilleur modèle et le vectoriseur
joblib.dump(tfidf, "models/vectorizer.pkl")
joblib.dump(best, "models/model.pkl")