# Multi-Agent Resume Analyzer

This project is a sophisticated **CrewAI-based system** designed to help candidates optimize their resumes for specific job opportunities. It employs a team of AI agents to analyze your resume, dissect the job description, and provide a detailed match assessment with actionable advice.

## 🚀 How It Works

The system orchestrates a sequential workflow involving three specialized AI agents:

### 🤖 The Agents

1.  **Senior Resume Analyst** (`resume_analyzer`)
    *   **Role:** Experienced HR Specialist.
    *   **Goal:** Deeply analyzes your resume to extract technical skills, soft skills, work experience, and industry keywords.
    *   **Tools:** `Resume File Parser` (reads local resume files).

2.  **Job Requirements Specialist** (`job_description_analyzer`)
    *   **Role:** Talent Acquisition Expert.
    *   **Goal:** Scrutinizes the job description to distinguish between "must-have" requirements and "nice-to-have" preferences.
    *   **Tools:** `Job URL Scraper` (extracts content from job postings).

3.  **Career Match Advisor** (`match_advisor`)
    *   **Role:** Professional Resume Coach.
    *   **Goal:** Synthesizes the findings to calculate a **Fit Score (0-100)**, identify skill gaps, and offer specific resume improvement suggestions.

## 🛠️ Tools

The agents are equipped with custom tools to interact with the real world:

*   **Resume File Parser:** Reads and extracts text content from local resume files.
*   **Job URL Scraper:** Fetches and cleans job description text from a provided URL.

## 🏃‍♂️ How to Run

1.  Ensure your .env file or environment variables are set with your provider keys
2.  Clone the repository:
    ```bash
    git clone https://github.com/Erenuo/Multi-Agent-Resume-Analyzer-with-CrewAI.git
    cd Multi-Agent-Resume-Analyzer-with-CrewAI
    ```
4.  Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```
6.  Run the main script:
    ```bash
    python src/resume_analyzer/main.py
    ```
7.  Follow the prompts to enter the **path to your resume** and the **URL of the job description**.

## 📄 Output

The system will generate a comprehensive report including:
*   **Fit Score:** A quantitative measure of your compatibility.
*   **Matching Skills:** Where you align with the role.
*   **Missing Skills:** Critical gaps to address.
*   **Improvement Suggestions:** Actionable steps to increase your chances of getting an interview.
