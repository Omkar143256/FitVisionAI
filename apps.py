from google import genai
from google.genai import types
import streamlit as st
from prompts import SYSTEM_PROMPT


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="FitVision AI",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# GEMINI CONFIGURATION
# ============================================================

API_KEY = st.secrets.get("GEMINI_API_KEY")

if not API_KEY:
    st.error("Gemini API key is not configured.")
    st.stop()

client = genai.Client(api_key=API_KEY)

MODEL_NAME = "gemini-2.5-flash"


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

    .stApp {
        background-color: #0B0F14;
        color: white;
    }

    [data-testid="stHeader"] {
        background-color: transparent;
    }

    .main-title {
        font-size: 48px;
        font-weight: 800;
        text-align: center;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        color: #9AA4B2;
        font-size: 18px;
        margin-bottom: 35px;
    }

    .card {
        background: #151B23;
        border: 1px solid #242B35;
        border-radius: 18px;
        padding: 24px;
        margin-bottom: 18px;
    }

    .metric-card {
        background: #151B23;
        border: 1px solid #242B35;
        border-radius: 16px;
        padding: 20px;
        text-align: center;
    }

    .metric-number {
        font-size: 30px;
        font-weight: 800;
        color: #7CFF6B;
    }

    .metric-label {
        color: #9AA4B2;
        font-size: 14px;
    }

    .section-title {
        font-size: 28px;
        font-weight: 750;
        margin-bottom: 15px;
    }

    .small-text {
        color: #9AA4B2;
    }

    .ai-message {
        background: #151B23;
        border-radius: 16px;
        padding: 18px;
        margin: 10px 0;
    }

    .welcome-box {
        background: linear-gradient(
            135deg,
            #151B23,
            #111820
        );
        border: 1px solid #242B35;
        border-radius: 24px;
        padding: 35px;
        text-align: center;
    }

    .stButton > button {
        border-radius: 12px;
        min-height: 42px;
        font-weight: 600;
    }

</style>
""", unsafe_allow_html=True)


# ============================================================
# SESSION STATE
# ============================================================

defaults = {
    "page": "signup",
    "onboarding_step": 1,
    "user": {},
    "messages": [],
    "logged_in": False,
    "onboarding_complete": False,
    "body_image": None,
    "body_analysis": None,
    "weekly_plan": None,
    "progress": {
        "workouts": 0,
        "streak": 0,
        "water": 0.0
    }
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def navigate(page):
    st.session_state.page = page
    st.rerun()


def get_profile_text():

    user = st.session_state.user

    return f"""
USER PROFILE

Name: {user.get("name", "User")}
Age: {user.get("age", "Not provided")}
Sex: {user.get("sex", "Not provided")}
Height: {user.get("height", "Not provided")} cm
Weight: {user.get("weight", "Not provided")} kg
Fitness Goal: {user.get("goal", "Not provided")}
Fitness Level: {user.get("fitness_level", "Not provided")}
Workout Days: {user.get("workout_days", "Not provided")}
Training Location: {user.get("location", "Not provided")}
Equipment: {user.get("equipment", "Not provided")}
Diet: {user.get("diet", "Not provided")}
Allergies: {user.get("allergies", "None")}
Physical Limitations: {user.get("limitations", "None")}
"""


def generate_ai_response(user_prompt, image=None):

    contents = [
        types.Part.from_text(
            text=f"""
USER PROFILE:
{get_profile_text()}

USER REQUEST:
{user_prompt}
"""
        )
    ]

    if image:

        contents.append(
            types.Part.from_bytes(
                data=image.getvalue(),
                mime_type=image.type
            )
        )

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=contents
    )

    return response.text


def generate_weekly_plan():

    prompt = """
Create a personalized 7-day fitness and nutrition plan.

Include:

1. Weekly workout schedule
2. Exercises
3. Sets and repetitions
4. Rest periods
5. Warm-up and cooldown
6. Weekly meal plan
7. Breakfast
8. Lunch
9. Snacks
10. Dinner
11. Hydration guidance

Use the user's profile.

Clearly identify nutritional and body-related values as estimates
when they cannot be determined precisely.

