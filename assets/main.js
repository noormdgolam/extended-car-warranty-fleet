document.addEventListener('DOMContentLoaded', () => {
    // Search Functionality
    const searchInput = document.getElementById('searchInput');
    const searchResults = document.getElementById('searchResults');

    if (searchInput && searchResults) {
        // Load index if not already present
        if (!window.searchIndex) {
            const script = document.createElement('script');
            script.src = '/assets/search_index.js';
            script.onload = initSearch;
            document.body.appendChild(script);
        } else {
            initSearch();
        }

        function initSearch() {
            searchInput.addEventListener('input', (e) => {
                const query = e.target.value.toLowerCase().trim();
                searchResults.innerHTML = '';
                
                if (query.length < 2) return;

                const results = window.searchIndex.filter(item => 
                    item.title.toLowerCase().includes(query) || 
                    item.content.toLowerCase().includes(query)
                ).slice(0, 10); // Limit to 10 results

                if (results.length === 0) {
                    searchResults.innerHTML = '<p>No guides found matching your query.</p>';
                    return;
                }

                results.forEach(item => {
                    const div = document.createElement('div');
                    div.className = 'search-result-item';
                    div.innerHTML = `
                        <h3><a href="${item.url}">${item.title}</a></h3>
                        <p>${item.content.substring(0, 150)}...</p>
                    `;
                    searchResults.appendChild(div);
                });
            });
        }
    }
});
