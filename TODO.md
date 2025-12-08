# TODOs

## Make beers.json better and utilize that in the body of the main page to have a list of beers that are available (and a section for retired beers too)
1. Enhance beers.json to include abv, style, featured flag, date released, currently available flag
```
{
  "Doe Brand": {
    "description": "A dark amber ale with rich malty notes and a smooth finish. Brewed with a touch of caramel malt for depth and balance.",
    "logo": "images/doe-brand-label.png",
    "untappd": "https://untappd.com/b/slade-brewing-doe-brand/6483546",
    "abv": "6.2%",
    "style": "Amber Ale",
    "releaseDate": "2025-12-01",
    "currentlyAvailable": true,
    "featured": true
  },
  "Fallow Pale Ale": {
    "description": "A crisp, hoppy pale ale with citrus notes and a refreshing finish. Perfect for a sunny afternoon.",
    "logo": "images/fallow-pale-ale.png",
    "untappd": "https://untappd.com/b/slade-brewing-fallow-pale-ale/1234567",
    "abv": "5.4%",
    "style": "Pale Ale",
    "releaseDate": "2025-11-15",
    "currentlyAvailable": true,
    "featured": false
  },
  "Other Beer": {
    "description": "An experimental beer with tropical fruit aroma and light body.",
    "logo": "images/other-beer.png",
    "untappd": "https://untappd.com/b/slade-brewing-other-beer/2345678",
    "abv": "5.8%",
    "style": "IPA",
    "releaseDate": "2025-10-30",
    "currentlyAvailable": true,
    "featured": false
  }
}
```
2. Use the beers.json for displaying images and everything nicely (copied from a bot, needs work)
```
<div id="featured-beer"></div>
<div id="beer-container"></div>
```
3. Javascript to render the beer cards
```
<script>
async function loadBeers() {
  const res = await fetch('beers.json');
  const beers = await res.json();

  const featuredContainer = document.getElementById('featured-beer');
  const container = document.getElementById('beer-container');

  // Convert JSON to array for sorting
  const beerArray = Object.entries(beers).map(([name, info]) => ({name, ...info}));

  // Separate featured beer
  const featuredBeer = beerArray.find(b => b.featured) || null;
  const otherBeers = beerArray
    .filter(b => !b.featured)
    .sort((a, b) => new Date(b.releaseDate) - new Date(a.releaseDate));

  // Render featured beer
  if (featuredBeer) {
    const card = document.createElement('div');
    card.className = 'beer-card featured';
    card.innerHTML = `
      <img src="${featuredBeer.logo}" alt="${featuredBeer.name} Logo" class="beer-logo"/>
      <h2>${featuredBeer.name}</h2>
      <p>${featuredBeer.description}</p>
      ${featuredBeer.style ? `<p><strong>Style:</strong> ${featuredBeer.style}</p>` : ''}
      ${featuredBeer.abv ? `<p><strong>ABV:</strong> ${featuredBeer.abv}</p>` : ''}
      ${featuredBeer.untappd ? `<a href="${featuredBeer.untappd}" target="_blank">View on Untappd</a>` : ''}
    `;
    featuredContainer.appendChild(card);
  }

  // Render other beers
  otherBeers.forEach(beer => {
    const card = document.createElement('div');
    card.className = 'beer-card';
    card.innerHTML = `
      <img src="${beer.logo}" alt="${beer.name} Logo" class="beer-logo"/>
      <h2>${beer.name}</h2>
      <p>${beer.description}</p>
      ${beer.style ? `<p><strong>Style:</strong> ${beer.style}</p>` : ''}
      ${beer.abv ? `<p><strong>ABV:</strong> ${beer.abv}</p>` : ''}
      ${beer.untappd ? `<a href="${beer.untappd}" target="_blank">View on Untappd</a>` : ''}
    `;
    container.appendChild(card);
  });
}

loadBeers();
</script>
```
4. CSS for display of beers.json (needs work but is technically scalable for mobile - validate)
```
/* Featured Beer */
.beer-card.featured {
  width: 100%;
  max-width: 700px;
  margin: 2rem auto;
  border: 2px solid #0077cc;
  box-shadow: 0 4px 12px rgba(0,0,0,0.2);
  background-color: #fefefe;
  padding: 1.5rem;
  text-align: center;
}

/* General Beer Card */
.beer-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 1rem;
  text-align: center;
  box-shadow: 0 2px 6px rgba(0,0,0,0.1);
  transition: transform 0.2s;
}

.beer-card:hover {
  transform: translateY(-4px);
}

.beer-logo {
  max-width: 100%;
  height: auto;
  margin-bottom: 0.5rem;
}

.beer-card a {
  display: inline-block;
  margin-top: 0.5rem;
  text-decoration: none;
  color: #0077cc;
}

.beer-card p {
  margin: 0.3rem 0;
}

/* Grid Layout for Other Beers */
.beer-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1.5rem;
  padding: 1rem;
  justify-items: center;
}

/* Responsive tweaks */
@media (max-width: 600px) {
  .beer-card {
    width: 100%;
  }
}
```
5. Somehow use the descriptions from beers.json and maybe even the image to update untappd if that is something you can do without the API?
