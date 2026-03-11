// Mobile menu toggle
document.addEventListener('DOMContentLoaded', function() {
    const hamburger = document.querySelector('.hamburger');
    const navMenu = document.querySelector('.nav-menu');
    const navLinks = document.querySelectorAll('.nav-link');

    if (hamburger) {
        hamburger.addEventListener('click', function() {
            navMenu.classList.toggle('active');
            hamburger.classList.toggle('active');
        });

        // Close menu when a link is clicked
        navLinks.forEach(link => {
            link.addEventListener('click', function() {
                navMenu.classList.remove('active');
                hamburger.classList.remove('active');
            });
        });
    }

    // Load beers from JSON or embedded data
    loadBeers();
});

// Load and display beers from beers.json or embedded data
async function loadBeers() {
    try {
        let beers;
        
        // Try to fetch from beers.json first (for server environments)
        try {
            console.log('Attempting to load beers.json...');
            const response = await fetch('./beers.json');
            
            if (response.ok) {
                beers = await response.json();
                console.log('Beers loaded from beers.json');
            } else {
                throw new Error('beers.json not found');
            }
        } catch (fetchError) {
            // Fallback to embedded data (for local file access)
            console.log('Using embedded beer data (local file mode)');
            if (typeof beersData !== 'undefined') {
                beers = beersData;
            } else {
                throw new Error('No beer data available');
            }
        }
        
        const container = document.getElementById('beer-container');
        if (!container) {
            console.warn('Beer container element not found');
            return;
        }

        // Convert to array and sort by release date (newest first)
        const beerArray = Object.entries(beers)
            .map(([name, data]) => ({ name, ...data }))
            .sort((a, b) => {
                const dateA = new Date(a.releaseDate);
                const dateB = new Date(b.releaseDate);
                return dateB - dateA;
            });

        console.log('Beer array:', beerArray);

        // Clear any error messages
        container.innerHTML = '';

        // Render beers
        beerArray.forEach(beer => {
            const card = createBeerCard(beer);
            container.appendChild(card);
        });
        
        console.log('Beers rendered successfully');
    } catch (error) {
        console.error('Error loading beers:', error);
        const container = document.getElementById('beer-container');
        if (container) {
            container.innerHTML = '<p style="text-align: center; color: #d4af37; padding: 2rem;">Unable to load beers. Please check your browser console for details.</p>';
        }
    }
}

// Create a beer card element
function createBeerCard(beer) {
    const card = document.createElement('div');
    card.className = 'beer-card';

    const img = document.createElement('img');
    img.src = beer.logo;
    img.alt = `${beer.name} Label`;
    img.className = 'beer-image';
    img.onerror = function() {
        // Fallback if image doesn't exist
        this.style.display = 'none';
    };

    const info = document.createElement('div');
    info.className = 'beer-info';

    // Beer name
    const nameEl = document.createElement('h3');
    nameEl.className = 'beer-name';
    nameEl.textContent = beer.name;

    // Beer style
    const styleEl = document.createElement('p');
    styleEl.className = 'beer-style';
    styleEl.textContent = beer.style || 'Craft Beer';

    // Beer stats (ABV and IBU)
    const statsEl = document.createElement('div');
    statsEl.className = 'beer-stats';

    if (beer.abv) {
        const abvStat = document.createElement('div');
        abvStat.className = 'beer-stat';
        abvStat.innerHTML = `
            <span class="beer-stat-label">ABV</span>
            <span class="beer-stat-value">${beer.abv}%</span>
        `;
        statsEl.appendChild(abvStat);
    }

    if (beer.ibu) {
        const ibuStat = document.createElement('div');
        ibuStat.className = 'beer-stat';
        ibuStat.innerHTML = `
            <span class="beer-stat-label">IBU</span>
            <span class="beer-stat-value">${beer.ibu}</span>
        `;
        statsEl.appendChild(ibuStat);
    }

    // Beer description
    const descEl = document.createElement('p');
    descEl.className = 'beer-description';
    descEl.textContent = beer.description;

    // Beer links
    const linksEl = document.createElement('div');
    linksEl.className = 'beer-links';

    if (beer.untappd) {
        const untappdLink = document.createElement('a');
        untappdLink.href = beer.untappd;
        untappdLink.target = '_blank';
        untappdLink.rel = 'noopener noreferrer';
        untappdLink.textContent = 'View on Untappd';
        linksEl.appendChild(untappdLink);
    }

    // Assemble the card
    info.appendChild(nameEl);
    info.appendChild(styleEl);
    if (statsEl.children.length > 0) {
        info.appendChild(statsEl);
    }
    info.appendChild(descEl);
    if (linksEl.children.length > 0) {
        info.appendChild(linksEl);
    }

    card.appendChild(img);
    card.appendChild(info);

    return card;
}
