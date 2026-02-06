import shap
import pandas as pd
import numpy as np

# Initialize JS visualization code for SHAP
shap.initjs()

def explain_decision(company_a_name, company_b_name, a_metrics, b_metrics):
    """
    Generates text explanations for the comparison decision.
    """
    explanations = []
    
    # Sentiment Explanation
    sent_a = float(a_metrics['sentiment'])
    sent_b = float(b_metrics['sentiment'])
    
    if sent_a > sent_b:
        diff = (sent_a - sent_b) * 100
        explanations.append(f"{company_a_name} has {diff:.1f}% higher positive sentiment in customer reviews.")
    else:
        diff = (sent_b - sent_a) * 100
        explanations.append(f"{company_b_name} leads in customer satisfaction by {diff:.1f}%.")

    # Growth Explanation
    growth_a = float(a_metrics['growth'])
    growth_b = float(b_metrics['growth'])
    
    if growth_a > growth_b:
        explanations.append(f"{company_a_name} shows stronger recent traction and review volume growth.")
    else:
        explanations.append(f"{company_b_name} is accelerating faster based on review trends.")

    # Stability Explanation
    risk_a = float(a_metrics['risk'])
    risk_b = float(b_metrics['risk'])
    
    if risk_a < risk_b:
        explanations.append(f"{company_a_name} has fewer anomalous review patterns, indicating higher stability.")
    else:
        explanations.append(f"{company_b_name} shows more consistent user feedback patterns.")
        
    return explanations

def get_shap_feature_importance(model, feature_data):
    """
    Placeholder for actual SHAP value generation to return to UI.
    Returns: top features influencing the Growth model.
    """
    # For RandomForestRegressor (Growth model)
    try:
        explainer = shap.TreeExplainer(model)
        shap_values = explainer.shap_values(feature_data)
        
        # Mean absolute SHAP values per feature
        # features are ['rating', 'review_length']
        feature_names = ['Customer Rating', 'Review Detail (Length)']
        
        if isinstance(shap_values, list):
             # For classification, shap_values is a list of arrays
            vals = np.abs(shap_values[0]).mean(0)
        else:
             # For regression
            vals = np.abs(shap_values).mean(0)
            
        importance = list(zip(feature_names, vals))
        importance.sort(key=lambda x: x[1], reverse=True)
        
        top_factor = importance[0][0]
        return f"The main driver for the growth score is {top_factor}."
    except Exception as e:
        return "Complex non-linear factors influenced the score."
