from flask import Flask, render_template, request, session
import json
import pandas as pd
import numpy as np
import spacy
from nltk.corpus import wordnet
import itertools
import joblib
import csv
import pickle
from sklearn.neighbors import KNeighborsClassifier
# Add other necessary imports


app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Required for session management

# Load NLP model
nlp = spacy.load('en_core_web_sm')

# Load data
df_tr = pd.read_csv('Medical_dataset/Training.csv')
df_tt = pd.read_csv('Medical_dataset/Testing.csv')

# Load model
knn_clf = joblib.load('model/knn.pkl')

# Load dictionaries
description_list = {}
severityDictionary = {}
precautionDictionary = {}

def load_dictionaries():
    global description_list, severityDictionary, precautionDictionary
    with open('Medical_dataset/symptom_Description.csv') as file:
        reader = csv.reader(file)
        description_list = {rows[0]: rows[1] for rows in reader}

    with open('Medical_dataset/symptom_severity.csv') as file:
        reader = csv.reader(file)
        severityDictionary = {rows[0]: int(rows[1]) for rows in reader}

    with open('Medical_dataset/symptom_precaution.csv') as file:
        reader = csv.reader(file)
        precautionDictionary = {rows[0]: rows[1:] for rows in reader}

load_dictionaries()

# Preprocess the symptoms list
def clean_symp(sym):
    return sym.replace('_', ' ').replace('.1', '').replace('(typhos)', '').replace('yellowish', 'yellow').replace('yellowing', 'yellow')

all_symp = [clean_symp(sym) for sym in df_tr.columns[:-1]]

def preprocess(doc):
    nlp_doc = nlp(doc)
    return ' '.join([token.lemma_.lower() for token in nlp_doc if not token.is_stop and token.is_alpha])

all_symp_pr = [preprocess(sym) for sym in all_symp]

# Mapping between processed symptoms and original columns
col_dict = dict(zip(all_symp_pr, df_tr.columns[:-1]))

# Functions for syntactic and semantic similarity
def jaccard_set(str1, str2):
    set1, set2 = set(str1.split()), set(str2.split())
    return len(set1 & set2) / len(set1 | set2)

def syntactic_similarity(symp_t, corpus):
    scores = [jaccard_set(symp_t, sym) for sym in corpus]
    max_score = max(scores)
    if max_score == 0:
        return 0, []
    max_index = np.argmax(scores)
    return 1, [corpus[max_index]]

def semanticD(doc1, doc2):
    doc1_words, doc2_words = preprocess(doc1).split(), preprocess(doc2).split()
    score = 0
    for w1 in doc1_words:
        for w2 in doc2_words:
            syn1, syn2 = lesk(doc1_words, w1), lesk(doc2_words, w2)
            if syn1 and syn2:
                sim = syn1.wup_similarity(syn2)
                if sim and sim > 0.25:
                    score += sim
    return score / (len(doc1_words) * len(doc2_words))

def semantic_similarity(symp_t, corpus):
    scores = [semanticD(symp_t, sym) for sym in corpus]
    max_score = max(scores)
    if max_score == 0:
        return 0, []
    max_index = np.argmax(scores)
    return 1, [corpus[max_index]]

def suggest_syn(sym):
    suggestions = []
    synonyms = wordnet.synsets(sym)
    lemmas = set(itertools.chain(*[syn.lemma_names() for syn in synonyms]))
    for lemma in lemmas:
        score, similar_symptom = semantic_similarity(lemma, all_symp_pr)
        if score > 0:
            suggestions.append(similar_symptom)
    return list(set(suggestions))

# Route handlers
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/get")
def get_bot_response():
    s = request.args.get('msg')
    step = session.get("step", "")
    
    if "step" in session:
        if session["step"] == "Q_C":
            name, age, gender = session["name"], session["age"], session["gender"]
            if s.lower() == "q":
                session.clear()
                return f"Thank you for using our service, {name}."
            else:
                session["step"] = "FS"
    
    if 'name' not in session:
        session['name'] = s
        session['step'] = "age"
        return "Welcome! Please enter your age."
    
    if session["step"] == "age":
        session["age"] = int(s)
        session["step"] = "gender"
        return "Please specify your gender."
    
    if session["step"] == "gender":
        session["gender"] = s
        session["step"] = "symptom"
        return "Please describe your main symptom."

    if session["step"] == "symptom":
        symptom = preprocess(s)
        syntactic_result, syntactic_match = syntactic_similarity(symptom, all_symp_pr)
        
        if syntactic_result == 1:
            session['symptoms'] = [syntactic_match[0]]
            session['step'] = 'second_symptom'
            return f"You mentioned {syntactic_match[0]}. Do you have another symptom?"
        else:
            semantic_result, semantic_match = semantic_similarity(symptom, all_symp_pr)
            if semantic_result == 1:
                session['symptoms'] = [semantic_match[0]]
                session['step'] = 'second_symptom'
                return f"You mentioned {semantic_match[0]}. Do you have another symptom?"
            else:
                suggestions = suggest_syn(symptom)
                if suggestions:
                    session['suggestions'] = suggestions
                    session['step'] = 'confirm_suggestion'
                    return f"Did you mean any of these: {', '.join(suggestions)}?"
                else:
                    return "I'm not sure about that symptom. Could you provide more details or specify another one?"
    
    if session["step"] == "confirm_suggestion":
        suggestions = session.get('suggestions', [])
        if suggestions and s.lower() in ["yes", "y"]:
            session['symptoms'] = [suggestions[0]]
            session['step'] = 'second_symptom'
            return f"You mentioned {suggestions[0]}. Do you have another symptom?"
        else:
            suggestions.pop(0)
            if suggestions:
                session['suggestions'] = suggestions
                return f"Did you mean any of these: {', '.join(suggestions)}?"
            else:
                session['step'] = 'symptom'
                return "I couldn't find a match for your symptom. Please try describing it again."
    
    if session["step"] == "second_symptom":
        second_symptom = preprocess(s)
        session['symptoms'].append(second_symptom)
        session['step'] = 'predict'
        return "Thank you. Now I will process your symptoms and make a prediction."
    
    if session["step"] == "predict":
        symptoms = session['symptoms']
        result = knn_clf.predict(OHV(symptoms, all_symp))
        session['step'] = 'done'
        return f"Based on your symptoms, you may have: {result[0]}. For more information, type 'info'."
    
    if session["step"] == "done":
        if s.lower() == "info":
            disease = session.get('disease', "")
            description = description_list.get(disease, "No description available.")
            return f"{description}"
        else:
            session.clear()
            return "Thank you for using our service. Goodbye!"

    return "Sorry, I didn't understand that. Could you please specify your symptom again?"

if __name__ == "__main__":
    app.run(debug=True)
