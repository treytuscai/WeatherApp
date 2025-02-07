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
