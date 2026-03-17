const BASE_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';

/**
 * POST /compare
 * Compare two companies using ML + SHAP analysis
 */
export async function compareCompanies(companyA, companyB) {
  const response = await fetch(`${BASE_URL}/compare`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ company_a: companyA, company_b: companyB }),
  });

  if (!response.ok) {
    const errData = await response.json();
    throw new Error(errData.detail || 'Analysis failed. Please try again.');
  }

  return response.json();
}

/**
 * POST /strategy
 * Get AI strategic outlook via Gemini
 */
export async function getStrategy(companyA, companyB) {
  const response = await fetch(`${BASE_URL}/strategy`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ company_a: companyA, company_b: companyB }),
  });

  if (!response.ok) {
    const errData = await response.json();
    throw new Error(errData.detail || 'Strategy fetch failed. Please try again.');
  }

  return response.json();
}
