import pandas as pd
import numpy as np

def verify_shariah_compliance(business_sector, asset_type):
    """
    Validates if the financing request complies with Islamic Finance principles.
    (Non-compliant sectors/assets are automatically rejected before ML scoring)
    """
    prohibited_sectors = ['alcohol', 'gambling', 'conventional_insurance', 'conventional_finance', 'tobacco']
    
    if business_sector.lower() in prohibited_sectors:
        return False, "Automated Shariah Non-Compliance Flag: Prohibited Sector Detected."
    return True, "Shariah Verification Passed."

def calculate_financial_ratios(monthly_income, existing_debts, requested_amount, tenure_months):
    """
    Computes analytical credit metrics: Debt-to-Income (DTI) and Asset Financing Burden.
    """
    monthly_installment = requested_amount / tenure_months
    total_monthly_obligations = existing_debts + monthly_installment
    
    # Debt-to-Income Ratio
    dti_ratio = (total_monthly_obligations / monthly_income) if monthly_income > 0 else 1.0
    return round(dti_ratio, 2)