# FitVisionAI
FitVision AI 💪
FitVision AI is an AI-powered fitness coaching application built with Streamlit and Google's Gemini API.
The application combines conversational AI, optional computer vision, personalized fitness profiles, workout planning, nutrition guidance, and progress tracking in one interface.
Features
🔐 Simple sign-up interface
👤 Personalized fitness onboarding
🎯 Fitness goal selection
💪 Personalized workout planning
🍎 Weekly nutrition planning
🤖 AI fitness coach chatbot
📸 AI-powered body image analysis
🏋️ Exercise and training guidance
📊 Basic progress tracking
👤 Fitness profile management
⚡ Quick actions for common fitness questions
🌐 Streamlit-based web interface
Application Flow
```text
Sign Up
   ↓
Fitness Onboarding
   ↓
Optional Body Image
   ↓
Personalized Fitness Profile
   ↓
Dashboard
   ├── AI Coach
   ├── Workouts
   ├── Nutrition
   ├── AI Vision
   ├── Progress
   └── Profile
```
Tech Stack
Python
Streamlit
Google Gemini API
Google GenAI Python SDK
HTML/CSS through Streamlit
Git & GitHub
Project Structure
```text
FitVisionAI/
│
├── apps.py
├── system_prompt.txt
├── requirements.txt
├── README.md
│
└── .streamlit/
    └── secrets.toml
```
Installation
1. Clone the repository
```bash
git clone https://github.com/Omkar143256/FitVisionAI.git
cd FitVisionAI
```
2. Create a virtual environment
Windows:
```powershell
python -m venv venv
venv\Scripts\activate
```
macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```
3. Install dependencies
```bash
pip install -r requirements.txt
```
Gemini API Configuration
Create:
```text
.streamlit/secrets.toml
```
Add your Gemini API key:
```toml
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"
```
Do not commit `secrets.toml` to GitHub.
Add it to `.gitignore`:
```text
.streamlit/secrets.toml
venv/
__pycache__/
*.pyc
```
Run the Application
Start Streamlit with:
```bash
streamlit run apps.py
```
The application will open in your browser.
AI System Prompt
The coaching behavior can be maintained separately in:
```text
system_prompt.txt
```
Keeping the system prompt separate from the application code makes it easier to update the AI's coaching behavior without modifying the UI implementation.
AI Vision
Users can optionally upload a suitable full-body image.
The vision functionality is intended to provide general fitness-related observations such as:
Visible posture
General body proportions
Potential training focus areas
General exercise recommendations
Image analysis should be treated as an estimate. It should not be used to diagnose medical conditions or determine precise body measurements.
Safety
FitVision AI provides general fitness and nutrition guidance.
It is not a replacement for:
A qualified personal trainer
Registered dietitian
Physiotherapist
Doctor or other healthcare professional
Users with injuries, medical conditions, severe pain, or other significant health concerns should seek appropriate professional advice.
Future Development
Potential areas for future development include:
🔑 Production authentication
🗄️ Persistent user database
📈 Advanced progress analytics
📸 Exercise-form analysis
🎥 Video-based movement analysis
🗓️ Adaptive workout scheduling
🥗 Automated meal and grocery planning
⌚ Wearable/device integration
🔔 Workout and nutrition reminders
📱 Mobile-first interface
🌍 Multilingual fitness coaching
Disclaimer
FitVision AI is an educational and fitness-support application. AI-generated fitness and nutrition recommendations may contain errors and should be evaluated using appropriate professional judgment.
Author
Omkar Mhaske
GitHub: https://github.com/Omkar143256
LinkedIn: https://www.linkedin.com/in/omkarmhaske14
