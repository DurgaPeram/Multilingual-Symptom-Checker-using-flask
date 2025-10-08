from flask import Flask, render_template, request, jsonify
import pandas as pd
import spacy
try:
    from spellchecker import SpellChecker
except Exception as _e:
    # If the installed 'spellchecker' package is missing native dependencies or is the
    # wrong package, avoid crashing at import time by providing a minimal fallback.
    # This preserves runtime behavior (no spelling corrections) while allowing
    # the rest of the app to load for debugging. Recommended permanent fix:
    # uninstall the broken package and install the maintained one: `pyspellchecker`.
    class SpellChecker:
        def __init__(self, *args, **kwargs):
            pass
        def correction(self, word):
            return word
from pathlib import Path

app = Flask(__name__)

# Load datasets using paths relative to this file so the app works from the repo/workspace
BASE_DIR = Path(__file__).resolve().parent
symptoms_df = pd.read_csv(BASE_DIR / 'diseases_and_symptoms.csv', on_bad_lines='skip')
descriptions_df = pd.read_csv(BASE_DIR / 'disease_descriptions.csv', on_bad_lines='skip')

# Load spaCy's English language model if available (graceful fallback)
try:
    nlp = spacy.load("en_core_web_sm")
except Exception as e:
    print("spaCy model 'en_core_web_sm' not available:", e)
    nlp = None

# Initialize SpellChecker
spell = SpellChecker()

def extract_multi_word_symptoms():
  
    multi_word_symptoms = set()
    for _, row in symptoms_df.iterrows():
        for i in range(1, 5):  # Assuming there are 4 symptom columns
            symptom = row[f'Symptom{i}']
            if isinstance(symptom, str) and len(symptom.split()) > 1:
                multi_word_symptoms.add(symptom.lower())  # Store in lowercase for matching
    return multi_word_symptoms

multi_word_symptoms = extract_multi_word_symptoms()

def process_user_input(user_input):
    
    # Step 1: Correct spelling for each word in the input
    corrected = []
    words = user_input.split()  # Split input into words
    
    # Correct spelling of individual words
    corrected_words = [spell.correction(word) or word for word in words]
    corrected_phrase = " ".join(corrected_words)
    corrected.append(corrected_phrase)
    
    # Join corrected phrases into a single string
    input_text = " ".join(corrected).lower()
    print(f"Corrected input: {input_text}")
    
    # Break the input into separate words
    words = input_text.split()
    
    # Combine words into pairs check for matches
    matched_symptoms = []
    
    #  generate combinations
    def check_combinations(word_list, n):
        combinations = []
        for i in range(len(word_list) - n + 1):
            combination = " ".join(word_list[i:i + n])
            if combination in multi_word_symptoms:
                combinations.append(combination)
        return combinations
    matched_symptoms.extend(check_combinations(words, 2))  # Pairs
    matched_symptoms.extend(check_combinations(words, 3))  
    
    print(f"Matched symptoms: {matched_symptoms}")
    
    words.extend(matched_symptoms)
    # normalize to lowercase and remove duplicates while preserving order
    normalized = [w.lower() for w in words if isinstance(w, str) and w.strip()]
    final_symptoms = list(dict.fromkeys(normalized))
    return final_symptoms


def find_disease(symptoms):
    for _, row in symptoms_df.iterrows():
        disease_symptoms = {row[f'Symptom{i+1}'].lower() for i in range(4) if pd.notna(row[f'Symptom{i+1}'])}
        
        # Count matching symptoms
        matches = len(set(symptoms).intersection(disease_symptoms))
        print(matches)
        if matches >= 3:
            return row['Disease']
    return None


def get_description(disease, language_code):
    # Find description for the disease in the specified language
    description_row = descriptions_df[
        (descriptions_df['Disease'].str.lower() == disease.lower()) &
        (descriptions_df['Language Code'] == language_code)
    ]
    # (debug) removed noisy DataFrame print

    # Return description if found
    if not description_row.empty:
        return description_row.iloc[0]['Description']
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/feedback')
def feedback():
    return render_template('feedback.html')

@app.route('/scheams')
def scheams():
    return render_template('scheams.html')

@app.route('/help')
def help():
    return render_template('help.html')

@app.route('/analyze', methods=['POST'])
def analyze_symptoms():
    """
    Analyzes user-input symptoms, finds a matching disease, and returns its description.
    """
    data = request.get_json()
    symptoms = data.get('symptoms', [])
    language = data.get('language', 'en')
    
    print(f"Received symptoms: {symptoms}, Language: {language}")
    
    # Process user input (spell check and lemmatization)
    processed_symptoms = process_user_input(" ".join(symptoms))  # Join symptoms to process them together
    
    print(processed_symptoms)
    # Find the disease based on symptoms
    disease = find_disease(processed_symptoms)
    
    if disease:
        # Find description in the specified language
        description = get_description(disease, language)
        if description:
            return jsonify({"disease": disease, "description": description})
    
    # Custom message if no disease matches
    return jsonify({
        "description": "Sorry, I am unable to find the disease based on the given symptoms. Please consult a doctor nearby you."
    })

if __name__ == '__main__':
    app.run(debug=True)