Do not diagnose medical conditions.
Do not recommend extreme diets or unsafe training.
"""

    return generate_ai_response(prompt)


# ============================================================
# SIGN UP PAGE
# ============================================================

def signup_page():

    st.markdown(
        '<div class="main-title">💪 FitVision AI</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Your AI-powered fitness coach'
        '</div>',
        unsafe_allow_html=True
    )

    left, center, right = st.columns([1, 1.2, 1])

    with center:

        st.markdown(
            """
            <div class="welcome-box">
                <h2>Start your fitness journey</h2>
                <p style="color:#9AA4B2;">
                Personalized workouts, nutrition and AI vision coaching.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.write("")

        name = st.text_input(
            "Full Name",
            placeholder="Enter your name"
        )

        email = st.text_input(
            "Email",
            placeholder="you@example.com"
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Create a password"
        )

        if st.button(
            "Create Account →",
            use_container_width=True
        ):

            if not name or not email or not password:

                st.warning(
                    "Please complete all fields."
                )

            else:

                st.session_state.user = {
                    "name": name,
                    "email": email
                }

                st.session_state.logged_in = True
                st.session_state.onboarding_step = 1
                st.session_state.page = "onboarding"

                st.rerun()

        st.markdown(
            """
            <div style="text-align:center;color:#9AA4B2;margin-top:20px;">
            Already have an account? <b>Sign In</b>
            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# ONBOARDING
# ============================================================

def onboarding_page():

    user = st.session_state.user
    step = st.session_state.onboarding_step

    st.progress(step / 5)

    st.markdown(
        '<div class="main-title" style="font-size:34px;">'
        "Let's build your fitness profile"
        "</div>",
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        f"Step {step} of 5"
        "</div>",
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # STEP 1
    # --------------------------------------------------------

    if step == 1:

        st.markdown(
            '<div class="section-title">'
            "🎯 What's your main goal?"
            "</div>",
            unsafe_allow_html=True
        )

        goal = st.radio(
            "Select one",
            [
                "🔥 Lose Fat",
                "💪 Build Muscle",
                "🏋️ Improve Strength",
                "🏃 Improve Endurance",
                "❤️ General Fitness",
                "🧘 Mobility & Flexibility"
            ],
            label_visibility="collapsed"
        )

        if st.button(
            "Continue →",
            use_container_width=True
        ):

            user["goal"] = goal
            st.session_state.onboarding_step = 2
            st.rerun()

    # --------------------------------------------------------
    # STEP 2
    # --------------------------------------------------------

    elif step == 2:

        st.markdown(
            '<div class="section-title">'
            "👤 About You"
            "</div>",
            unsafe_allow_html=True
        )

        age = st.number_input(
            "Age",
            13,
            100,
            18
        )

        sex = st.selectbox(
            "Sex (optional)",
            [
                "Prefer not to say",
                "Male",
                "Female",
                "Other"
            ]
        )

        height = st.number_input(
            "Height (cm)",
            100,
            250,
            170
        )

        weight = st.number_input(
            "Weight (kg)",
            30,
            300,
            65
        )

        fitness_level = st.selectbox(
            "Fitness Level",
            [
                "Beginner",
                "Intermediate",
                "Advanced"
            ]
        )

        if st.button(
            "Continue →",
            use_container_width=True
        ):

            user.update({
                "age": age,
                "sex": sex,
                "height": height,
                "weight": weight,
                "fitness_level": fitness_level
            })

            st.session_state.onboarding_step = 3
            st.rerun()

    # --------------------------------------------------------
    # STEP 3
    # --------------------------------------------------------

    elif step == 3:

        st.markdown(
            '<div class="section-title">'
            "🏋️ Your Training"
            "</div>",
            unsafe_allow_html=True
        )

        workout_days = st.slider(
            "How many days can you train?",
            1,
            7,
            4
        )

        location = st.selectbox(
            "Where do you train?",
            [
                "Home",
                "Gym",
                "Outdoors"
            ]
        )

        equipment = st.multiselect(
            "Available Equipment",
            [
                "Dumbbells",
                "Resistance Bands",
                "Barbell",
                "Machines",
                "Pull-up Bar",
                "No Equipment"
            ]
        )

        if st.button(
            "Continue →",
            use_container_width=True
        ):

            user.update({
                "workout_days": workout_days,
                "location": location,
                "equipment": ", ".join(equipment)
            })

            st.session_state.onboarding_step = 4
            st.rerun()

    # --------------------------------------------------------
    # STEP 4
    # --------------------------------------------------------

    elif step == 4:

        st.markdown(
            '<div class="section-title">'
            "🍎 Nutrition"
            "</div>",
            unsafe_allow_html=True
        )

        diet = st.radio(
            "Diet",
            [
                "Vegetarian",
                "Non-Vegetarian",
                "Vegan",
                "Other"
            ],
            horizontal=True
        )

        allergies = st.text_input(
            "Food allergies / restrictions",
            placeholder="Optional"
        )

        limitations = st.text_input(
            "Injuries / physical limitations",
            placeholder="Optional"
        )

        if st.button(
            "Continue →",
            use_container_width=True
        ):

            user.update({
                "diet": diet,
                "allergies": allergies,
                "limitations": limitations
            })

            st.session_state.onboarding_step = 5
            st.rerun()

    # --------------------------------------------------------
    # STEP 5
    # --------------------------------------------------------

    elif step == 5:

        st.markdown(
            '<div class="section-title">'
            "📸 Add your fitness profile"
            "</div>",
            unsafe_allow_html=True
        )

        st.write(
            "Upload a clear full-body image for optional "
            "AI vision-based fitness observations."
        )

        image = st.file_uploader(
            "Upload Image",
            type=[
                "jpg",
                "jpeg",
                "png"
            ]
        )

        if image:
            st.image(
                image,
                width=300
            )

        if st.button(
            "Complete Setup →",
            use_container_width=True
        ):

            st.session_state.body_image = image
            st.session_state.onboarding_complete = True
            st.session_state.page = "dashboard"

            st.rerun()


# ============================================================
# SIDEBAR NAVIGATION
# ============================================================

def sidebar():

    with st.sidebar:

        st.markdown("## 💪 FitVision AI")

        st.write(
            f"Hi, {st.session_state.user.get('name', 'User')} 👋"
        )

        st.divider()

        if st.button("🏠 Home", use_container_width=True):
            navigate("dashboard")

        if st.button("🤖 AI Coach", use_container_width=True):
            navigate("coach")

        if st.button("💪 Workouts", use_container_width=True):
            navigate("workouts")

        if st.button("🍎 Nutrition", use_container_width=True):
            navigate("nutrition")

        if st.button("📸 AI Vision", use_container_width=True):
            navigate("vision")

        if st.button("📊 Progress", use_container_width=True):
            navigate("progress")

        if st.button("👤 Profile", use_container_width=True):
            navigate("profile")

        st.divider()

        if st.button("🚪 Log Out", use_container_width=True):

            st.session_state.logged_in = False
            st.session_state.page = "signup"
            st.rerun()


# ============================================================
# DASHBOARD
# ============================================================

def dashboard():

    user = st.session_state.user

    st.markdown(
        f"""
        <div class="section-title">
        Good evening, {user.get("name", "User")} 👋
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write(
        "Here's your fitness overview for today."
    )

    # Today's workout
    st.markdown(
        """
        <div class="card">
        <h2>💪 Today's Workout</h2>
        <p class="small-text">
        Your personalized workout is ready.
        </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    c1, c2 = st.columns(2)

    with c1:

        if st.button(
            "▶ Start Workout",
            use_container_width=True
        ):
            navigate("workouts")

    with c2:

        if st.button(
            "🤖 Ask AI Coach",
            use_container_width=True
        ):
            navigate("coach")

    st.write("")

    # Metrics
    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(
            f"""
            <div class="metric-card">
            <div class="metric-number">
            {st.session_state.progress["streak"]}
            </div>
            <div class="metric-label">🔥 Day Streak</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c2:
        st.markdown(
            f"""
            <div class="metric-card">
            <div class="metric-number">
            {st.session_state.progress["workouts"]}
            </div>
            <div class="metric-label">💪 Workouts</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c3:
        st.markdown(
            f"""
            <div class="metric-card">
            <div class="metric-number">
            {st.session_state.progress["water"]:.1f}L
            </div>
            <div class="metric-label">💧 Water</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.write("")

    # Quick actions
    st.markdown(
        '<div class="section-title">Quick Actions</div>',
        unsafe_allow_html=True
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        if st.button(
            "💪 Today's Workout",
            use_container_width=True
        ):
            navigate("workouts")

    with c2:
        if st.button(
            "🍎 Today's Meals",
            use_container_width=True
        ):
            navigate("nutrition")

    with c3:
        if st.button(
            "📸 Analyze My Body",
            use_container_width=True
        ):
            navigate("vision")


# ============================================================
# AI COACH
# ============================================================

def coach():

    st.markdown(
        '<div class="section-title">'
        "🤖 FitVision AI Coach"
        "</div>",
        unsafe_allow_html=True
    )

    st.write(
        "Ask me about your workouts, nutrition, recovery or progress."
    )

    # Quick prompts
    c1, c2, c3 = st.columns(3)

    quick_prompt = None

    with c1:
        if st.button(
            "💪 Today's Workout",
            use_container_width=True
        ):
            quick_prompt = "What should my workout be today?"

    with c2:
        if st.button(
            "🍎 Today's Meals",
            use_container_width=True
        ):
            quick_prompt = "What should I eat today?"

    with c3:
        if st.button(
            "📅 Weekly Plan",
            use_container_width=True
        ):
            quick_prompt = "Create my personalized weekly fitness plan."

    # Chat history
    for message in st.session_state.messages:

        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    user_input = st.chat_input(
        "Ask your AI coach..."
    )

    if quick_prompt:
        user_input = quick_prompt

    if user_input:

        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })

        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):

            with st.spinner(
                "FitVision AI is thinking..."
            ):

                try:

                    answer = generate_ai_response(
                        user_input,
                        st.session_state.body_image
                    )

                    st.markdown(answer)

                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer
                    })

                except Exception as e:

                    st.error(
                        f"Unable to contact the AI: {e}"
                    )


