from flask import Flask,render_template, request, jsonify
import pandas as pd
import sqlite3

app = Flask(__name__)

# Load the disease dataset
dataset = pd.read_csv('symptom.csv')

# Connect to the database with disease descriptions
conn = sqlite3.connect('disease_descriptions.db')
cursor = conn.cursor()

# Function to match symptoms and retrieve disease description
def find_disease_description(symptoms):
    for _, row in dataset.iterrows():
        disease_symptoms = [row['Symptom1'], row['Symptom2'], row['Symptom3'], row['Symptom4']]
        matches = sum(1 for symptom in symptoms if symptom in disease_symptoms)
        
        if matches >= 3:
            disease_name = row['Disease']
            cursor.execute("SELECT description FROM descriptions WHERE disease = ?", (disease_name,))
            description = cursor.fetchone()
            return disease_name, description[0] if description else "Description not found."
    
    return None, "Sorry, I am unable to find the disease based on the given symptoms. Can you please consult a doctor nearby you."
@app.route('/')
def index():
    return render_template('new2.html')
# API endpoint to handle symptom analysis
@app.route('/analyze', methods=['POST'])
def analyze_symptoms():
    data = request.json
    symptoms = data.get('symptoms', [])
    language = data.get('language', 'en')

    disease_name, description = find_disease_description(symptoms)

    response = {"disease": disease_name or "Unknown", "description": description, "language": language}
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
