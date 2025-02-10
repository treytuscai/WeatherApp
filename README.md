# WeatherApp 🌦️

Welcome to **WeatherApp**, a sleek and simple weather forecasting web application powered by the OpenWeatherMap API! Get up-to-date weather information for any city in the world with a user-friendly interface.

## 🌍 Features

- **Real-time weather updates**: Get the current temperature, weather conditions, and humidity for any city.
- **City and country validation**: Ensure the city and country inputs are alphanumeric, with the country code strictly limited to two capitalized letters.
- **Error handling**: Displays informative error messages for incorrect or missing input.
- **Lightweight and Fast**: Minimalistic design focused on delivering weather information quickly and effectively.

## ⚙️ Tech Stack

- **Flask**: Web framework for building the app.
- **OpenWeatherMap API**: To fetch real-time weather data.
- **Heroku**: To host the app and make it accessible online.
- **HTML/JS/Bootstrap**: For the website's frontend interface.

## 🚀 Getting Started

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/tvtusc25/weatherapp.git
   cd weatherapp
   ```

2. **Set up a Virtual Environment** (Optional but recommended):

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # For macOS/Linux
   venv\Scripts\activate     # For Windows
   ```

3. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up the OpenWeatherMap API Key**:

   - Go to [OpenWeatherMap](https://openweathermap.org/api) and create an account.
   - Get your **API Key** and add it to a `.env` file:
   
     ```env
     API_KEY=your_api_key_here
     ```

5. **Run the Application**:

   ```bash
   flask run
   ```

6. **Access the Web Application**:

   Visit `http://127.0.0.1:5000` in your browser to start using the app locally!

## 🌐 Live Demo

Check out the live version of **WeatherApp** hosted on Heroku:

[WeatherApp on Heroku](https://weather-appv-3d0daf77a308.herokuapp.com/)

## 🧪 Testing

The project includes unit and functional tests to ensure that everything works smoothly. You can run the tests with:

```bash
pytest
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
