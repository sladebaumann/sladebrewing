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
    loadNews();
});

// Load and display beers from beers.json or embedded data
async function loadBeers() {
    let beers;
    
    // Check for embedded data first (for local file access)
    if (typeof beersData !== 'undefined') {
        console.log('Using embedded beer data');
        beers = beersData;
    } else {
        // Try to fetch from beers.json (for server environments)
        try {
            console.log('Attempting to load beers.json...');
            let response = await fetch('./beers.json');
            
            if (response.ok) {
                beers = await response.json();
                console.log('Beers loaded from beers.json');
            } else {
                throw new Error('beers.json not found');
            }
        } catch (fetchError) {
            // Try API endpoint as fallback
            try {
                console.log('beers.json failed, trying API endpoint...');
                const response = await fetch('/api/beers');
                if (response.ok) {
                    const data = await response.json();
                    beers = data.beers;
                    console.log('Beers loaded from API');
                } else {
                    throw new Error('API not available');
                }
            } catch (apiError) {
                console.error('Could not load beers:', apiError);
                return;
            }
        }
    }
    
    try {
        // Convert to array and sort by currently available first, then by release date (newest first)
        const beerArray = Object.entries(beers)
            .map(([name, data]) => ({ name, ...data }))
            .sort((a, b) => {
                // First sort by currentlyAvailable (available first)
                if (a.currentlyAvailable !== b.currentlyAvailable) {
                    return b.currentlyAvailable ? 1 : -1;
                }
                // Then sort by release date (newest first)
                const dateA = new Date(a.releaseDate);
                const dateB = new Date(b.releaseDate);
                return dateB - dateA;
            });

        console.log('Beer array:', beerArray);

        // Check which page we're on and render accordingly
        const homepageContainer = document.getElementById('beer-container');
        const currentBeersContainer = document.getElementById('current-beers-container');
        const pastBeersContainer = document.getElementById('past-beers-container');
        
        console.log('Homepage container:', homepageContainer);
        console.log('Current beers container:', currentBeersContainer);
        console.log('Past beers container:', pastBeersContainer);
        
        // Homepage: show all beers
        if (homepageContainer) {
            console.log('Rendering beers for homepage');
            homepageContainer.innerHTML = '';
            beerArray.forEach(beer => {
                const card = createBeerCard(beer);
                homepageContainer.appendChild(card);
            });
            
            // Set featured beer (most recent one that's currently available)
            const availableBeers = beerArray.filter(b => b.currentlyAvailable);
            if (availableBeers.length > 0) {
                populateFeaturedBeer(availableBeers[0]);
            }
        }
        
        // Beers page: split into current and past
        if (currentBeersContainer && pastBeersContainer) {
            console.log('Rendering beers for beers page');
            const currentBeers = beerArray.filter(b => b.currentlyAvailable);
            const pastBeers = beerArray.filter(b => !b.currentlyAvailable);
            
            currentBeersContainer.innerHTML = '';
            pastBeersContainer.innerHTML = '';
            
            if (currentBeers.length === 0) {
                currentBeersContainer.innerHTML = '<p class="no-beers">No current beers available.</p>';
            } else {
                currentBeers.forEach(beer => {
                    const card = createBeerCard(beer);
                    currentBeersContainer.appendChild(card);
                });
            }
            
            if (pastBeers.length === 0) {
                pastBeersContainer.innerHTML = '<p class="no-beers">No past beers yet.</p>';
            } else {
                pastBeers.forEach(beer => {
                    const card = createBeerCard(beer);
                    pastBeersContainer.appendChild(card);
                });
            }
        }
        
        console.log('Beers rendered successfully');
    } catch (error) {
        console.error('Error loading beers:', error);
        const container = document.getElementById('beer-container') || document.getElementById('current-beers-container');
        if (container) {
            container.innerHTML = '<p style="text-align: center; color: #5a9fb5; padding: 2rem;">Unable to load beers. Please check your browser console for details.</p>';
        }
    }
}

