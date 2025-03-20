from typing import Text, List, Any, Dict
from rasa_sdk import Tracker, FormValidationAction, Action
from rasa_sdk.events import EventType
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict


# Sample data for flights, restaurants, and hotels
flights = [
    {"airline": "Delta", "flight_number": "DL123", "departure": "Miami", "arrival": "Chicago", "date": "2025-02-15"},
    {"airline": "American Airlines", "flight_number": "AA456", "departure": "New York", "arrival": "Chicago", "date": "2025-02-16"},
    {"airline": "United Airlines", "flight_number": "UA789", "departure": "Los Angeles", "arrival": "Chicago", "date": "2025-02-17"},
    {"airline": "Southwest Airlines", "flight_number": "SW123", "departure": "Atlanta", "arrival": "Chicago", "date": "2025-02-18"},
    {"airline": "Spirit Airlines", "flight_number": "SP123", "departure": "Boston", "arrival": "Chicago", "date": "2025-02-19"},
    {"airline": "Alaska Airlines", "flight_number": "AS123", "departure": "Seattle", "arrival": "Chicago", "date": "2025-02-20"},
    {"airline": "Frontier Airlines", "flight_number": "FT123", "departure": "Denver", "arrival": "Chicago", "date": "2025-02-21"},
    {"airline": "JetBlue", "flight_number": "JB123", "departure": "Fort Lauderdale", "arrival": "Chicago", "date": "2025-02-22"},
    {"airline": "Air Canada", "flight_number": "AC123", "departure": "Toronto", "arrival": "Chicago", "date": "2025-02-23"},
    {"airline": "British Airways", "flight_number": "BA123", "departure": "London", "arrival": "Chicago", "date": "2025-02-24"},
    {"airline": "Lufthansa", "flight_number": "LH123", "departure": "Frankfurt", "arrival": "Chicago", "date": "2025-02-25"},
    {"airline": "Air France", "flight_number": "AF123", "departure": "Paris", "arrival": "Chicago", "date": "2025-02-26"},
    {"airline": "KLM", "flight_number": "KL123", "departure": "Amsterdam", "arrival": "Chicago", "date": "2025-02-27"},
    {"airline": "Qatar Airways", "flight_number": "QR123", "departure": "Doha", "arrival": "Chicago", "date": "2025-02-28"},
    {"airline": "Emirates", "flight_number": "EK123", "departure": "Dubai", "arrival": "Chicago", "date": "2025-03-01"},
    {"airline": "Turkish Airlines", "flight_number": "TK123", "departure": "Istanbul", "arrival": "Chicago", "date": "2025-03-02"},
    {"airline": "Singapore Airlines", "flight_number": "SQ123", "departure": "Singapore", "arrival": "Chicago", "date": "2025-03-03"},
    {"airline": "ANA", "flight_number": "NH123", "departure": "Tokyo", "arrival": "Chicago", "date": "2025-03-04"},
    {"airline": "Air India", "flight_number": "AI123", "departure": "Delhi", "arrival": "Chicago", "date": "2025-03-05"},
    {"airline": "Cathay Pacific", "flight_number": "CX123", "departure": "Hong Kong", "arrival": "Chicago", "date": "2025-03-06"}
]

