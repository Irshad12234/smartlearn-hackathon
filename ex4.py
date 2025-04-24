import streamlit as st
import time
import random

# ---------------------------
# STUDY PLANNER SECTION
# ---------------------------
class Student:
    def __init__(self, name):
        self.name = name
        self.subjects = {}

    def add_subject(self, subject_name, proficiency):
        self.subjects[subject_name] = proficiency

    def generate_study_plan(self):
        st.subheader(f"\U0001F4DA Study Plan for {self.name}")
        if not self.subjects:
            st.info("No subjects added yet.")
            return

        sorted_subjects = sorted(self.subjects.items(), key=lambda x: x[1])
        for subject, proficiency in sorted_subjects:
            hours = (6 - proficiency) * 2
            st.write(f"**{subject}**: {hours} hrs/week")

    def adaptive_recommendation(self):
        st.subheader("\U0001F4C8 Adaptive Plan Suggestions")
        for subject, proficiency in self.subjects.items():
            if proficiency < 3:
                st.warning(f"Spend more time on **{subject}** — proficiency is low!")
            else:
                st.info(f"**{subject}** is in good shape. Maintain consistency.")

# ---------------------------
# DOUBT FORUM SECTION
# ---------------------------
class DoubtForum:
    def __init__(self):
        self.questions = []
        self.answers = {}

    def post_question(self, user, question):
        q_id = len(self.questions)
        self.questions.append((q_id, user, question))
        self.answers[q_id] = []
        return q_id

    def answer_question(self, user, q_id, answer):
        if q_id in self.answers:
            self.answers[q_id].append((user, answer))
        else:
            st.warning("Invalid Question ID")

    def view_questions(self):
        for q_id, user, question in self.questions:
            st.write(f"**{q_id}. {question}** _(Asked by {user})_")

    def view_answers(self, q_id):
        if q_id in self.answers:
            st.write(f"### Answers for Question {q_id}:")
            for user, ans in self.answers[q_id]:
                st.write(f"- **{user}**: {ans}")
        else:
            st.warning("No such question.")

# ---------------------------
# POMODORO SECTION
# ---------------------------
def pomodoro_timer():
    st.subheader("⏱️ Pomodoro Timer")
    work_duration = st.number_input("Work Duration (minutes):", 1, 60, 25, key="pomodoro_work")
    break_duration = st.number_input("Break Duration (minutes):", 1, 30, 5, key="pomodoro_break")
    cycles = st.number_input("Number of Cycles:", 1, 10, 4, key="pomodoro_cycles")

    if st.button("Start Pomodoro"):
        for i in range(cycles):
            st.success(f"Cycle {i+1}: Work for {work_duration} minutes")
            time.sleep(1)
            st.info(f"Break Time: {break_duration} minutes")
            time.sleep(1)
        st.balloons()
        st.success("All Pomodoro cycles completed!")

# ---------------------------
# AI SUGGESTION BOT
# ---------------------------
def ai_suggestions():
    st.subheader("\U0001F916 AI Study Bot Suggestions")
    tips = [
        "Review notes after each class.",
        "Use active recall and spaced repetition.",
        "Teach someone else to better understand the topic.",
        "Use flashcards for quick revision.",
        "Take regular breaks to avoid burnout."
    ]
    st.write(random.choice(tips))

# ---------------------------
# GAMIFIED PROGRESS TRACKER
# ---------------------------
class ProgressTracker:
    def __init__(self):
        self.points = 0
        self.level = 1

    def update_progress(self, action):
        action_points = {
            "study": 10,
            "answer": 5,
            "ask": 2
        }
        self.points += action_points.get(action, 0)
        self.level = 1 + self.points // 50

    def display_progress(self):
        st.subheader("\U0001F3C6 Gamified Progress")
        st.write(f"Points: {self.points}")
        st.write(f"Level: {self.level}")

# ---------------------------
# STREAMLIT UI
# ---------------------------
st.title("\U0001F4D6 Smart Study Planner + Forum + Pomodoro + AI Bot + Gamification")

if "student" not in st.session_state:
    st.session_state.student = Student("")

if "forum" not in st.session_state:
    st.session_state.forum = DoubtForum()

if "tracker" not in st.session_state:
    st.session_state.tracker = ProgressTracker()

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "\U0001F4C5 Planner", "\U0001F4AC Forum", "⏱️ Pomodoro", "\U0001F4C8 Adaptive Plan", "\U0001F916 AI Bot", "\U0001F3C6 Progress Tracker"
])

# ---------------------------
# TAB 1: Study Planner
# ---------------------------
with tab1:
    st.header("Create Your Study Plan")
    name = st.text_input("Your Name", value=st.session_state.student.name, key="planner_name")
    subject = st.text_input("Subject", key="planner_subject")
    proficiency = st.slider("Proficiency (1 = weak, 5 = strong)", 1, 5, 3, key="planner_proficiency")

    if st.button("Add Subject"):
        if name:
            st.session_state.student.name = name
            st.session_state.student.add_subject(subject, proficiency)
            st.session_state.tracker.update_progress("study")
            st.success(f"Added {subject} with proficiency {proficiency}")
        else:
            st.warning("Please enter your name.")

    if st.button("Generate Study Plan"):
        st.session_state.student.generate_study_plan()

# ---------------------------
# TAB 2: Doubt Forum
# ---------------------------
with tab2:
    st.header("Ask and Answer Questions")

    st.subheader("Ask a Question")
    q_user = st.text_input("Your Name (for Question)", key="forum_q_user")
    question = st.text_area("Your Question", key="forum_q_text")

    if st.button("Post Question"):
        if q_user and question:
            q_id = st.session_state.forum.post_question(q_user, question)
            st.session_state.tracker.update_progress("ask")
            st.success(f"Question posted with ID: {q_id}")
        else:
            st.warning("Name and question cannot be empty.")

    st.subheader("Answer a Question")
    a_user = st.text_input("Your Name (for Answer)", key="forum_a_user")
    q_id_to_answer = st.number_input("Question ID to Answer", min_value=0, step=1, key="forum_qid_input")
    answer = st.text_area("Your Answer", key="forum_a_text")

    if st.button("Submit Answer"):
        st.session_state.forum.answer_question(a_user, int(q_id_to_answer), answer)
        st.session_state.tracker.update_progress("answer")
        st.success("Answer submitted!")

    st.subheader("All Questions")
    st.session_state.forum.view_questions()

    q_id_view = st.number_input("Enter Question ID to View Answers", min_value=0, step=1, key="forum_view_qid")
    if st.button("Show Answers"):
        st.session_state.forum.view_answers(int(q_id_view))

# ---------------------------
# TAB 3: Pomodoro Timer
# ---------------------------
with tab3:
    pomodoro_timer()

# ---------------------------
# TAB 4: Adaptive Planner
# ---------------------------
with tab4:
    st.session_state.student.adaptive_recommendation()

# ---------------------------
# TAB 5: AI Suggestion Bot
# ---------------------------
with tab5:
    ai_suggestions()

# ---------------------------
# TAB 6: Gamified Progress Tracker
# ---------------------------
with tab6:
    st.session_state.tracker.display_progress()