# ============================================================
# WORKOUTS
# ============================================================

def workouts():

    st.markdown(
        '<div class="section-title">'
        "💪 Workout Plan"
        "</div>",
        unsafe_allow_html=True
    )

    user = st.session_state.user

    st.info(
        f"Goal: {user.get('goal', 'Not specified')} | "
        f"Level: {user.get('fitness_level', 'Not specified')} | "
        f"{user.get('workout_days', 'Not specified')} days/week"
    )

    if st.button(
        "✨ Generate Personalized Weekly Plan",
        use_container_width=True
    ):

        with st.spinner(
            "Creating your personalized plan..."
        ):

            try:

                plan = generate_weekly_plan()

                st.session_state.weekly_plan = plan

            except Exception as e:

                st.error(
                    f"Unable to generate plan: {e}"
                )

    if st.session_state.weekly_plan:

        st.markdown(
            st.session_state.weekly_plan
        )

    else:

        days = [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday"
        ]

        for day in days:

            with st.expander(day):

                st.write(
                    "Generate your personalized plan above "
                    "to populate this day."
                )


# ============================================================
# NUTRITION
# ============================================================

def nutrition():

    st.markdown(
        '<div class="section-title">'
        "🍎 Weekly Nutrition"
        "</div>",
        unsafe_allow_html=True
    )

    if st.button(
        "✨ Generate Weekly Diet Plan",
        use_container_width=True
    ):

        prompt = """
Create a practical 7-day nutrition plan for this user.

Include breakfast, lunch, snack and dinner for every day.

Respect the user's dietary preferences and restrictions.

Use practical foods that are reasonably available to the user.

Provide approximate nutrition values only when enough information
is available and clearly identify them as estimates.
"""

        with st.spinner(
            "Creating your nutrition plan..."
        ):

            try:

                result = generate_ai_response(prompt)

                st.session_state["nutrition_plan"] = result

            except Exception as e:

                st.error(
                    f"Unable to generate nutrition plan: {e}"
                )

    if "nutrition_plan" in st.session_state:

        st.markdown(
            st.session_state["nutrition_plan"]
        )

    else:

        st.info(
            "Generate your personalized weekly nutrition plan."
        )


