# Travel Planner AI Agent

A conversational AI agent that helps users plan custom travel itineraries based on natural language preferences. Users can describe their ideal vacation (e.g., "I want a 5-day trip to somewhere spiritual and not too expensive") and receive a complete, personalized travel plan — with the ability to refine it through follow-up conversations.

---

## 🔧 Tech Stack
- **Python**
- **LangGraph** – for state-based graph execution
- **Custom dataset** – destinations with tags, budget, seasons
- **CLI-based chat** – terminal-based conversation loop

---

## ✨ Features
- 🗣️ **Natural Language Understanding**: Extracts trip preferences like duration, budget level, and interest tags from user prompts.
- 🧭 **Smart Destination Matching**: Recommends destinations that align with user interests, season, and budget.
- 🏞️ **Itinerary Generation**: Auto-generates day-wise activities using a mapped tag-to-activity system.
- 🔁 **Follow-up Refinement**: Handles changes like "make it shorter" or "add some adventure" and updates the itinerary.
- 🧠 **Fuzzy Input Handling**: Recognizes and corrects typos in interests and budget words.
- 🧪 **Node-based Unit Testing**: Each core logic node is independently testable.

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd travel-planner-ai-agent
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the chatbot
```bash
python main.py
```

---

## 💬 Example Usage
```
👤 User: I want a 4-day adventurous and budget-friendly trip
🤖 Agent: Suggests destination + creates itinerary

👤 User: Make it shorter
🤖 Agent: Updates to 3 days, re-generates itinerary

👤 User: Great!
🤖 Agent: Confirms and exits
```

---

## 🧪 Running Tests
```bash
python tests.py
```
All major logic nodes are tested: preference extraction, destination selection, itinerary creation, and follow-up handling.

---

## 📁 Folder Structure
```
agent/
  ├── state.py                  # AgentState dataclass
  ├── graph.py                  # LangGraph workflow
  └── nodes/                    # Individual logic nodes
       ├── extract_preferences.py
       ├── find_destinations.py
       ├── create_itinerary.py
       └── handle_followup.py

main.py                         # CLI loop + agent runner
data/destinations.json          # Destination dataset
tests.py                        # Unit tests
```

---

## 👨‍💻 Developed By
**Umesh Tarasariya**