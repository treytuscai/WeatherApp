function fetchWeatherData(city, country) {
    // Construct the URL for the API request
    const url = `/weather?city=${city}&country=${country}`;

    // Fetch weather data from the backend
    fetch(url)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                console.error('Error:', data.error);
                displayError(data.error);
                return;
            }

            const errorSection = document.getElementById('weather-error');
            const errorMessage = document.getElementById('error-message');
            errorMessage.textContent = "";
            errorSection.style.display = 'none';

            const currentTime = new Date();
            const hours = currentTime.getHours();
            const minutes = currentTime.getMinutes();
            const formattedTime = `${hours % 12 || 12}:${minutes < 10 ? '0' : ''}${minutes} ${hours >= 12 ? 'PM' : 'AM'}`;

            document.getElementById('weather-time').textContent = formattedTime;

            // Update the weather UI with the data
            const weather = data;
            console.log(data)

            // Update temperature
            document.getElementById('temperature').textContent = `${weather.temperature}°C`;
            document.getElementById('weather-description').textContent = weather.description;
            document.getElementById('detailed-description').textContent = `${weather.detailed_description}.`
            document.getElementById('feels-like').textContent = `Feels like: ${weather.feels_like}°C`;
            document.getElementById('wind-speed').textContent = `${weather.wind_speed} km/h`;
            document.getElementById('humidity').textContent = `${weather.humidity}%`;
            document.getElementById('visibility').textContent = `${weather.visibility / 1000} km`;
            document.getElementById('pressure').textContent = `${weather.pressure} mb`;
            document.getElementById('dew-point').textContent = `${weather.dew_point}°C`;

            let locationText = `${city}, ${country}`;
            document.getElementById("cityDropdown").innerHTML = `${locationText} <i class="bi bi-caret-down-fill"></i>`;

            const iconUrl = `https://openweathermap.org/img/wn/${data.icon}.png`;
            document.getElementById("weather-icon").src = iconUrl;

            document.getElementById('name').textContent = `${city}, ${country}`
            document.getElementById('latitude').textContent = weather.latitude
            document.getElementById('longitude').textContent = weather.longitude
            document.getElementById('uvi').textContent = `${weather.uvi}`
            document.getElementById('clouds').textContent = `${weather.clouds}%`
            updateMap(weather.latitude, weather.longitude);
        })
        .catch(error => {
            console.error('Error fetching weather data:', error);
        });
}

// Convert the country code to uppercase 
document.getElementById('countryInput').addEventListener('input', function () {
    this.value = this.value.toUpperCase();
});

function toTitleCase(str) {
    return str.replace(/\w\S*/g, function (txt) {
        return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
    });
}

// Update the city to title case
document.getElementById('cityInput').addEventListener('input', function () {
    this.value = toTitleCase(this.value);
});

// Update Leaflet map with new lat/lon
function updateMap(lat, lon) {
    map.setView([lat, lon], 10); // Adjust zoom level

    // Remove existing marker (if any)
    if (window.weatherMarker) {
        map.removeLayer(window.weatherMarker);
    }

    // Add a new marker for the location
    window.weatherMarker = L.marker([lat, lon]).addTo(map)
}


function displayError(message) {
    const errorSection = document.getElementById('weather-error');
    const errorMessage = document.getElementById('error-message');
    errorMessage.textContent = message;
    errorSection.style.display = 'block';
}

// Function to initialize and rotate the Weather Fun Facts
function initWeatherFunFacts() {
    const factElement = document.getElementById('weatherFact');
    if (!factElement) return; // If the element is not found, exit.

    const facts = [
        "A single bolt of lightning can contain up to one billion volts of electricity!",
        "Raindrops can fall at speeds of up to 22 miles per hour.",
        "Snowflakes are unique; no two are exactly alike.",
        "The highest temperature ever recorded on Earth was 134°F (56.7°C).",
        "Lightning strikes the Earth 100 times every second."
    ];

    let currentIndex = 0;
    // Ensure a smooth fade transition is applied
    factElement.style.transition = "opacity 0.5s ease-in-out";

    setInterval(() => {
        // Fade out the current fact
        factElement.style.opacity = 0;
        // After the fade-out transition, update the text and fade back in
        setTimeout(() => {
            currentIndex = (currentIndex + 1) % facts.length;
            factElement.textContent = facts[currentIndex];
            factElement.style.opacity = 1;
        }, 500);
    }, 5000);
}

window.addEventListener('DOMContentLoaded', () => {
    fetchWeatherData('Waterville', 'US');
    particlesJS('particles-js', {
        particles: {
            number: { value: 50 },
            size: { value: 3 },
            move: { speed: 1, direction: "none" },
        }
    });
    initWeatherFunFacts();
});

const cityForm = document.getElementById('cityForm');

cityForm.addEventListener('submit', function (event) {
    event.preventDefault();
    const city = document.getElementById('cityInput').value;
    const country = document.getElementById('countryInput').value;
    fetchWeatherData(city, country);
});