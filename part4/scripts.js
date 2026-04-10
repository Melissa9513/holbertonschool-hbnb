document.addEventListener('DOMContentLoaded', () => {
    setupLogin();
    checkAuthentication();

    const filter = document.getElementById('price-filter');
    if (filter) {
        filter.addEventListener('change', filterPlaces);
    }
});

let allPlaces = [];

/* ================= LOGIN ================= */

function setupLogin() {
    const form = document.getElementById('login-form');
    const errorMessage = document.getElementById('error-message');

    if (form) {
        form.addEventListener('submit', async (event) => {
            event.preventDefault();

            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            try {
                await loginUser(email, password);
            } catch (error) {
                errorMessage.textContent = error.message;
            }
        });
    }
}

async function loginUser(email, password) {
    const response = await fetch('http://127.0.0.1:5000/api/v1/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
    });

    if (response.ok) {
        const data = await response.json();

        document.cookie = `token=${data.access_token}; path=/`;

        window.location.href = 'index.html';
    } else {
        throw new Error('Invalid credentials');
    }
}

/* ================= AUTH ================= */

function checkAuthentication() {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');

    if (!loginLink) return;

    if (!token) {
        loginLink.style.display = 'block';
    } else {
        loginLink.style.display = 'none';
        fetchPlaces(token);
    }
}

function getCookie(name) {
    const cookies = document.cookie.split('; ');
    for (let cookie of cookies) {
        const [key, value] = cookie.split('=');
        if (key === name) return value;
    }
    return null;
}

/* ================= PLACES ================= */

async function fetchPlaces(token) {
    try {
        const response = await fetch('http://127.0.0.1:5000/api/v1/places', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        const data = await response.json();
        allPlaces = data;

        displayPlaces(allPlaces);
    } catch (error) {
        console.error(error);
    }
}

function displayPlaces(places) {
    const container = document.getElementById('places-list');
    if (!container) return;

    container.innerHTML = '';

    places.forEach(place => {
        const card = document.createElement('div');
        card.className = 'place-card';

        card.innerHTML = `
            <h2>${place.name}</h2>
            <p>Price: $${place.price_per_night}</p>
            <p>${place.description || ''}</p>
            <a href="place.html?id=${place.id}" class="details-button">View Details</a>
        `;

        container.appendChild(card);
    });
}

/* ================= FILTER ================= */

function filterPlaces() {
    const value = document.getElementById('price-filter').value;

    if (value === 'all') {
        displayPlaces(allPlaces);
        return;
    }

    const filtered = allPlaces.filter(place =>
        place.price_per_night <= parseInt(value)
    );

    displayPlaces(filtered);
}
