from flask import Flask, render_template
import pickle
import pandas as pd
import random

app = Flask(__name__)

# Load model & features
model = pickle.load(open('model/model.pkl', 'rb'))
features = pickle.load(open('model/features.pkl', 'rb'))

# Generate realistic transaction
def generate_transaction(features):
    data = {}
    for f in features:
        if f == "Amount":
            data[f] = random.uniform(10, 50000)
        elif f == "Time":
            data[f] = random.uniform(1, 200000)
        else:
            data[f] = random.uniform(-3, 3)
    return data

# Home page
@app.route('/')
def home():
    return render_template('index.html')

# Single simulation
@app.route('/simulate')
def simulate():

    input_data = generate_transaction(features)
    input_df = pd.DataFrame([input_data])

    prob = model.predict_proba(input_df)[0][1]

    if prob > 0.8:
        risk = "High Risk 🚨"
        decision = "BLOCK 🚫"
    elif prob > 0.4:
        risk = "Medium Risk ⚠️"
        decision = "OTP Verification"
    else:
        risk = "Low Risk ✅"
        decision = "ALLOW"

    return render_template('index.html',
                           probability=round(prob*100,2),
                           risk=risk,
                           decision=decision,
                           transaction=input_data)

# Live monitoring
@app.route('/live')
def live():

    transactions = []

    for _ in range(10):
        input_data = generate_transaction(features)
        input_df = pd.DataFrame([input_data])

        prob = model.predict_proba(input_df)[0][1]

        if prob > 0.8:
            risk = "High 🚨"
            decision = "BLOCK"
        elif prob > 0.4:
            risk = "Medium ⚠️"
            decision = "OTP"
        else:
            risk = "Low ✅"
            decision = "ALLOW"

        transactions.append({
            "amount": round(input_data.get("Amount", 0), 2),
            "prob": round(prob * 100, 2),
            "risk": risk,
            "decision": decision
        })

    return render_template('index.html', transactions=transactions)

if __name__ == "__main__":
    app.run(debug=True)