restaurants = [
    {"name": "Giordano's", "cuisine": "Pizza", "location": "Downtown"},
    {"name": "Lou Malnati's", "cuisine": "Pizza", "location": "Downtown"},
    {"name": "RPM Italian", "cuisine": "Italian", "location": "Downtown"},
    {"name": "Gibson's Bar & Steakhouse", "cuisine": "Steakhouse", "location": "Rush Street"},
    {"name": "Fogo de Chão", "cuisine": "Brazilian Steakhouse", "location": "Downtown"},
    {"name": "Rosebud on Rush", "cuisine": "Italian", "location": "Rush Street"},
    {"name": "The Purple Pig", "cuisine": "Mediterranean", "location": "Downtown"},
    {"name": "Eataly Chicago", "cuisine": "Italian", "location": "Downtown"},
    {"name": "Portillo's Hot Dogs", "cuisine": "American", "location": "Downtown"},
    {"name": "Wildberry Pancakes and Cafe", "cuisine": "Breakfast", "location": "Downtown"},
    {"name": "Pequod's Pizza", "cuisine": "Pizza", "location": "Downtown"},
    {"name": "Chicago Cut Steakhouse", "cuisine": "Steakhouse", "location": "Downtown"},
    {"name": "Bavette's Bar & Boeuf", "cuisine": "Steakhouse", "location": "Downtown"},
    {"name": "Greek Islands", "cuisine": "Greek", "location": "Greek Town"},
    {"name": "Athena Greek Restaurant", "cuisine": "Greek", "location": "Greek Town"},
    {"name": "Al's Beef", "cuisine": "American", "location": "Downtown"},
    {"name": "Harry Caray's Italian Steakhouse", "cuisine": "Steakhouse", "location": "Downtown"},
    {"name": "Siena Tavern", "cuisine": "Italian", "location": "Downtown"},
    {"name": "Au Cheval", "cuisine": "American", "location": "Downtown"},
    {"name": "Gene & Georgetti", "cuisine": "Steakhouse", "location": "Downtown"}
]

hotels = [
    {"name": "Hilton Chicago O'Hare Airport", "location": "O'Hare Airport"},
    {"name": "Hyatt Regency O'Hare Chicago", "location": "O'Hare Airport"},
    {"name": "The Peninsula Chicago", "location": "Downtown"},
    {"name": "The Langham, Chicago", "location": "Downtown"},
    {"name": "The Ritz-Carlton, Chicago", "location": "Downtown"},
    {"name": "Hyatt Regency Chicago", "location": "Downtown"},
    {"name": "Sheraton Grand Chicago", "location": "Downtown"},
    {"name": "Swissotel Chicago", "location": "Downtown"},
    {"name": "Trump International Hotel & Tower Chicago", "location": "Downtown"},
    {"name": "Loews Chicago Hotel", "location": "Downtown"},
    {"name": "Sofitel Chicago Magnificent Mile", "location": "Downtown"},
    {"name": "JW Marriott Chicago", "location": "Downtown"},
    {"name": "Four Seasons Hotel Chicago", "location": "Downtown"},
    {"name": "Waldorf Astoria Chicago", "location": "Downtown"},
    {"name": "The Westin Chicago River North", "location": "Downtown"},
    {"name": "Kimpton Hotel Monaco Chicago", "location": "Downtown"},
    {"name": "Palmer House A Hilton Hotel", "location": "Downtown"},
    {"name": "Fairmont Chicago Millennium Park", "location": "Downtown"},
    {"name": "Conrad Chicago", "location": "Downtown"},
    {"name": "Hotel Julian", "location": "Downtown"}
]

class ActionListAirlines(Action):

    def name(self) -> Text:
        return "action_list_airlines"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        airlines = {flight["airline"] for flight in flights}
        airlines_list = "\n".join(airlines)

        dispatcher.utter_message(text=f"Here are the available airlines to travel to Chicago:\n{airlines_list}")
        return []

class ActionListHotelsOhare(Action):

    def name(self) -> Text:
        return "action_list_hotels_ohare"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        hotels_ohare = [hotel["name"] for hotel in hotels if hotel["location"] == "O'Hare Airport"]
        hotels_list = "\n".join(hotels_ohare)

        dispatcher.utter_message(text=f"Here are the available hotels near O'Hare Airport:\n{hotels_list}")
        return []

class ActionListHotelsDowntown(Action):

    def name(self) -> Text:
        return "action_list_hotels_downtown"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        hotels_downtown = [hotel["name"] for hotel in hotels if hotel["location"] == "Downtown"]
        hotels_list = "\n".join(hotels_downtown)

        dispatcher.utter_message(text=f"Here are the available hotels in downtown Chicago:\n{hotels_list}")
        return []

