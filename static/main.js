document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('form');
  if (!form) return;
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const hash = document.getElementById('hash').value.trim();
    const algo = document.getElementById('algo').value;
    const res = await fetch('/api/v1/crack', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ hash, algo, mode: 'sync', wordlist: 'dico.txt' })
    });
    const data = await res.json();
    document.getElementById('result').textContent = JSON.stringify(data, null, 2);
  });
});
