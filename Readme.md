# 📅 Multi-Agent Scheduling Assistant

A Multi-Agent Scheduling Assistant built using **LangGraph**, **LangChain**, **Groq LLM**, **SQLite**, and **Streamlit**.

The assistant understands user requests, routes them to specialized agents, validates booking details, checks calendar availability, reserves appointments, and sends mock notifications.

---

## 🚀 Features

- 🤖 Multi-Agent workflow using LangGraph
- 🧠 Triage Agent for intent classification
- 📅 Booking Agent for appointment handling
- 📆 Relative date parsing (e.g. "tomorrow", "next Monday")
- ⏰ Time normalization
- 📧 Email validation
- 💾 SQLite database for appointment storage
- 🧠 SQLiteSaver checkpoint memory
- 🔔 Mock booking notification
- 🎨 Streamlit chat interface
- 🔄 Multi-turn conversations

---

# 🏗️ Architecture

```

```
                    Streamlit UI
                         │
                         ▼
                 LangGraph Workflow
                         │
                ┌────────┴────────┐
                │                 │
                ▼                 ▼
         Triage Agent       Booking Agent
                                 │
          ┌──────────────────────┼─────────────────────┐
          ▼                      ▼                     ▼
     Validator            Calendar Tools      Notification Tool
                                 │
                                 ▼
                         Database Manager
                                 │
                                 ▼
                              SQLite
```

---

# 🧠 Agent Workflow

### 1️⃣ Triage Agent

Responsible for understanding user intent.

Supported intents:

- Greeting
- Appointment Booking
- Availability Check
- Unknown Query

Example:

```
User:
Book an appointment tomorrow

↓

Intent:
booking
```

---

### 2️⃣ Booking Agent

Handles the complete booking process.

Responsibilities:

- Extract booking details
- Parse relative dates
- Validate inputs
- Ask for missing information
- Check slot availability
- Reserve appointments
- Trigger notification

Example:

```
User:
Book tomorrow

↓

Assistant:
Please provide your preferred time and email.

↓

User:
3 PM

↓

Assistant:
Please provide your email.

↓

User:
abc@gmail.com

↓

Appointment Confirmed
```

---

# 📂 Project Structure

```
multi-agent-scheduler/

│
├── app.py
│
├── requirements.txt
│
├── README.md
│
├── graph_memory.db
│
├── appointments.db
│
└── src
    │
    ├── agents
    │     ├── booking_agent.py
    │     └── triage_agent.py
    │
    ├── config
    │
    ├── database
    │
    ├── graph
    │     ├── graph.py
    │     └── state.py
    │
    ├── prompts
    │
    ├── tools
    │     ├── calendar_tools.py
    │     ├── notification.py
    │     └── validator.py
    │
    └── utils
          └── llm.py
```

---

# ⚙️ Tech Stack

| Technology | Purpose |
|------------|---------|
| Python | Backend |
| LangGraph | Agent orchestration |
| LangChain | LLM integration |
| Groq | LLM |
| SQLite | Appointment database |
| SQLiteSaver | Conversation memory |
| Streamlit | Frontend |
| DateParser | Date parsing |

---

# 🔄 Conversation Flow

```
User
 │
 ▼
Streamlit
 │
 ▼
LangGraph
 │
 ▼
Triage Agent
 │
 ├── Greeting
 │
 ├── Unknown
 │
 └── Booking
        │
        ▼
 Booking Agent
        │
        ▼
Extract Details
        │
        ▼
Validate Inputs
        │
        ▼
Missing?
 │
 ├── Yes → Ask User
 │
 └── No
       │
       ▼
Check Availability
       │
       ▼
Reserve Slot
       │
       ▼
Send Notification
       │
       ▼
Return Response
```

---

# 📦 Installation

Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/multi-agent-scheduler.git

cd multi-agent-scheduler
```

Create a virtual environment

```bash
python -m venv .venv
```

Activate the environment

Windows

```bash
.venv\Scripts\activate
```

Linux / Mac

```bash
source .venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create a `.env` file.

```
GROQ_API_KEY=your_api_key
MODEL_NAME=llama-3.3-70b-versatile
```

---

# ▶️ Run the Application

```bash
streamlit run app.py
```

---

# 💬 Example Conversations

### Booking Appointment

```
User:
Book tomorrow at 3 PM

Assistant:
Please provide your email.

User:
abc@gmail.com

Assistant:
Your appointment has been booked successfully.
```

---

### Slot Unavailable

```
User:
Book tomorrow at 3 PM for abc@gmail.com

Assistant:
The slot is already booked.

Would you like another time or date?
```

---

### Greeting

```
User:
Hello

Assistant:
Hello! How can I help you schedule an appointment today?
```

---

# ✅ Assignment Requirements Covered

| Requirement | Status |
|-------------|--------|
| LangGraph | ✅ |
| Multi-Agent Workflow | ✅ |
| Triage Agent | ✅ |
| Booking Agent | ✅ |
| Input Validation | ✅ |
| Relative Date Parsing | ✅ |
| SQLite Database | ✅ |
| SQLiteSaver Memory | ✅ |
| Mock Notification | ✅ |
| Streamlit UI | ✅ |
| Render Deployment Ready | ✅ |

---

# 📸 Demo

## Greeting

![HOME](screenshots/Home.png)

## Multi-turn Booking

![Booking](screenshots/booking.png)

## Slot Unavailable

![Unavailable](screenshots/unavailable.png)
# 🔮 Future Improvements

- Google Calendar Integration
- Email Notifications
- Multiple Appointment Types
- Real Calendar API
- Authentication
- Timezone Support

---

# 👨‍💻 Author

**Adhrav Rai**

Third Year B.Tech Student

Madan Mohan Malaviya University of Technology

---