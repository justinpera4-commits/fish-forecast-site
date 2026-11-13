
from drafter import *
from dataclasses import dataclass
from bakery import assert_equal


# 2025 Newark, Delaware assumed weather data
AVERAGE_TEMP = 56.5
AVERAGE_HIGH = 78.1
AVERAGE_LOW = 35.1
AVERAGE_HUMIDITY = 74
AVERAGE_WIND = 2.7


@dataclass
class FishingResult:
    fish_species: str
    season: str
    fishing_time: str
    temperature: float
    humidity: float
    wind_speed: float
    score: int
    rating: str
    recommendation: str


@dataclass
class State:
    fish_species: str
    season: str
    fishing_time: str
    temperature: float
    humidity: float
    wind_speed: float
    past_forecasts: list[FishingResult]
    status: str


# ----------------------------------
# TEMPERATURE SCORING
# ----------------------------------

def temperature_score(fish_species: str,
                      temperature: float) -> int:
    """Calculate points based on fish species and temperature."""

    if fish_species == "Bass":
        if 60 <= temperature <= 80:
            return 40
        elif 50 <= temperature < 60:
            return 30
        else:
            return 15

    elif fish_species == "Trout":
        if 45 <= temperature <= 65:
            return 40
        elif 35 <= temperature < 45:
            return 30
        else:
            return 15

    elif fish_species == "Catfish":
        if 65 <= temperature <= 85:
            return 40
        elif 50 <= temperature < 65:
            return 30
        else:
            return 15

    else:  # Crappie
        if 55 <= temperature <= 75:
            return 40
        elif 45 <= temperature < 55:
            return 30
        else:
            return 15


# ----------------------------------
# SEASON SCORING
# ----------------------------------

def season_score(fish_species: str, season: str) -> int:
    """Calculate points based on fish species and season."""

    if fish_species == "Bass":
        if season == "Spring" or season == "Fall":
            return 25
        else:
            return 18

    elif fish_species == "Trout":
        if season == "Spring" or season == "Fall":
            return 25
        else:
            return 18

    elif fish_species == "Catfish":
        if season == "Summer":
            return 25
        else:
            return 18

    else:  # Crappie
        if season == "Spring" or season == "Fall":
            return 25
        else:
            return 18


# ----------------------------------
# TIME SCORING
# ----------------------------------

def time_score(fishing_time: str) -> int:
    """Calculate points based on time of day."""

    if fishing_time == "Early Morning":
        return 20

    elif fishing_time == "Evening":
        return 20

    elif fishing_time == "Afternoon":
        return 12

    else:
        return 8


# ----------------------------------
# WEATHER SCORING
# ----------------------------------

def weather_score(humidity: float,
                  wind_speed: float) -> int:
    """Calculate points based on humidity and wind."""

    score = 0

    if humidity <= 75:
        score += 8
    elif humidity <= 85:
        score += 5
    else:
        score += 2

    if wind_speed <= 3:
        score += 7
    elif wind_speed <= 5:
        score += 5
    else:
        score += 2

    return score


# ----------------------------------
# FISHING RATING
# ----------------------------------

def get_rating(score: int) -> str:
    """Convert the total score into a fishing rating."""

    if score >= 85:
        return "Excellent"

    elif score >= 70:
        return "Good"

    elif score >= 55:
        return "Fair"

    elif score >= 40:
        return "Poor"

    else:
        return "Very Poor"


def get_recommendation(rating: str) -> str:
    """Give fishing advice based on the rating."""

    if rating == "Excellent":
        return "Excellent estimated conditions for fishing!"

    elif rating == "Good":
        return "Good estimated conditions. Fishing is worth considering."

    elif rating == "Fair":
        return "Average conditions. You may still have some luck."

    elif rating == "Poor":
        return "Conditions are not very favorable for fishing."

    else:
        return "These conditions may make fishing difficult."


# ----------------------------------
# CALCULATE TOTAL SCORE
# ----------------------------------

def calculate_score(fish_species: str,
                    season: str,
                    fishing_time: str,
                    temperature: float,
                    humidity: float,
                    wind_speed: float) -> int:
    """Add all four scoring categories together."""

    temperature_points = temperature_score(
        fish_species, temperature)

    season_points = season_score(
        fish_species, season)

    time_points = time_score(fishing_time)

    weather_points = weather_score(
        humidity, wind_speed)

    total = (temperature_points + season_points
             + time_points + weather_points)

    return total


# ----------------------------------
# HOME PAGE
# ----------------------------------

@route
def index(state: State) -> Page:
    return Page(state, [
        Header("FishCast"),

        "Welcome to FishCast!",

        "Find out how good the fishing conditions are in Newark, Delaware.",

        "This version uses assumed weather data based on 2025 conditions.",

        "You can customize your fish species, season, time, and weather conditions.",

        Button("Choose Your Fish", "fish_selection"),

        Button("Previous Results", "previous_results")
    ])


# ----------------------------------
# FISH SELECTION PAGE
# ----------------------------------

