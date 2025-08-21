import { WeatherData, HourlyWeather, WeatherAPIResponse } from '../types';

// OpenWeatherMap API configuration
const OPENWEATHER_API_KEY = 'YOUR_API_KEY_HERE'; // Replace with your API key
const OPENWEATHER_BASE_URL = 'https://api.openweathermap.org/data/2.5';

// Fallback weather data for demo purposes
const DEMO_WEATHER_DATA: Record<string, WeatherData> = {
  'New York': {
    location: 'New York',
    latitude: 40.7128,
    longitude: -74.0060,
    hourly: generateDemoHourlyData(40.7128, -74.0060)
  },
  'London': {
    location: 'London',
    latitude: 51.5074,
    longitude: -0.1278,
    hourly: generateDemoHourlyData(51.5074, -0.1278)
  },
  'Tokyo': {
    location: 'Tokyo',
    latitude: 35.6762,
    longitude: 139.6503,
    hourly: generateDemoHourlyData(35.6762, 139.6503)
  },
  'Sydney': {
    location: 'Sydney',
    latitude: -33.8688,
    longitude: 151.2093,
    hourly: generateDemoHourlyData(-33.8688, 151.2093)
  },
  'Beijing': {
    location: 'Beijing',
    latitude: 39.9042,
    longitude: 116.4074,
    hourly: generateDemoHourlyData(39.9042, 116.4074)
  }
};

// Generate demo hourly weather data based on latitude
function generateDemoHourlyData(lat: number, lon: number): HourlyWeather[] {
  const hourly: HourlyWeather[] = [];
  
  for (let hour = 0; hour < 24; hour++) {
    // Base solar irradiance based on latitude and time of day
    let baseIrradiance = 0;
    
    if (hour >= 6 && hour <= 18) { // Daytime hours
      const solarNoon = 12;
      const timeDiff = Math.abs(hour - solarNoon);
      const maxIrradiance = Math.max(0, 1000 - Math.abs(lat) * 2); // Higher latitude = lower irradiance
      baseIrradiance = maxIrradiance * Math.cos((timeDiff / 6) * Math.PI / 2);
    }
    
    // Add some realistic variation
    const variation = 0.2;
    const irradiance = Math.max(0, baseIrradiance * (1 + (Math.random() - 0.5) * variation));
    
    // Temperature variation (warmer during day)
    const baseTemp = 20 - Math.abs(lat) * 0.5; // Higher latitude = colder
    const tempVariation = Math.cos((hour - 6) * Math.PI / 12) * 10;
    const temperature = baseTemp + tempVariation + (Math.random() - 0.5) * 5;
    
    // Humidity (higher at night)
    const humidity = 60 + Math.cos((hour - 6) * Math.PI / 12) * 20 + (Math.random() - 0.5) * 10;
    
    // Cloud cover (random with some pattern)
    const cloudCover = Math.max(0, Math.min(100, 
      30 + Math.sin(hour * Math.PI / 12) * 20 + (Math.random() - 0.5) * 30
    ));
    
    hourly.push({
      hour,
      solarIrradiance: Math.round(irradiance),
      temperature: Math.round(temperature * 10) / 10,
      humidity: Math.round(humidity),
      cloudCover: Math.round(cloudCover)
    });
  }
  
  return hourly;
}

// Get weather data for a location
export async function getWeatherData(location: string): Promise<WeatherAPIResponse> {
  try {
    // Check if we have demo data for this location
    if (DEMO_WEATHER_DATA[location]) {
      return {
        success: true,
        data: DEMO_WEATHER_DATA[location]
      };
    }
    
    // Try to get real weather data from OpenWeatherMap
    if (OPENWEATHER_API_KEY !== 'YOUR_API_KEY_HERE') {
      const response = await fetch(
        `${OPENWEATHER_BASE_URL}/forecast?q=${encodeURIComponent(location)}&appid=${OPENWEATHER_API_KEY}&units=metric`
      );
      
      if (response.ok) {
        const data = await response.json();
        const weatherData = convertOpenWeatherData(data, location);
        return {
          success: true,
          data: weatherData
        };
      }
    }
    
    // Fallback to demo data for unknown locations
    const demoData = generateDemoWeatherData(location);
    return {
      success: true,
      data: demoData
    };
    
  } catch (error) {
    console.error('Error fetching weather data:', error);
    return {
      success: false,
      error: 'Failed to fetch weather data'
    };
  }
}

