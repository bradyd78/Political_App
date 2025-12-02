document.addEventListener('DOMContentLoaded', function() {
  const addBillForm = document.getElementById('addBillForm');
  const addPublishForm = document.getElementById('addPublishForm');

  if (addBillForm) {
    addBillForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const title = document.getElementById('billTitle').value.trim();
      const description = document.getElementById('billDescription').value.trim();
      const category = document.getElementById('billCategory').value.trim();
      if (!title || !description) return alert('Title and description required');
      const res = await fetch('/api/bills', {
        method: 'POST', headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({title, description, category})
      });
      const data = await res.json();
      if (res.ok) {
        alert('Bill added: ' + data.id);
        location.reload();
      } else {
        alert('Error: ' + (data.error || JSON.stringify(data)));
      }
    });
  }

  if (addPublishForm) {
    addPublishForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const title = document.getElementById('pubTitle').value.trim();
      const content = document.getElementById('pubContent').value.trim();
      const type = document.getElementById('pubType').value;
      if (!title || !content) return alert('Title and content required');
      const res = await fetch('/api/publishes', {
        method: 'POST', headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({title, content, type})
      });
      const data = await res.json();
      if (res.ok) {
        alert('Published: ' + data.publish.id);
        location.reload();
      } else {
        alert('Error: ' + (data.error || JSON.stringify(data)));
      }
    });
  }
});
