document.addEventListener('DOMContentLoaded', function() {
  const addBillForm = document.getElementById('addBillForm');
  const addPublishForm = document.getElementById('addPublishForm');
  const alertContainer = document.getElementById('alertContainer');

  // Load recent bills on page load
  loadRecentBills();

  function showAlert(message, type = 'success') {
    const alert = document.createElement('div');
    alert.className = `alert alert-${type} alert-dismissible fade show`;
    alert.innerHTML = `
      ${message}
      <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    alertContainer.appendChild(alert);
    
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
      alert.remove();
    }, 5000);
    
    // Scroll to top to see alert
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  async function loadRecentBills() {
    try {
      const res = await fetch('/api/bills');
      if (!res.ok) throw new Error('Failed to load bills');
      const bills = await res.json();
      
      const recentBills = bills.slice(-5).reverse(); // Last 5 bills, newest first
      const container = document.getElementById('recentBills');
      
      if (recentBills.length === 0) {
        container.innerHTML = '<div class="text-muted">No bills yet.</div>';
        return;
      }
      
      container.innerHTML = recentBills.map(bill => `
        <div class="card mb-2">
          <div class="card-body">
            <h6 class="card-title">${bill.title}</h6>
            <p class="card-text"><small class="text-muted">${bill.id} • ${bill.category}</small></p>
            <p class="card-text">${bill.description}</p>
          </div>
        </div>
      `).join('');
    } catch (err) {
      document.getElementById('recentBills').innerHTML = 
        '<div class="text-danger">Error loading bills: ' + err.message + '</div>';
    }
  }

  if (addBillForm) {
    addBillForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const title = document.getElementById('billTitle').value.trim();
      const description = document.getElementById('billDescription').value.trim();
      const category = document.getElementById('billCategory').value.trim() || 'General';
      
      if (!title || !description) {
        showAlert('Title and description are required!', 'warning');
        return;
      }
      
      const submitBtn = e.target.querySelector('button[type="submit"]');
      submitBtn.disabled = true;
      submitBtn.textContent = 'Adding...';
      
      try {
        const res = await fetch('/api/bills', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({title, description, category})
        });
        const data = await res.json();
        
        if (res.ok) {
          showAlert(`✅ Bill added successfully! ID: ${data.id}`, 'success');
          // Clear form
          addBillForm.reset();
          // Reload recent bills
          await loadRecentBills();
        } else {
          showAlert(`❌ Error: ${data.error || 'Failed to add bill'}`, 'danger');
        }
      } catch (err) {
        showAlert(`❌ Error: ${err.message}`, 'danger');
      } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = 'Add Bill';
      }
    });
  }

  if (addPublishForm) {
    addPublishForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const title = document.getElementById('pubTitle').value.trim();
      const content = document.getElementById('pubContent').value.trim();
      const type = document.getElementById('pubType').value;
      
      if (!title || !content) {
        showAlert('Title and content are required!', 'warning');
        return;
      }
      
      const submitBtn = e.target.querySelector('button[type="submit"]');
      submitBtn.disabled = true;
      submitBtn.textContent = 'Publishing...';
      
      try {
        const res = await fetch('/api/publishes', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({title, content, type})
        });
        const data = await res.json();
        
        if (res.ok) {
          showAlert(`✅ ${type} published successfully! You can view it in the Publishes page.`, 'success');
          // Clear form
          addPublishForm.reset();
          // Reload page to show new publish
          setTimeout(() => location.reload(), 2000);
        } else {
          showAlert(`❌ Error: ${data.error || 'Failed to publish'}`, 'danger');
          submitBtn.disabled = false;
          submitBtn.textContent = 'Publish';
        }
      } catch (err) {
        showAlert(`❌ Error: ${err.message}`, 'danger');
        submitBtn.disabled = false;
        submitBtn.textContent = 'Publish';
      }
    });
  }
});
