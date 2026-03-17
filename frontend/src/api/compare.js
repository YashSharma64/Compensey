const BASE_URL = import.meta.env.VITE_API_URL || '/api';

/**
 * POST /compare
 * Compare two companies using ML + SHAP analysis
 */
export async function compareCompanies(companyA, companyB) {
  console.log('Making API call to:', `${BASE_URL}/compare`);
  console.log('Request payload:', { company_a: companyA, company_b: companyB });
  
  const response = await fetch(`${BASE_URL}/compare`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ company_a: companyA, company_b: companyB }),
  });

  console.log('Response status:', response.status);
  console.log('Response ok:', response.ok);

  if (!response.ok) {
    const errData = await response.json();
    console.error('API Error:', errData);
    throw new Error(errData.detail || 'Analysis failed. Please try again.');
  }

  const result = await response.json();
  console.log('API Success:', result);
  return result;
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
