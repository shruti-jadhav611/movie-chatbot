# Movie Chatbot

This is a full-stack movie chatbot application built using React for the frontend, Node.js with Express for the backend, and Python for handling machine learning model predictions. The chatbot allows users to ask about movie stories, cast members, and receive movie recommendations based on similarity.

---

## Features

- Ask about movie plots, characters, and cast members
- Get intelligent movie recommendations
- Uses a machine learning model with precomputed similarity data
- React-based responsive UI with modern design
- Communicates between Node.js and Python using child processes
- Deployed using Render (frontend and backend independently)

---

## Technologies Used

### Frontend

- React
- CSS (custom gradients and layout)

### Backend

- Node.js
- Express
- Python (for model execution)
- child_process module

### ML & Data

- Precomputed `.pkl` files (`similarity.pkl`, `movies.pkl`)
- TMDB dataset used to train the recommendation model

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/movie-chatbot.git
cd movie-chatbot