@route
def fish_selection(state: State) -> Page:
    return Page(state, [
        Header("Choose Your Fishing Conditions"),

        "What type of fish are you trying to catch?",

        SelectBox(
            "fish_species",
            ["Bass", "Trout", "Catfish", "Crappie"],
            state.fish_species if state.fish_species else "Bass"
        ),

        "What season are you fishing in?",

        SelectBox(
            "season",
            ["Spring", "Summer", "Fall", "Winter"],
            state.season
        ),

        "What time of day will you be fishing?",

        SelectBox(
            "fishing_time",
            ["Early Morning", "Afternoon", "Evening"],
            state.fishing_time
        ),

        "Enter the current temperature (Fahrenheit):",

        TextBox(
            "temperature",
            kind="number",
            default_value=state.temperature
        ),

        "Enter the humidity percentage:",

        TextBox(
            "humidity",
            kind="number",
            default_value=state.humidity
        ),

        "Enter the wind speed (MPH):",

        TextBox(
            "wind_speed",
            kind="number",
            default_value=state.wind_speed
        ),

        Button("Calculate Forecast", "calculate_forecast"),

        Button("Home", "index")
    ])


# ----------------------------------
# CALCULATE FORECAST PAGE
# ----------------------------------

@route
def calculate_forecast(state: State,
                       fish_species: str,
                       season: str,
                       fishing_time: str,
                       temperature: float,
                       humidity: float,
                       wind_speed: float) -> Page:

    # Save the user's selections

    state.fish_species = fish_species
    state.season = season
    state.fishing_time = fishing_time
    state.temperature = temperature
    state.humidity = humidity
    state.wind_speed = wind_speed

    # Calculate total score

    total_score = calculate_score(
        fish_species,
        season,
        fishing_time,
        temperature,
        humidity,
        wind_speed
    )

    # Determine rating and recommendation

    rating = get_rating(total_score)

    recommendation = get_recommendation(rating)

    # Create a new fishing result

    new_result = FishingResult(
        fish_species,
        season,
        fishing_time,
        temperature,
        humidity,
        wind_speed,
        total_score,
        rating,
        recommendation
    )

    # Save result in history

    state.past_forecasts.append(new_result)

    state.status = "Your fishing forecast is ready!"

    return results(state)


# ----------------------------------
# RESULTS PAGE
# ----------------------------------

@route
def results(state: State) -> Page:

    latest = state.past_forecasts[-1]

    return Page(state, [

        Header("Your Fishing Forecast"),

        state.status,

        "Location: Newark, Delaware",

        "Fish Species: " + latest.fish_species,

        "Season: " + latest.season,

        "Time of Day: " + latest.fishing_time,

        "Temperature: " + str(latest.temperature) + " F",

        "Humidity: " + str(latest.humidity) + "%",

        "Wind Speed: " + str(latest.wind_speed) + " MPH",

        Header("Score Breakdown"),

        "Temperature: " + str(temperature_score(
            latest.fish_species,
            latest.temperature)) + " / 40",

        "Season: " + str(season_score(
            latest.fish_species,
            latest.season)) + " / 25",

        "Time: " + str(time_score(
            latest.fishing_time)) + " / 20",

        "Weather: " + str(weather_score(
            latest.humidity,
            latest.wind_speed)) + " / 15",

        Header("Final Fishing Score"),

        str(latest.score) + " / 100",

        "Rating: " + latest.rating,

        latest.recommendation,

        Button("Try Another Fish", "fish_selection"),

        Button("Previous Results", "previous_results"),

        Button("Home", "index")
    ])


# ----------------------------------
# PREVIOUS RESULTS PAGE
# ----------------------------------

@route
def previous_results(state: State) -> Page:

    content = [Header("Previous Fishing Results")]

    if len(state.past_forecasts) == 0:

        content.append("You have no previous forecasts.")

    else:

        for forecast in state.past_forecasts:

            content.append("--------------------")

            content.append("Fish: " + forecast.fish_species)

            content.append("Season: " + forecast.season)

            content.append("Time: " + forecast.fishing_time)

            content.append(
                "Temperature: " + str(forecast.temperature) + " F")

            content.append(
                "Humidity: " + str(forecast.humidity) + "%")

            content.append(
                "Wind Speed: " + str(forecast.wind_speed) + " MPH")

            content.append(
                "Score: " + str(forecast.score) + " / 100")

            content.append("Rating: " + forecast.rating)

            content.append(forecast.recommendation)

    content.append(Button("Choose Another Fish", "fish_selection"))

    content.append(Button("Clear History", "clear_history"))

    content.append(Button("Home", "index"))

    return Page(state, content)


# ----------------------------------
# CLEAR HISTORY
# ----------------------------------

@route
def clear_history(state: State) -> Page:

    state.past_forecasts = []

    state.status = "Your history has been cleared."

    return previous_results(state)


# ----------------------------------
# TESTS
# ----------------------------------

assert_equal(get_rating(90), "Excellent")
assert_equal(get_rating(75), "Good")
assert_equal(get_rating(60), "Fair")
assert_equal(get_rating(45), "Poor")
assert_equal(get_rating(20), "Very Poor")

assert_equal(time_score("Early Morning"), 20)
assert_equal(time_score("Afternoon"), 12)
assert_equal(time_score("Evening"), 20)

assert_equal(weather_score(74, 2.7), 15)

assert_equal(season_score("Bass", "Fall"), 25)
assert_equal(season_score("Catfish", "Summer"), 25)

assert_equal(temperature_score("Bass", 65), 40)


# ----------------------------------
# START WEBSITE
# ----------------------------------

start_server(State(
    "Bass",
    "Fall",
    "Early Morning",
    AVERAGE_TEMP,
    AVERAGE_HUMIDITY,
    AVERAGE_WIND,
    [],
    "Welcome to FishCast!"
))
