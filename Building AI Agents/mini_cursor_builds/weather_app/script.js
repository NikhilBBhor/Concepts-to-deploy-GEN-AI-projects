async function getWeather() {
    const city = document.getElementById("city-dropdown").value;
    if (!city) return;
    // For now, simulate a weather API response
    const weatherData = await mockWeatherAPI(city);
    document.getElementById("weather-details").innerText = `Weather in ${city}: ${weatherData}`;
}

async function mockWeatherAPI(city) {
    // Simulated API response based on city
    const weatherResponses = {
        "New York": "Sunny, 25°C",
        "London": "Cloudy, 18°C",
        "Paris": "Rainy, 14°C",
        "Tokyo": "Windy, 22°C",
        "Sydney": "Clear, 29°C"
    };
    return weatherResponses[city];
}
