import streamlit as st
from agent import agent_executor
from tools.places_tool import discover_places

st.set_page_config(page_title="Agentic AI Travel Planner")

st.title("✈️ Agentic AI Travel Planner")

query = st.text_input(
    "Enter your trip request",
    placeholder="Example: 4 day trip hyderabad-goa"
)

if st.button("Generate Plan"):

    if query:

        with st.spinner("Generating your travel plan..."):

            # -----------------------------
            # Run Agent
            # -----------------------------
            result = agent_executor.invoke({
                "input": query
            })

            # -----------------------------
            # Extract outputs
            # -----------------------------
            output = result.get("output", "")

            steps = result.get(
                "intermediate_steps",
                []
            )

            flight = None
            hotel = None
            places = []

            # -----------------------------
            # Extract tool results
            # -----------------------------
            for action, observation in steps:

                tool_name = action.tool

                if tool_name == "search_flights":

                    flight = observation

                elif tool_name == "recommend_hotel":

                    hotel = observation

                elif tool_name == "discover_places":

                    places = observation

            # -----------------------------
            # Force places if agent skipped
            # -----------------------------
            if not places:

                destination = "Goa"

                if flight:
                    destination = flight["to"]

                places = discover_places.invoke(
                    destination
                )

            # -----------------------------
            # Extract days dynamically
            # -----------------------------
            days = 3

            for word in query.split():

                if word.isdigit():

                    days = int(word)

                    break

            # -----------------------------
            # Weather fallback
            # -----------------------------
            weather_samples = [
                "Sunny (31°C)",
                "Partly Cloudy (29°C)",
                "Light Rain (27°C)",
                "Clear Sky (30°C)",
                "Humid (28°C)",
                "Overcast (26°C)"
            ]

            # -----------------------------
            # Display success
            # -----------------------------
            st.success(
                "Travel Plan Generated!"
            )

            # -----------------------------
            # Agent reasoning
            # -----------------------------
            st.subheader(
                "🧠 Agent Reasoning"
            )

            st.code(output)

            # -----------------------------
            # Flight
            # -----------------------------
            if flight:

                st.subheader(
                    "✈️ Flight Selected"
                )

                st.write(
                    f"**{flight['airline']}** "
                    f"(₹{flight['price']})"
                )

                st.write(
                    f"Route: "
                    f"{flight['from']} → "
                    f"{flight['to']}"
                )

                st.write(
                    f"Departure: "
                    f"{flight['departure']}"
                )

            # -----------------------------
            # Hotel
            # -----------------------------
            if hotel:

                st.subheader(
                    "🏨 Hotel Booked"
                )

                st.write(
                    f"**{hotel['name']}** "
                    f"({hotel['stars']}★)"
                )

                st.write(
                    f"₹{hotel['price_per_night']} "
                    f"per night"
                )

            # -----------------------------
            # Weather
            # -----------------------------
            st.subheader(
                "🌦️ Weather Forecast"
            )

            for i in range(days):

                weather = weather_samples[
                    i % len(weather_samples)
                ]

                st.write(
                    f"Day {i+1}: "
                    f"{weather}"
                )

            # -----------------------------
            # Places / Itinerary
            # -----------------------------
            st.subheader("📍 Itinerary")

            # Safety handling
            if isinstance(places, dict):

                places = list(
                    places.values()
                )

            elif isinstance(places, str):

                cleaned = (
                    places
                    .replace("[", "")
                    .replace("]", "")
                    .replace("'", "")
                )

                places = [
                    p.strip()
                    for p in cleaned.split(",")
                    if p.strip()
                ]

            elif not isinstance(places, list):

                places = []

            # Display itinerary
            if places:

                for i in range(days):

                    place = places[
                        i % len(places)
                    ]

                    st.write(
                        f"Day {i+1}: "
                        f"{place}"
                    )

            else:

                st.write(
                    "No itinerary available."
                )

            # -----------------------------
            # Budget
            # -----------------------------
            st.subheader(
                "💰 Estimated Budget"
            )

            flight_cost = (
                flight["price"]
                if flight else 0
            )

            hotel_cost = (
                hotel["price_per_night"]
                * days
                if hotel else 0
            )

            food_cost = 1500 * days

            total = (
                flight_cost
                + hotel_cost
                + food_cost
            )

            st.write(
                f"Flight: ₹{flight_cost}"
            )

            st.write(
                f"Hotel: ₹{hotel_cost}"
            )

            st.write(
                f"Food & Travel: ₹{food_cost}"
            )

            st.markdown("---")

            st.success(
                f"Total Cost: ₹{total}"
            )

    else:

        st.warning(
            "Please enter a trip request."
        )