class ActionListItalianRestaurantsDowntown(Action):

    def name(self) -> Text:
        return "action_list_italian_restaurants_downtown"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        italian_restaurants = [restaurant["name"] for restaurant in restaurants if restaurant["cuisine"] == "Italian" and restaurant["location"] == "Downtown"]
        restaurants_list = "\n".join(italian_restaurants)
        dispatcher.utter_message(text=f"Here are the available Italian restaurants in downtown Chicago:\n{restaurants_list}")
        return []

from datetime import datetime, timedelta

class ActionRecommendTripPlan(Action):
    def name(self) -> Text:
        return "action_recommend_trip_plan"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        departure_city = tracker.get_slot("departure_city")
        destination_city = tracker.get_slot("destination_city")
        departure_date = tracker.get_slot("departure_date")
        return_date = tracker.get_slot("return_date")
        flight_preference = tracker.get_slot("flight_preference")
        food_preference = tracker.get_slot("food_preference")

        # Debug statements to print slot values
        print(f"Departure City: {departure_city}")
        print(f"Destination City: {destination_city}")
        print(f"Departure Date: {departure_date}")
        print(f"Return Date: {return_date}")
        print(f"Flight Preference: {flight_preference}")
        print(f"Food Preference: {food_preference}")

        # Check if all necessary slots are filled
        if not all([departure_city, destination_city, departure_date, return_date, flight_preference, food_preference]):
            dispatcher.utter_message(text="Please provide all the necessary information for the trip plan.")
            return []

        # Convert natural language dates to YYYY-MM-DD format
        today = datetime.today()
        days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        
        def get_date_from_day(day_name, start_date):
            day_index = days_of_week.index(day_name)
            current_day_index = start_date.weekday()
            delta_days = (day_index - current_day_index + 7) % 7
            return (start_date + timedelta(days=delta_days)).strftime("%Y-%m-%d")

        departure_date_formatted = get_date_from_day(departure_date, today)
        return_date_formatted = get_date_from_day(return_date, datetime.strptime(departure_date_formatted, "%Y-%m-%d"))

        # Debug statements to print formatted dates
        print(f"Formatted Departure Date: {departure_date_formatted}")
        print(f"Formatted Return Date: {return_date_formatted}")

        # Find flights based on user preferences
        matching_flights = [flight for flight in flights if flight["departure"] == departure_city and flight["arrival"] == destination_city and departure_date_formatted <= flight["date"] <= return_date_formatted and flight_preference in flight["airline"]]

        # Debug statement to print matching flights
        print(f"Matching Flights: {matching_flights}")

        # Find restaurants based on user preferences
        matching_restaurants = [restaurant for restaurant in restaurants if food_preference in restaurant["cuisine"]]

        # Debug statement to print matching restaurants
        print(f"Matching Restaurants: {matching_restaurants}")

        # Create a trip plan message
        trip_plan = f"Here is your recommended trip plan:\n\nFlights:\n"
        for flight in matching_flights:
            trip_plan += f"- {flight['airline']} flight {flight['flight_number']} from {flight['departure']} to {flight['arrival']} on {flight['date']}\n"

        trip_plan += "\nRestaurants:\n"
        for restaurant in matching_restaurants:
            trip_plan += f"- {restaurant['name']} ({restaurant['cuisine']}) at {restaurant['location']}\n"

        dispatcher.utter_message(text=trip_plan)
        return []




ALLOWED_PIZZA_SIZES = [
    "small",
    "medium",
    "large",
    "extra-large",
    "extra large",
    "s",
    "m",
    "l",
    "xl",
]
ALLOWED_PIZZA_TYPES = ["mozzarella", "fungi", "veggie", "pepperoni", "hawaii"]
VEGETARIAN_PIZZAS = ["mozzarella", "fungi", "veggie"]
MEAT_PIZZAS = ["pepperoni", "hawaii"]





