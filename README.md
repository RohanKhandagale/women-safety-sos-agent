# 🚨 Women Safety SOS Agent (Google ADK + Vertex AI)

An AI-powered multilingual emergency detection agent built using the **Google AI Agents Development Kit (ADK)** and deployed on **Vertex AI Agent Engine**.  
This project was created as part of the **Google Kaggle 5-Day AI Agents Intensive Capstone Project**.

The agent listens for emergency phrases in **English, Hindi, and Marathi** and triggers a **simulated SOS alert** after user confirmation.

---

## 🧠 Features

### ✔ Multilingual Support  
Understands help phrases in:
- English  
- हिंदी (Hindi)  
- मराठी (Marathi)

### ✔ Emergency Phrase Detection  
Detects commands like:
- **“help”**, **“save me”**  
- **“मुझे मदद चाहिए”**, **“बचाओ”**  
- **“मदत करा”**, **“वाचवा”**

### ✔ Confirmation Flow  
Before sending SOS, the agent asks:
> “Do you want to send SOS? Yes or Cancel?”

### ✔ SOS Simulation  
Returns a structured JSON file, like:

```json
{
  "time": "20251125_071746",
  "details": {
    "reason": {
      "is_emergency": true,
      "level": "danger",
      "matches": ["bachao"]
    }
  },
  "note": "SOS simulated — no real dispatch."
}

