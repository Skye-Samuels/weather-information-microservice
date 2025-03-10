from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

BASE_URL = "https://wttr.in"


def fetch_weather_data(location, forecast=False):

    try:
        endpoint = f"{BASE_URL}/{location}?format=j1"
        response = requests.get(endpoint, timeout=10)
        response.raise_for_status()
        data = response.json()

        if forecast:
            return data["weather"]
        return data["current_condition"][0]

    except requests.exceptions.Timeout:
        return {"error": "Request timed out. Try again later."}
    except requests.exceptions.HTTPError:
        return {"error": "Invalid location or API error. Check your input."}
    except requests.exceptions.RequestException:
        return {"error": "Failed to connect to the weather service."}


@app.route('/current_weather', methods=['GET'])
def get_current_weather():

    location = request.args.get("location")
    if not location:
        return jsonify({"error": "Missing location parameter"}), 400

    data = fetch_weather_data(location)

    if "error" in data:
        return jsonify(data), 400

    temp_c = float(data["temp_C"])
    temp_f = round((temp_c * 9/5) + 32, 1)

    result = {
        "location": location,
        "temperature_C": temp_c,
        "temperature_F": temp_f,
        "humidity": data["humidity"],
        "weather_condition": data["weatherDesc"][0]["value"]
    }
    return jsonify(result)


@app.route('/forecast', methods=['GET'])
def get_forecast():

    location = request.args.get("location")
    if not location:
        return jsonify({"error": "Missing location parameter"}), 400

    data = fetch_weather_data(location, forecast=True)

    if "error" in data:
        return jsonify(data), 400

    forecast_list = []
    for day in data:
        temp_max_c = float(day["maxtempC"])
        temp_min_c = float(day["mintempC"])

        temp_max_f = round((temp_max_c * 9/5) + 32, 1)
        temp_min_f = round((temp_min_c * 9/5) + 32, 1)

        forecast_list.append({
            "date": day["date"],
            "temperature_max_C": temp_max_c,
            "temperature_max_F": temp_max_f,
            "temperature_min_C": temp_min_c,
            "temperature_min_F": temp_min_f,
            "weather_condition": day["hourly"][0]["weatherDesc"][0]["value"]
        })

    return jsonify({"location": location, "forecast": forecast_list})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8009, debug=True)