# ============================================================
# VISION
# ============================================================

def vision():

    st.markdown(
        '<div class="section-title">'
        "📸 AI Vision"
        "</div>",
        unsafe_allow_html=True
    )

    st.write(
        "Upload a clear full-body image for AI-based "
        "fitness observations."
    )

    image = st.file_uploader(
        "Upload Body Image",
        type=[
            "jpg",
            "jpeg",
            "png"
        ],
        key="vision_upload"
    )

    if image:

        st.image(
            image,
            width=350
        )

        if st.button(
            "🔍 Analyze With AI",
            use_container_width=True
        ):

            prompt = """
Analyze the uploaded image for general fitness-related
observations.

Discuss only characteristics that can reasonably be observed.

Focus on:
- General visible posture
- General body proportions
- Potential fitness-training focus areas
- General exercise recommendations

Do not estimate exact body fat percentage, BMI, weight,
muscle mass or medical conditions from the image.

Clearly state that the observations are estimates and
that image analysis cannot replace professional assessment.
"""

            with st.spinner(
                "Analyzing image..."
            ):

                try:

                    result = generate_ai_response(
                        prompt,
                        image
                    )

                    st.session_state.body_analysis = result
                    st.session_state.body_image = image

                except Exception as e:

                    st.error(
                        f"Vision analysis failed: {e}"
                    )

    if st.session_state.body_analysis:

        st.markdown(
            "### AI Fitness Insight"
        )

        st.markdown(
            st.session_state.body_analysis
        )


