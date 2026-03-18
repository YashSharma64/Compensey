const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

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

export async function getStrategy(companyA, companyB, metricsA, metricsB, question, drivers) {
  const response = await fetch(`${BASE_URL}/strategy`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      company_a: companyA, company_b: companyB,
      metrics_a: metricsA, metrics_b: metricsB,
      question, drivers
    }),
  });

  if (!response.ok) {
    const errData = await response.json();
    throw new Error(errData.detail || 'Strategy fetch failed. Please try again.');
  }

  return response.json();
}