class ActionSearchSports(Action):
    def name(self) -> Text:
        return "action_search_sports"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        sports_events = "Here are some sports events: Football, Basketball, Baseball."
        dispatcher.utter_message(text=sports_events)
        return []


class ActionShowSportsReviews(Action):
    def name(self) -> Text:
        return "action_show_sports_reviews"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        sports_reviews = "Here are some sports reviews: Great game, Exciting game, the refs suck."
        dispatcher.utter_message(text=sports_reviews)
        return []


class ValidateSimplePizzaForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_simple_pizza_form"

    def validate_pizza_size(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `pizza_size` value."""

        if slot_value.lower() not in ALLOWED_PIZZA_SIZES:
            dispatcher.utter_message(text=f"We only accept pizza sizes: s/m/l/xl.")
            return {"pizza_size": None}
        dispatcher.utter_message(text=f"OK! You want to have a {slot_value} pizza.")
        return {"pizza_size": slot_value}

    def validate_pizza_type(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `pizza_type` value."""

        if slot_value not in ALLOWED_PIZZA_TYPES:
            dispatcher.utter_message(
                text=f"I don't recognize that pizza. We serve {'/'.join(ALLOWED_PIZZA_TYPES)}."
            )
            return {"pizza_type": None}
        dispatcher.utter_message(text=f"OK! You want to have a {slot_value} pizza.")
        return {"pizza_type": slot_value}


class AskForVegetarianAction(Action):
    def name(self) -> Text:
        return "action_ask_vegetarian"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        dispatcher.utter_message(
            text="Would you like to order a vegetarian pizza?",
            buttons=[
                {"title": "yes", "payload": "/affirm"},
                {"title": "no", "payload": "/deny"},
            ],
        )
        return []


class AskForPizzaTypeAction(Action):
    def name(self) -> Text:
        return "action_ask_pizza_type"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        if tracker.get_slot("vegetarian"):
            dispatcher.utter_message(
                text=f"What kind of pizza do you want?",
                buttons=[{"title": p, "payload": p} for p in VEGETARIAN_PIZZAS],
            )
        else:
            dispatcher.utter_message(
                text=f"What kind of pizza do you want?",
                buttons=[{"title": p, "payload": p} for p in MEAT_PIZZAS],
            )
        return []


class ValidateFancyPizzaForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_fancy_pizza_form"

    def validate_vegetarian(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `pizza_size` value."""
        if tracker.get_intent_of_latest_message() == "affirm":
            dispatcher.utter_message(
                text="I'll remember you prefer vegetarian."
            )
            return {"vegetarian": True}
        if tracker.get_intent_of_latest_message() == "deny":
            dispatcher.utter_message(
                text="I'll remember that you don't want a vegetarian pizza."
            )
            return {"vegetarian": False}
        dispatcher.utter_message(text="I didn't get that.")
        return {"vegetarian": None}

    def validate_pizza_size(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `pizza_size` value."""

        if slot_value not in ALLOWED_PIZZA_SIZES:
            dispatcher.utter_message(text=f"We only accept pizza sizes: s/m/l/xl.")
            return {"pizza_size": None}
        dispatcher.utter_message(text=f"OK! You want to have a {slot_value} pizza.")
        return {"pizza_size": slot_value}

    def validate_pizza_type(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `pizza_type` value."""

        if slot_value not in ALLOWED_PIZZA_TYPES:
            dispatcher.utter_message(
                text=f"I don't recognize that pizza. We serve {'/'.join(ALLOWED_PIZZA_TYPES)}."
            )
            return {"pizza_type": None}
        if not slot_value:
            dispatcher.utter_message(
                text=f"I don't recognize that pizza. We serve {'/'.join(ALLOWED_PIZZA_TYPES)}."
            )
            return {"pizza_type": None}
        dispatcher.utter_message(text=f"OK! You want to have a {slot_value} pizza.")
        return {"pizza_type": slot_value}
