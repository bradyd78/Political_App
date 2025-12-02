document.addEventListener('DOMContentLoaded', function() {
  const list = document.getElementById('publishesList');
  const search = document.getElementById('pubSearch');
  const typeSel = document.getElementById('pubType');
  const reloadBtn = document.getElementById('reloadPublishes');
  const view = document.getElementById('publishView');
  const titleEl = document.getElementById('publishTitle');
  const metaEl = document.getElementById('publishMeta');
  const contentEl = document.getElementById('publishContent');
  const closeBtn = document.getElementById('closePublish');

  let publishes = [];

  async function loadPublishes() {
    list.innerHTML = 'Loading...';
    const q = encodeURIComponent(search.value || '');
    const type = encodeURIComponent(typeSel.value || '');
    try {
      const res = await fetch(`/api/publishes?q=${q}&type=${type}`);
      if (!res.ok) throw new Error('Server error ' + res.status);
      publishes = await res.json();
      renderList();
    } catch (err) {
      list.innerHTML = `<div class="text-danger">${err.message}</div>`;
    }
  }

  function renderList() {
    if (!publishes.length) {
      list.innerHTML = '<div class="text-muted">No publishes found.</div>';
      return;
    }
    list.innerHTML = '';
    publishes.forEach(p => {
      const item = document.createElement('div');
      item.className = 'list-group-item d-flex justify-content-between align-items-start';
      item.innerHTML = `<div><h5 class="mb-1">${p.title}</h5><small class="text-secondary">${p.type} • ${p.timestamp}</small></div><div><button class="btn btn-link btn-sm">Read</button></div>`;
      item.querySelector('button').addEventListener('click', () => showPublish(p.id));
      list.appendChild(item);
    });
  }

  async function showPublish(id) {
    try {
      const res = await fetch(`/api/publishes/${id}`);
      if (!res.ok) throw new Error('Not found');
      const p = await res.json();
      titleEl.textContent = p.title;
      metaEl.textContent = `${p.type} • ${p.timestamp}`;
      contentEl.textContent = p.content;
      view.classList.remove('d-none');
      window.scrollTo({ top: 0, behavior: 'smooth' });
    } catch (err) {
      alert('Failed to load publish: ' + err.message);
    }
  }

  closeBtn.addEventListener('click', () => view.classList.add('d-none'));
  reloadBtn.addEventListener('click', loadPublishes);
  search.addEventListener('input', loadPublishes);
  typeSel.addEventListener('change', loadPublishes);

  // initial load
  loadPublishes();
});
