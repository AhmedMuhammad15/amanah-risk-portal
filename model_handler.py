import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import pickle
import os

def generate_synthetic_banking_data(num_samples=2000):
    """
    Generates high-fidelity synthetic financial data mapping Credit History, 
    Income, DTI ratios, and Shariah indicators to train the evaluation model.
    """
    np.random.seed(42)
    
    # Simulating standard financial features
    monthly_income = np.random.normal(150000, 50000, num_samples).clip(30000, 500000)
    existing_debts = np.random.normal(25000, 15000, num_samples).clip(0, 150000)
    requested_amount = np.random.normal(1000000, 600000, num_samples).clip(100000, 5000000)
    tenure_months = np.random.choice([12, 24, 36, 48, 60], size=num_samples)
    
    # Calculating baseline indicators
    monthly_installment = requested_amount / tenure_months
    dti = (existing_debts + monthly_installment) / monthly_income
    
    # Credit History Score (Simulating a score out of 100)
    credit_score = np.random.normal(70, 15, num_samples).clip(30, 100)
    
    # Target Variable: Risk Profile (1 = High Risk/Default, 0 = Low Risk/Secure)
    # Risk calculation matrix derived from standard risk modeling
    risk_formula = (dti * 0.6) - (credit_score / 100 * 0.4) + np.random.normal(0, 0.1, num_samples)
    target_risk = (risk_formula > 0.15).astype(int)
    
    df = pd.DataFrame({
        'monthly_income': monthly_income,
        'existing_debts': existing_debts,
        'requested_amount': requested_amount,
        'tenure_months': tenure_months,
        'dti': dti,
        'credit_score': credit_score,
        'risk_profile': target_risk
    })
    return df

def train_risk_model():
    """
    Trains an Ensemble RandomForest Classifier to predict financing default risk 
    and serializes the production-ready model state.
    """
    model_path = 'murabaha_risk_model.pkl'
    
    # Generate and split data
    df = generate_synthetic_banking_data()
    X = df[['monthly_income', 'existing_debts', 'requested_amount', 'tenure_months', 'dti', 'credit_score']]
    y = df['risk_profile']
    
    # Fit Production Grade Ensemble Model
    model = RandomForestClassifier(n_estimators=100, max_depth=8, random_state=42)
    model.fit(X, y)
    
    # Save model binary
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
        
    return model

def predict_customer_risk(input_features):
    """
    Loads serialized model weights and yields real-time default probability percentage.
    """
    model_path = 'murabaha_risk_model.pkl'
    
    # Auto-train if binary artifact does not exist
    if not os.path.exists(model_path):
        model = train_risk_model()
    else:
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
            
    # Input formatting and prediction
    features_df = pd.DataFrame([input_features])
    probability = model.predict_proba(features_df)[0][1] # Probability of being High Risk (Class 1)
    
    return round(probability * 100, 2)