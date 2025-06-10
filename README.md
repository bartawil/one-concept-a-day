# One Concept a Day

A learning platform that delivers one educational concept per day based on your interests.

## Overview

This application helps users learn new concepts daily in their areas of interest. Users can register, select their learning interests, receive daily concept explanations, and track their learning progress.

## Tech Stack

- **Frontend**: React + TypeScript + Vite + TailwindCSS
- **Backend**: FastAPI + Python
- **Database**: MongoDB
- **AI**: Integration for concept generation

## Quick Start

### Prerequisites
- Node.js (v18+)
- Python (3.11+)
- MongoDB instance

### Installation

1. Clone and setup:
```bash
git clone <repo-url>
cd one-concept-a-day
npm install
```

2. Backend setup:
```bash
cd server
python -m venv venv311
source venv311/bin/activate
pip install -r requirements.txt
```

3. Frontend setup:
```bash
cd ../client
npm install
```

4. Environment configuration:

- `server/.env` - Database and API keys
- `client/.env` - API URL

### Running

Development mode (both frontend & backend):
```bash
npm run dev
```

Or separately:
```bash
npm run server  # Backend only
npm run client  # Frontend only
```

Access:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000

## Project Structure

```
one-concept-a-day/
├── client/          # React frontend
├── server/          # FastAPI backend
├── package.json     # Root project configuration
└── README.md
```