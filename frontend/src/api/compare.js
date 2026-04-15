const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// Warmup ping - call on page load to wake up cold server
export async function warmupBackend() {
  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 90000); // 90s timeout
    
    await fetch(`${BASE_URL}/`, { 
      method: 'GET',
      signal: controller.signal 
    });
    clearTimeout(timeoutId);
    console.log('Backend warmed up');
  } catch (e) {
    console.log('Warmup ping sent (server waking up)');
  }
}

export async function compareCompanies(companyA, companyB, onProgress) {
  const response = await fetch(`${BASE_URL}/compare`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'Accept': 'text/event-stream' },
    body: JSON.stringify({ company_a: companyA, company_b: companyB }),
  });

  if (!response.ok) {
    let errMsg = 'Analysis failed. Please try again.';
    try {
      const errData = await response.json();
      errMsg = errData.detail || errMsg;
    } catch (e) {}
    throw new Error(errMsg);
  }

  const reader = response.body.getReader();
  const decoder = new TextDecoder("utf-8");
  let buffer = '';
  let result = null;

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    
    buffer += decoder.decode(value, { stream: true });
    
    let boundary = buffer.indexOf('\n\n');
    while (boundary !== -1) {
      const message = buffer.slice(0, boundary);
      buffer = buffer.slice(boundary + 2);
      
      const lines = message.split('\n');
      for (let line of lines) {
        if (line.startsWith('data: ')) {
          try {
            const data = JSON.parse(line.slice(6));
            if (data.error) {
              throw new Error(data.error);
            }
            if (data.stage === 'complete') {
              result = data.result;
            } else if (onProgress) {
              onProgress(data);
            }
          } catch (e) {
            if (e.name !== 'SyntaxError') throw e;
          }
        }
      }
      boundary = buffer.indexOf('\n\n');
    }
  }

  if (!result) throw new Error('Stream finished without returning results.');
  return result;
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