// Convert OpenWeatherMap data to our format
function convertOpenWeatherData(data: any, location: string): WeatherData {
  const hourly: HourlyWeather[] = [];
  
  // OpenWeatherMap provides 3-hour forecasts, we'll interpolate to hourly
  data.list.forEach((forecast: any, index: number) => {
    const hour = index * 3;
    if (hour < 24) {
      hourly.push({
        hour,
        solarIrradiance: estimateSolarIrradiance(forecast, hour),
        temperature: forecast.main.temp,
        humidity: forecast.main.humidity,
        cloudCover: forecast.clouds.all
      });
    }
  });
  
  return {
    location,
    latitude: data.city.coord.lat,
    longitude: data.city.coord.lon,
    hourly
  };
}

// Estimate solar irradiance from weather conditions
function estimateSolarIrradiance(forecast: any, hour: number): number {
  if (hour < 6 || hour > 18) return 0; // Night time
  
  const baseIrradiance = 800; // Base irradiance at solar noon
  const timeFactor = Math.cos((hour - 12) * Math.PI / 12);
  const cloudFactor = 1 - (forecast.clouds.all / 100) * 0.7;
  
  return Math.max(0, baseIrradiance * timeFactor * cloudFactor);
}

// Generate demo weather data for unknown locations
function generateDemoWeatherData(location: string): WeatherData {
  const lat = Math.random() * 180 - 90;
  const lon = Math.random() * 360 - 180;
  
  return {
    location,
    latitude: lat,
    longitude: lon,
    hourly: generateDemoHourlyData(lat, lon)
  };
}

// Calculate solar generation based on weather and PV parameters
export function calculateSolarGeneration(
  weatherData: WeatherData,
  area: number, // m²
  efficiency: number, // %
  orientation: string
): number[] {
  const hourlyGeneration: number[] = [];
  
  // Orientation factors (how much sun each orientation gets)
  const orientationFactors = {
    'east': [0.8, 0.9, 1.0, 0.9, 0.8, 0.6, 0.4, 0.3, 0.2, 0.1, 0.1, 0.1, 0.1, 0.2, 0.3, 0.4, 0.6, 0.8, 0.9, 1.0, 0.9, 0.8, 0.6, 0.4],
    'southeast': [0.6, 0.7, 0.8, 0.9, 1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 0.9, 0.8, 0.6],
    'south': [0.1, 0.1, 0.2, 0.3, 0.4, 0.6, 0.8, 0.9, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.9, 0.8, 0.6, 0.4, 0.3, 0.2, 0.1],
    'southwest': [0.4, 0.6, 0.8, 0.9, 1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 0.9, 0.8, 0.6],
    'west': [0.2, 0.1, 0.1, 0.1, 0.1, 0.2, 0.3, 0.4, 0.6, 0.8, 0.9, 1.0, 0.9, 0.8, 0.6, 0.4, 0.3, 0.2, 0.1, 0.1, 0.1, 0.1, 0.2, 0.3]
  };
  
  const factors = orientationFactors[orientation as keyof typeof orientationFactors] || orientationFactors.south;
  
  weatherData.hourly.forEach((hourly, index) => {
    // Convert W/m² to kWh based on panel area and efficiency
    const irradianceFactor = hourly.solarIrradiance / 1000; // Convert to kW/m²
    const areaFactor = area / 1000; // Convert to 1000 m² base
    const efficiencyFactor = efficiency / 100; // Convert percentage to decimal
    
    // Base generation calculation
    let generation = irradianceFactor * areaFactor * efficiencyFactor;
    
    // Apply orientation factor
    generation *= factors[index];
    
    // Temperature effect (higher temperature = lower efficiency)
    const tempEffect = 1 - (hourly.temperature - 25) * 0.004; // 0.4% per °C above 25°C
    generation *= Math.max(0.8, tempEffect);
    
    // Cloud cover effect
    const cloudEffect = 1 - (hourly.cloudCover / 100) * 0.3;
    generation *= cloudEffect;
    
    // Ensure non-negative and reasonable values
    generation = Math.max(0, Math.min(area * efficiency / 100, generation));
    
    hourlyGeneration.push(parseFloat(generation.toFixed(3)));
  });
  
  return hourlyGeneration;
}