// Populate featured beer section
function populateFeaturedBeer(beer) {
    const dateObj = new Date(beer.releaseDate);
    const monthYear = dateObj.toLocaleDateString('en-US', { month: 'short', year: 'numeric' });

    document.getElementById('featured-beer-name').textContent = beer.name;
    document.getElementById('featured-beer-desc').textContent = beer.description;
    document.getElementById('featured-beer-style').textContent = beer.style;
    document.getElementById('featured-beer-abv').textContent = beer.abv + '%';
    document.getElementById('featured-beer-ibu').textContent = beer.ibu;
    document.getElementById('featured-beer-date').textContent = monthYear;
    document.getElementById('featured-beer-img').src = beer.logo;
    document.getElementById('featured-beer-img').alt = beer.name;
    
    // Add rating if available from enriched data
    const ratingContainer = document.getElementById('featured-beer-rating-container');
    const ratingEl = document.getElementById('featured-beer-rating');
    if (ratingContainer && ratingEl && beer.rating) {
        ratingEl.textContent = `★ ${beer.rating.toFixed(2)} (${beer.ratingCount} ratings)`;
        ratingContainer.style.display = 'block';
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

    // Beer links and enriched data
    const linksEl = document.createElement('div');
    linksEl.className = 'beer-links';

    // Add enriched data from Untappd (ratings, checkins)
    if (beer.rating) {
        const ratingEl = document.createElement('div');
        ratingEl.className = 'beer-rating';
        ratingEl.innerHTML = `
            <span class="rating-stars">★ ${beer.rating.toFixed(2)}</span>
            <span class="rating-count">${beer.ratingCount} ratings</span>
        `;
        linksEl.appendChild(ratingEl);
    }

    if (beer.totalCheckins) {
        const checkinsEl = document.createElement('div');
        checkinsEl.className = 'beer-checkins';
        checkinsEl.innerHTML = `
            <span class="checkins-count">${beer.totalCheckins}</span>
            <span class="checkins-label">check-ins</span>
        `;
        linksEl.appendChild(checkinsEl);
    }

    if (beer.untappd) {
        const untappdLink = document.createElement('a');
        untappdLink.href = beer.untappd;
        untappdLink.target = '_blank';
        untappdLink.rel = 'noopener noreferrer';
        untappdLink.textContent = 'View on Untappd';
        untappdLink.className = 'untappd-link';
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

// Load and display news
async function loadNews() {
    try {
        let news;
        
        try {
            const response = await fetch('./news.json');
            if (response.ok) {
                news = await response.json();
            } else {
                throw new Error('news.json not found');
            }
        } catch (fetchError) {
            // Try API endpoint as fallback
            try {
                const response = await fetch('/api/news');
                if (response.ok) {
                    news = await response.json();
                } else {
                    throw new Error('API not available');
                }
            } catch (apiError) {
                if (typeof newsData !== 'undefined') {
                    news = newsData;
                } else {
                    throw new Error('No news data available');
                }
            }
        }

        const latestContainer = document.getElementById('latest-news-container');
        const allNewsContainer = document.getElementById('all-news-container');

        // Convert to array and sort by date (newest first)
        const newsArray = Object.entries(news)
            .map(([id, data]) => ({ id, ...data }))
            .sort((a, b) => new Date(b.date) - new Date(a.date));

        // Render latest news on homepage
        if (latestContainer && newsArray.length > 0) {
            const latestNews = newsArray[0];
            latestContainer.innerHTML = '';
            latestContainer.appendChild(createNewsCard(latestNews, false));
        }

        // Render all news on news page
        if (allNewsContainer) {
            allNewsContainer.innerHTML = '';
            newsArray.forEach(newsItem => {
                allNewsContainer.appendChild(createNewsCard(newsItem, true));
            });
        }
    } catch (error) {
        console.error('Error loading news:', error);
    }
}

// Create a news card element
function createNewsCard(newsItem, showFullContent = false) {
    const card = document.createElement('article');
    card.className = 'news-item';

    const dateObj = new Date(newsItem.date);
    const formattedDate = dateObj.toLocaleDateString('en-US', { 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric' 
    });

    let content = '';
    if (showFullContent && newsItem.content) {
        content = `<p>${newsItem.content}</p>`;
    } else if (newsItem.summary) {
        content = `<p>${newsItem.summary}</p>`;
    }

    const imageHtml = newsItem.image ? `<img src="${newsItem.image}" alt="${newsItem.title}" class="news-image">` : '';

    card.innerHTML = `
        <header class="news-item-header">
            <span class="news-date">${formattedDate}</span>
            <h3>${newsItem.title}</h3>
        </header>
        ${imageHtml}
        ${content}
        ${!showFullContent ? '<a href="/news" class="btn btn-secondary">View All News</a>' : ''}
    `;

    return card;
}
