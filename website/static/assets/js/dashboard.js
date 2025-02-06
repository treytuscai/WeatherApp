function fetchWeatherData(city, country) {
    // Construct the URL for the API request
    const url = `/weather?city=${city}&country=${country}`;

    // Fetch weather data from the backend
    fetch(url)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                console.error('Error:', data.error);
                return;
            }

            const currentTime = new Date();
            const hours = currentTime.getHours();
            const minutes = currentTime.getMinutes();
            const formattedTime = `${hours % 12 || 12}:${minutes < 10 ? '0' : ''}${minutes} ${hours >= 12 ? 'PM' : 'AM'}`;

            document.getElementById('weather-time').textContent = formattedTime;

            // Update the weather UI with the data
            const weather = data;

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

            const iconUrl = `https://openweathermap.org/img/wn/${data.icon}.png`;
            document.getElementById('weather-icon').src = iconUrl;
        })
        .catch(error => {
            console.error('Error fetching weather data:', error);
            displayError("An unexpected error occurred while fetching weather data.");
        });
}

function displayError(message) {
    const errorSection = document.getElementById('weather-error');
    const errorMessage = document.getElementById('error-message');
    errorMessage.textContent = message;
    errorSection.style.display = 'block';
}

window.addEventListener('DOMContentLoaded', () => {
    fetchWeatherData('Waterville', 'US');
});

const cityForm = document.getElementById('cityForm');

cityForm.addEventListener('submit', function (event) {
    event.preventDefault(); 
    const city = document.getElementById('cityInput').value;
    const country = document.getElementById('countryInput').value;
    fetchWeatherData(city, country);
});