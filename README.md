# MarketMind

MarketMind is a smart digital marketing platform built for small and medium businesses that struggle to manage marketing, payments, and customer engagement across multiple tools. It brings automation, AI-powered content generation, and real-time insights into one unified web application.

---

##  Project Purpose

MarketMind aims to help businesses grow their digital presence effortlessly by offering:

- Automated scheduling of posts across multiple social platforms  
- AI-generated personalized marketing content  
- Real-time marketing analytics and performance tracking  
- AI-powered FAQ assistant using RAG (Retrieval-Augmented Generation)  
- Secure, fast payments using Stripe or QR-based transactions  

The platform reduces manual marketing work, improves consistency, and provides all-in-one tools to support business growth.

---

##  Tech Stack

| Component | Technology |
|----------|------------|
| **Frontend** | React/Next.js, Redux, TailwindCSS |
| **Backend** | FastAPI |
| **Database** | PostgreSQL + pgvector |
| **Authentication** | Supabase (JWT-based) |
| **AI/NLP** | OpenAI / Google Gemini APIs |
| **Payments** | Stripe + QR Code Payments |
| **Hosting** | Vercel / Render |
| **Version Control** | GitHub |
| **Deployment** | Cloud-based CI/CD pipeline |

---

##  How to Run the Project

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/marketmind.git
cd marketmind
```

---

### 2. Run the Backend (FastAPI)

#### Install dependencies:
```bash
cd backend
pip install -r requirements.txt
```

#### Start FastAPI server:
```bash
uvicorn main:app --reload
```

Backend will run on:  
`http://127.0.0.1:8000`

---

### 3. Run the Frontend (React/Next.js)

#### Install dependencies:
```bash
cd frontend
npm install
```

#### Start development server:
```bash
npm run dev
```

Frontend will run on:  
`http://localhost:3000`

---

### 4. Environment Variables Needed

Create `.env` files for both frontend and backend. Example variables:

#### Backend `.env`
```
DATABASE_URL=postgresql://user:password@localhost:5432/marketmind
OPENAI_API_KE
