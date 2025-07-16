# 📘 AskEDU – AI-Powered Interactive Learning Assistant

*Intelunnati Project 2025 Submission*  
*Team Name:* Bugslayers  
*Theme:* AI for Education  
*Submission Date:* 12 July 2025  

AskEDU is a real-time, AI-powered learning assistant that supports classroom education through multimodal input (text, voice, image, PDF, webcam) and emotionally adaptive responses. It’s built to help students learn better and teachers teach smarter.

---

## 🧠 Core Features

- ✅ *Multimodal AI Assistant* – Accepts queries via text, voice, image, or webcam.
- 🎭 *Emotion Detection* – Adjusts explanations based on facial expressions.
- 📚 *Storytelling & Concept Remix* – Converts boring topics into fun formats (raps, stories, comics).
- 📊 *Quiz Generator* – Auto-creates quizzes with feedback.
- 👩‍🏫 *Teacher Tools* – Attendance, announcements, Zoom scheduler, behavior notes.
- 👨‍🎓 *Student Dashboard* – Pinboard, mentors, progress tracking.
- 💬 *Mentor Chat* – Different AI personalities: Chill, Strict, Anime.
- 📷 *Classroom Recorder* – Upload lectures, auto-generate notes and quizzes.
- 🔍 *Plagiarism Checker* – Detects text similarity and offers suggestions.
- 💡 *Homework Helper* – Q&A, code debugging, creative output, and more.

---

## 🧱 Tech Stack

| Layer        | Tools Used |
|--------------|------------|
| *Frontend* | React, HTML, JS, Tailwind CSS |
| *Backend*  | Django, Flask, Convex |
| *Auth*     | Firebase Authentication |
| *AI/ML*    | Gemini API, OpenAI (GPT-4, Whisper), Google TTS, Mediapipe, OpenCV |
| *Database* | SQLite, PostgreSQL |
| *Deployment* | Firebase |
| *Other* |  Chart.js, Timeline.js |

---

## 📂 Project Structure


AskEDU/
├── authentication/              
│   ├── login/                   
│   └── register/                
│
├── student_dashboard/          
│   ├── quiz_engine/           
│   ├── mentor_chat/            
│   ├── visual_aid_generator/   
│   ├── storytelling_mode/      
│   ├── homework_helper/        
│   ├── remix_studio/           
│   ├── pinboard/              
│   ├── plagiarism_checker/     
│   └── emotion_tracker/        
│
├── teacher_dashboard/          
│   ├── classroom_recorder/     
│   ├── attendance_tracker/     
│   ├── behavior_notes/         
│   ├── announcement_board/     
│   ├── zoom_scheduler/         
│   └── student_manager/        
│
├── group_study_matchmaker/          
│   ├── matchmaker/   
│ 
└── common/
    ├── api_services/           
    ├── utils/                  
    └── templates/              


---

## 👥 Team Members

- [*Khushi Saraswat* (Team Leader)](https://github.com/Khushi-saraswat-007)
- [Ayushi Sharma](https://github.com/Ayushi536)
- [Kritika Kanchan](https://github.com/Kritika-Kanchan-dev)
- [Kratika Rathi](https://github.com/kratikarathi123)
- [Harshita Bansal](https://github.com/Harshitabansal123)

---
## 👩‍💻 Team Member Contributions

Organized by Name:

---

🔹 *Khushi Saraswat*  
- Storytelling Mode  
- Visual Aid Generator   
- Teacher Dashboard (Attendance, Behavior, Zoom)  
- Student Dashboard  
- Firebase Role-Based Authentication  
Designed for structured classroom management and AI-generated academic content delivery.

---

🔹 *Ayushi Sharma*  
- Mentor-Specific Chat with History + Reset  
- Quiz Generation  
- AI Suggestions + Leaderboard (based on weak areas)  
- Group Study Match Chatroom  
Focused on crafting engagement-centered learning tools, combining AI mentoring, performance tracking, and real-time collaboration features to enrich the overall student experience within AskEDU.

---

🔹 *Kritika Kanchan*  
- Landing Page (Animated & Responsive)  
- Multimodal AI Assistant  
- AI Code Assistant  
- Classroom Recorder  
- Pinboard (TTS + Tone + Saved Concepts)  
Handled all technical integrations related to diverse AI input types and creative learning support tools.


---

🔹 *Kratika Rathi*  
- Homework Helper Suite  
- Plagiarism Checker  
- Attention Recognition System (Facial Tracking)  
- Login/Signup Form UI  
Focused on performance-driven tools, facial tracking, and user-side access components.

---

🔹 *Harshita Bansal*  
- Teaching Mode (Learn by Teaching)  
- Concept Remix Studio  
- Historical Time Machine  
Focused on creative, feedback-driven, and immersive modules to promote self-expression and exploration in learning.

---

## ✅ Sample Use Cases

- A student uploads a handwritten math problem → Receives AI-generated explanation with diagram.
- A student looks confused → Emotion engine simplifies the answer automatically.
- A teacher uploads a lecture video → Notes + quiz generated.
- A student saves a topic in the pinboard → Gets it later in cartoon-style narration.

---

## 🧪 Testing & Performance

| Action | Response Time |
|--------|----------------|
| Text Query → Answer | ~3.2 sec |
| Voice Input → Answer | ~3.5 sec |
| Image Upload → Answer | ~2.8 sec |
| Quiz Generation | 5–8 sec |
| Emotion Detection | <2.5 sec |
| Dashboard Load | ~1.2 sec |

All core functionalities passed black-box and component tests.

---

## 🧭 Future Enhancements

- 📱 Mobile App (Android/iOS)
- 🌐 LMS Integrations (Moodle, Google Classroom)
- 🗣 Voice narrator customization
- 🧠 Adaptive Learning Paths
- 🔐 Privacy & parental controls
- 🎨 Collaborative whiteboard
- 📈 Analytics for teachers

---

## 📘 References

- [Gemini API (Google)](https://ai.google.dev)
- [OpenAI GPT & Whisper](https://platform.openai.com)
- [Django](https://www.djangoproject.com)
- [React](https://reactjs.org)
- [Firebase](https://firebase.google.com/)
- [Mediapipe](https://github.com/google/mediapipe)
- [Tailwind CSS](https://tailwindcss.com/)

---

## 🏁 Conclusion

AskEDU was built to reshape how students learn and teachers teach. It’s more than a project – it’s a scalable, AI-powered education companion ready for the classroom of tomorrow.

## 🔴 Note:

The group_study_matchmaker/ folder contains an independently runnable sub-project focused on group study matching logic. Although it is currently not integrated into the main AskEDU system, it functions correctly on its own and may be merged in future iterations.

> “AskEDU listens, adapts, and responds — just like a real teacher would.”
