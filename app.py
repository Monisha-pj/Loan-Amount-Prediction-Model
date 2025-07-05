from flask import Flask, render_template, request
import joblib
import pandas as pd

app = Flask(__name__)
model = joblib.load('model.pkl')  # Load your trained model

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        # Get form data
        gender = 1 if request.form['gender'].lower() == 'male' else 0
        married = 1 if request.form['married'].lower() == 'yes' else 0
        dependents = 3 if request.form['dependents'] == '3+' else int(request.form['dependents'])
        education = 0 if request.form['education'].lower() == 'graduate' else 1
        self_employed = 1 if request.form['self_employed'].lower() == 'yes' else 0
        income = float(request.form['income'])
        co_income = float(request.form['co_income'])
        term = float(request.form['term'])
        credit = float(request.form['credit'])

        # Prepare input data
        input_df = pd.DataFrame([[gender, married, dependents, education, self_employed,
                                  income, co_income, term, credit]],
                                columns=['Gender', 'Married', 'Dependents', 'Education', 'Self_Employed',
                                         'ApplicantIncome', 'CoapplicantIncome', 'Loan_Amount_Term', 'Credit_History'])

        # Make prediction
        pred = model.predict(input_df)[0]
        loan_in_lakhs = round(pred / 100, 2)
        result = f"₹{loan_in_lakhs} Lakhs"

    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