# ============================================================
# PROGRESS
# ============================================================

def progress():

    st.markdown(
        '<div class="section-title">'
        "📊 Your Progress"
        "</div>",
        unsafe_allow_html=True
    )

    c1, c2, c3 = st.columns(3)

    with c1:

        workouts = st.number_input(
            "Completed Workouts",
            min_value=0,
            value=st.session_state.progress["workouts"]
        )

        st.session_state.progress["workouts"] = workouts

    with c2:

        streak = st.number_input(
            "Current Streak",
            min_value=0,
            value=st.session_state.progress["streak"]
        )

        st.session_state.progress["streak"] = streak

    with c3:

        water = st.number_input(
            "Water Today (L)",
            min_value=0.0,
            max_value=20.0,
            value=st.session_state.progress["water"],
            step=0.1
        )

        st.session_state.progress["water"] = water

    st.divider()

    st.markdown(
        "### 🏆 Weekly Focus"
    )

    st.write(
        "Stay consistent with your scheduled workouts, "
        "nutrition and recovery."
    )

    if st.button(
        "🤖 Ask AI to Analyze My Progress",
        use_container_width=True
    ):

        prompt = f"""
Analyze the user's current progress:

Completed workouts:
{workouts}

Current streak:
{streak}

Water today:
{water} liters

Provide concise fitness coaching feedback and suggestions
for maintaining consistency.
"""

        with st.spinner(
            "Analyzing progress..."
        ):

            try:

                result = generate_ai_response(prompt)

                st.markdown(result)

            except Exception as e:

                st.error(
                    f"Unable to analyze progress: {e}"
                )


# ============================================================
# PROFILE
# ============================================================

def profile():

    st.markdown(
        '<div class="section-title">'
        "👤 My Profile"
        "</div>",
        unsafe_allow_html=True
    )

    user = st.session_state.user

    for key, value in user.items():

        st.markdown(
            f"""
            <div class="card">
            <b>{key.replace("_", " ").title()}</b>
            <br>
            <span class="small-text">{value}</span>
            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# MAIN ROUTER
# ============================================================

if not st.session_state.logged_in:

    signup_page()

else:

    if not st.session_state.onboarding_complete:

        onboarding_page()

    else:

        sidebar()

        if st.session_state.page == "dashboard":
            dashboard()

        elif st.session_state.page == "coach":
            coach()

        elif st.session_state.page == "workouts":
            workouts()

        elif st.session_state.page == "nutrition":
            nutrition()

        elif st.session_state.page == "vision":
            vision()

        elif st.session_state.page == "progress":
            progress()

        elif st.session_state.page == "profile":
            profile()