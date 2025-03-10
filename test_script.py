import requests
import json

BASE_URL = "http://localhost:8009"

def test_current_weather(location):
    print(f"\n🔍 Testing Current Weather for: 🌍 {location}")
    
    try:
        response = requests.get(f"{BASE_URL}/current_weather?location={location}", timeout=5)
        response.raise_for_status()
        data = response.json()

        print("\n📜 RAW JSON Response:")
        print(json.dumps(data, indent=4))

        if "error" in data:
            print(f"\n❌ Test Failed: {data['error']}")
        else:
            print("\n✅ Test Passed")
            print(f"🌡 Temperature: {data['temperature_C']}°C / {data['temperature_F']}°F")
            print(f"💧 Humidity: {data['humidity']}%")
            print(f"⛅ Condition: {data['weather_condition']}")

    except requests.exceptions.RequestException as e:
        print(f"\n❌ Test Failed: {e}")


def test_forecast(location):
    print(f"\n🔍 Testing 7-Day Forecast for: 🌍 {location}")
    
    try:
        response = requests.get(f"{BASE_URL}/forecast?location={location}", timeout=5)
        response.raise_for_status()
        data = response.json()

        print("\n📜 RAW JSON Response:")
        print(json.dumps(data, indent=4))

        if "error" in data:
            print(f"\n❌ Test Failed: {data['error']}")
        else:
            print("\n✅ Test Passed")
            for day in data["forecast"]:
                print(f"\n📅 Date: {day['date']}")
                print(f"🌡 Max Temp: {day['temperature_max_C']}°C / {day['temperature_max_F']}°F")
                print(f"🌡 Min Temp: {day['temperature_min_C']}°C / {day['temperature_min_F']}°F")
                print(f"⛅ Condition: {day['weather_condition']}")

    except requests.exceptions.RequestException as e:
        print(f"\n❌ Test Failed: {e}")


def run_tests():
    print("\n🚀 Running Weather Service Tests...\n")

    test_locations = ["London", "Los Angeles", "Corvallis", "InvalidCity"]

    for location in test_locations:
        test_current_weather(location)
        test_forecast(location)

    print("\n✅ All tests completed.\n")


if __name__ == "__main__":
    run_tests()
