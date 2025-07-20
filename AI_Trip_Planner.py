from langchain_ollama import OllamaLLM
from langchain_community.tools import GoogleSerperResults
from langchain_community.utilities import GoogleSerperAPIWrapper
from crewai import Agent, Crew, Task
import os
import streamlit as st

os.environ["SERPER_API_KEY"] = "dae6a09a1d439f16c3aa02c5eb96ead4b42e744e"

llm = OllamaLLM(model="ollama/llama3.2", base_url="http://localhost:11434")

def search_serp(query: str):
    """
    Searches the web and returns results.
    """
    
    api_wrapper = GoogleSerperAPIWrapper(k=7)
    search_tool = GoogleSerperResults(api_wrapper=api_wrapper)
    return search_tool.run(query)

planner_agent = Agent(
    role="Travel Planner",
    goal="Create a detailed daily itinerary including sightseeing, food, hotels and adventure with priority to users interests",
    backstory="An expert travel consultant and travel guide who crafts personalized travel plans",
    verbose=True,
    llm=llm
)

research_agent = Agent(
    role="Travel Researcher",
    goal="Research the best places to visit, stay, eat, and adventure activities in a city with priority to users interests",
    backstory="An researcher who uses the internet to find latest info about travel destinations",
    verbose=True,
    llm=llm,
)

def gen_plan(from_city, to_city, from_date, to_date, interests):
    srch_query = f"Top {interests}, best places, attractions, food, hotels, and adventure in {to_city}"
    srch_results = search_serp(srch_query)
    #print(f"test 1 {srch_results}")

    research_task = Task(
        description=f"""Use this search result to find key travel recommendations 
        based on traveler interests: {interests}, for {to_city} : {srch_results}
        Summarize in a structered way (Sightseeing, Food, Hotels, Adventure, other activities).""",
        expected_output="Structered travel highlights for the destination",
        agent=research_agent,
    )

    planner_task = Task(
        description=f"""Using the research data, create a day-wise travel itinerary from 
        {from_date.strftime('%Y-%m-%d')} to {to_date.strftime('%Y-%m-%d')} for a traveler going 
        from {from_city} to {to_city}. Provide two-liner introduction for each place. 
        Include recommendations for :
        - Sightseeing
        - Food (Breakfast, Lunch, Dinner)
        - Hotels to stay
        - Optional adventure or cultural activity each day.
        Give priority to traveler interests : {interests}.
        """,
        expected_output="Day-wise travel itinerary",
        agent=planner_agent,
        context=[research_task],
    )


    # Define Crew
    crew = Crew(
        agents=[research_agent, planner_agent],
        tasks=[research_task, planner_task],
        full_output=True,
        verbose=True,
    )

    # Run Crew AI
    result = crew.kickoff()

    #print(f'Results:\n {result}')
    return result


# Streamlit App Title
st.title("🌍 AI-Powered Trip Planner")

st.markdown("""
💡 **Plan your next trip with AI!**  
Enter your travel details below, and our AI-powered travel assistant will create a personalized itinerary including:
 Best places to visit 🎡   Accommodation & budget planning 💰
 Local food recommendations 🍕   Transportation details🚆
""")

# User Inputs
from_city = st.text_input("🏡 From City", "India")
destination_city = st.text_input("✈️ Destination City", "Rome")
date_from = st.date_input("📅 Departure Date")
date_to = st.date_input("📅 Return Date")
interests = st.text_area("🎯 Your Interests (e.g., sightseeing, food, adventure)", "sightseeing and good food")

# Button to run CrewAI
if st.button("🚀 Generate Travel Plan"):
    if not from_city or not destination_city or not date_from or not date_to or not interests:
        st.error("⚠️ Please fill in all fields before generating your travel plan.")
    else:
        st.write("⏳ AI is preparing your personalized travel itinerary... Please wait.")
        
        result = gen_plan(from_city, destination_city, date_from, date_to, interests)

        # Display Results
        st.subheader("✅ Your AI-Powered Travel Plan")
        st.markdown(result)


        # Ensure result is a string
        travel_plan_text = str(result)  # ✅ Convert CrewOutput to string

        st.download_button(
            label="📥 Download Travel Plan",
            data=travel_plan_text,  # ✅ Now passing a valid string
            file_name=f"Travel_Plan_{destination_city}.txt",
            mime="text/plain"
        )

