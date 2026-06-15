// web/static/search.js
let fuse = null;
let allData = [];

async function initSearch() {
  const resp = await fetch('/search-index.json');
  allData = await resp.json();
  fuse = new Fuse(allData, {
    keys: [
      { name: 'title', weight: 3 },
      { name: 'section', weight: 2 },
      { name: 'author', weight: 2 },
      { name: 'games', weight: 2 },
      { name: 'snippet', weight: 1 },
    ],
    threshold: 0.3,
    includeMatches: true,
  });

  const input = document.getElementById('search-input');
  const params = new URLSearchParams(window.location.search);
  if (params.get('q')) {
    input.value = params.get('q');
    doSearch(params.get('q'));
  }
  input.addEventListener('input', (e) => doSearch(e.target.value));
}

function doSearch(query) {
  const results = document.getElementById('search-results');
  if (!query.trim()) {
    results.innerHTML = '';
    return;
  }
  const hits = fuse.search(query, { limit: 20 });
  results.innerHTML = hits.map(({ item }) => `
    <a href="${item.url}" class="search-result">
      <div class="search-result-title">${item.title}</div>
      <div class="search-result-meta">
        ${item.issue} · ${item.section}${item.author ? ' · ● ' + item.author : ''}
      </div>
      <div class="search-result-snippet">${item.snippet}</div>
    </a>
  `).join('');
  if (hits.length === 0) {
    results.innerHTML = '<div class="search-empty">未找到匹配结果</div>';
  }
}

document.addEventListener('DOMContentLoaded', initSearch);
