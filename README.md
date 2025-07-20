AI-Powered Trip Planner
Project Overview
This project is an AI-driven travel planning tool that automatically creates personalized travel itineraries. It helps users plan trips by simply entering their source and destination cities, travel dates, and interests such as food, adventure, nature, etc. The system then generates a complete day-wise travel plan, saving users time and effort.

Features
Accepts user inputs for destination, dates, and interests

Real-time data collection using Google Serper API

Personalized travel recommendations with language model (OllamaLLM)

Two intelligent agents: Research Agent and Planner Agent using CrewAI

Generates structured itineraries including:

Sightseeing

Food and dining options

Accommodation

Activities and experiences

Simple and interactive user interface built with Streamlit

Tech Stack
Frontend: Streamlit

Backend:

Python

LangChain with OllamaLLM

Google Serper API

CrewAI for multi-agent collaboration

Architecture
User Input: Users provide travel details via the Streamlit interface.

Research Agent: Searches for relevant travel content using the Google Serper API.

Planner Agent: Organizes the data into a structured, day-wise itinerary.

Output: The complete itinerary is displayed to the user in an easy-to-read format.

How to Run
Clone the repository:

bash
Copy
Edit
git clone https://github.com/yourusername/ai-trip-planner.git
cd ai-trip-planner
Install required packages:

nginx
Copy
Edit
pip install -r requirements.txt
Set up environment variables for Serper API and other credentials.

Run the application:

arduino
Copy
Edit
streamlit run app.py
Use Cases
Solo travel planning

Family vacation organization

Last-minute trip preparation

Travel agencies looking to automate itinerary suggestions

Future Improvements
Integration with flight and hotel booking APIs

Offline itinerary export (PDF, Word)

Multilingual support

User feedback and itinerary rating

License
This project is open-source and available under the MIT License.
