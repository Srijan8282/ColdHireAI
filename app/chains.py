import os
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()


class Chain:
    def __init__(self):
        self.llm = ChatGroq(
            temperature=0.3,
            groq_api_key=os.getenv("GROQ_API_KEY"),
            model_name="llama-3.3-70b-versatile",
        )
        self.llm_precise = ChatGroq(
            temperature=0.0,
            groq_api_key=os.getenv("GROQ_API_KEY"),
            model_name="llama-3.3-70b-versatile",
        )

    # ── Extract Jobs ──────────────────────────────────────────────────────────
    def extract_jobs(self, cleaned_text):
        prompt_extract = PromptTemplate.from_template(
            """
            ### SCRAPED TEXT FROM WEBSITE:
            {page_data}
            ### INSTRUCTION:
            The scraped text is from the career page of a website.
            Extract the job postings and return them in JSON format with keys:
            `role`, `experience`, `skills`, `description`, `company`, `location`, `salary`
            (use null if not available).
            Only return valid JSON.
            ### VALID JSON (NO PREAMBLE):
            """
        )
        chain_extract = prompt_extract | self.llm_precise
        res = chain_extract.invoke(input={"page_data": cleaned_text})
        try:
            json_parser = JsonOutputParser()
            res = json_parser.parse(res.content)
        except OutputParserException:
            raise OutputParserException("Context too big. Unable to parse jobs.")
        return res if isinstance(res, list) else [res]

    def write_mail(self, job, links, tone="Professional",
               name="Alex", role="Business Development Executive"):
        tone_guide = {
            "Professional": "formal, polished, and respectful.",
            "Friendly":     "warm, approachable, and conversational. Use a personal touch.",
            "Confident":    "assertive and bold. Emphasise your value strongly.",
            "Concise":      "brief and to the point. Use short sentences.",
            "Storytelling": "narrative-driven, open with a relatable insight before pitching.",
        }
        tone_instruction = tone_guide.get(tone, tone_guide["Professional"])

        prompt_email = PromptTemplate.from_template(
            """
            ### JOB DESCRIPTION:
            {job_description}

            ### INSTRUCTION:
            You are {name}, a {role} who is looking for a career switch and targeting this company.

            Write a cold outreach email to someone at this company (could be a recruiter, hiring manager,
            or an employee) asking for a referral or expressing strong interest in this role.

            The email should:
            - Feel personal, human, and genuine — NOT like a corporate pitch
            - Briefly introduce who you are and your background
            - Show specific enthusiasm for THIS company and THIS role (mention role details)
            - Mention 1-2 relevant skills or experiences that make you a strong fit
            - Politely ask for a referral OR request a short chat/call
            - Be respectful of their time — keep it concise
            - If relevant, mention these portfolio/work links naturally: {link_list}

            Tone: {tone_instruction}

            Important:
            - Start with "Subject: " on line 1
            - Blank line
            - Then the email body
            - Sign off warmly as {name}
            - Do NOT mention any current employer or consulting company
            - Do NOT sound like a sales pitch
            - No preamble or meta-commentary

            ### EMAIL:
            """
        )
        chain_email = prompt_email | self.llm
        res = chain_email.invoke({
            "job_description":  str(job),
            "link_list":        links,
            "name":             name,
            "role":             role,
            "tone_instruction": tone_instruction,
        })
        return res.content
    


    # ── Cover Letter ──────────────────────────────────────────────────────────
    def write_cover_letter(self, job, candidate_info: dict):
        prompt = PromptTemplate.from_template(
            """
            ### JOB DESCRIPTION:
            {job_description}

            ### CANDIDATE INFO:
            Name: {name}
            Current Role: {current_role}
            Skills: {skills}
            Years of Experience: {years_exp}
            Key Achievements: {achievements}

            ### INSTRUCTION:
            Write a professional, compelling cover letter for this job application.
            - 3-4 paragraphs
            - Opening: hook with enthusiasm and relevance
            - Middle: match skills/experience to job requirements
            - Closing: strong call to action
            - Formal but engaging tone
            - Address to "Hiring Manager"

            ### COVER LETTER (NO PREAMBLE):
            """
        )
        chain = prompt | self.llm
        res = chain.invoke({
            "job_description": str(job),
            "name":            candidate_info.get("name", "Candidate"),
            "current_role":    candidate_info.get("current_role", "Professional"),
            "skills":          ", ".join(candidate_info.get("skills", [])),
            "years_exp":       candidate_info.get("years_exp", "several years"),
            "achievements":    candidate_info.get("achievements", "Various industry achievements"),
        })
        return res.content

    # ── Interview Prep ────────────────────────────────────────────────────────
    def generate_interview_questions(self, job, question_type="mixed"):
        type_guide = {
            "technical":   "Focus on technical and coding questions relevant to the skills required.",
            "behavioral":  "Focus on STAR-format behavioral questions.",
            "situational": "Focus on situational and case-study questions.",
            "mixed":       "Include a mix of technical, behavioral, and situational questions.",
        }
        prompt = PromptTemplate.from_template(
            """
            ### JOB DESCRIPTION:
            {job_description}

            ### INSTRUCTION:
            Generate 8 interview questions for this role.
            Type: {type_guide}

            Return JSON array with this structure:
            [
              {{
                "question": "...",
                "type": "technical|behavioral|situational",
                "difficulty": "easy|medium|hard",
                "tip": "brief answering tip"
              }}
            ]
            ### VALID JSON ARRAY (NO PREAMBLE):
            """
        )
        chain = prompt | self.llm_precise
        res = chain.invoke({
            "job_description": str(job),
            "type_guide":      type_guide.get(question_type, type_guide["mixed"]),
        })
        try:
            return JsonOutputParser().parse(res.content)
        except Exception:
            return []

    # ── Job Fit Analyser ──────────────────────────────────────────────────────
    def analyse_job_fit(self, job, candidate_skills: list, candidate_exp: str):
        prompt = PromptTemplate.from_template(
            """
            ### JOB DESCRIPTION:
            {job_description}

            ### CANDIDATE PROFILE:
            Skills: {candidate_skills}
            Experience: {candidate_exp}

            ### INSTRUCTION:
            Analyse how well this candidate fits the job.
            Return JSON:
            {{
              "fit_score": <0-100 integer>,
              "matching_skills": ["skill1", ...],
              "missing_skills": ["skill1", ...],
              "strengths": ["strength1", ...],
              "gaps": ["gap1", ...],
              "recommendation": "short paragraph of advice",
              "verdict": "Strong Fit | Good Fit | Partial Fit | Weak Fit"
            }}
            ### VALID JSON (NO PREAMBLE):
            """
        )
        chain = prompt | self.llm_precise
        res = chain.invoke({
            "job_description":  str(job),
            "candidate_skills": ", ".join(candidate_skills),
            "candidate_exp":    candidate_exp,
        })
        try:
            return JsonOutputParser().parse(res.content)
        except Exception:
            return {
                "fit_score": 0, "verdict": "Analysis failed",
                "recommendation": res.content,
                "matching_skills": [], "missing_skills": [],
                "strengths": [], "gaps": [],
            }

    # ── Summarise Job ─────────────────────────────────────────────────────────
    def summarise_job(self, job):
        prompt = PromptTemplate.from_template(
            """
            ### JOB:
            {job}

            ### INSTRUCTION:
            Give a crisp summary. Return JSON:
            {{
              "tldr": ["point1", "point2", "point3"],
              "culture_hints": ["hint1", "hint2"],
              "red_flags": ["flag1"]
            }}
            ### VALID JSON (NO PREAMBLE):
            """
        )
        chain = prompt | self.llm_precise
        res = chain.invoke({"job": str(job)})
        try:
            return JsonOutputParser().parse(res.content)
        except Exception:
            return {"tldr": [], "culture_hints": [], "red_flags": []}

    # ── Salary Negotiation Script ─────────────────────────────────────────────
    def generate_salary_script(self, job, current_salary: str, expected_salary: str):
        prompt = PromptTemplate.from_template(
            """
            ### JOB DESCRIPTION:
            {job_description}

            ### CONTEXT:
            Current Salary: {current_salary}
            Expected Salary: {expected_salary}

            ### INSTRUCTION:
            Write a professional salary negotiation script/email the candidate can use
            after receiving a job offer. Include:
            - Opening acknowledgment of the offer
            - Diplomatic counter-offer with justification
            - Highlight value they bring (based on job skills)
            - Graceful closing that keeps the relationship positive
            Keep it confident, not aggressive.

            ### NEGOTIATION SCRIPT (NO PREAMBLE):
            """
        )
        chain = prompt | self.llm
        res = chain.invoke({
            "job_description":  str(job),
            "current_salary":   current_salary,
            "expected_salary":  expected_salary,
        })
        return res.content

    # ── LinkedIn Connection Note ──────────────────────────────────────────────
    def write_linkedin_note(self, job, name: str, company: str):
        prompt = PromptTemplate.from_template(
            """
            ### JOB DESCRIPTION:
            {job_description}

            ### SENDER:
            Name: {name}
            Company: {company}

            ### INSTRUCTION:
            Write a LinkedIn connection request note (max 300 characters) to the hiring manager
            for this role. Make it personal, relevant, and compelling. No hashtags.

            ### NOTE (NO PREAMBLE, UNDER 300 CHARS):
            """
        )
        chain = prompt | self.llm
        res = chain.invoke({"job_description": str(job), "name": name, "company": company})
        return res.content.strip()

    # ── Generic Chat ──────────────────────────────────────────────────────────
    def chat_generic(self, user_message: str, history: list) -> str:
        """General cold email / career assistant — no job context."""
        system = (
            "You are ColdHire AI, an expert assistant specialising in cold email outreach, "
            "job hunting strategy, professional communication, portfolio presentation, "
            "interview preparation, salary negotiation, and career development.\n"
            "Give practical, actionable, concise advice. Be encouraging and professional.\n"
            "Use markdown formatting (bold, bullets) when helpful."
        )
        conversation = _build_history(history)
        prompt = PromptTemplate.from_template(
            "{system}\n\n### CONVERSATION:\n{conversation}User: {message}\nColdHire AI:"
        )
        res = (prompt | self.llm).invoke({
            "system": system, "conversation": conversation, "message": user_message,
        })
        return res.content.strip()

    # ── Job-Specific Chat ─────────────────────────────────────────────────────
    def chat_job(self, user_message: str, history: list, job: dict) -> str:
        """Answers questions specifically about the loaded job description."""
        system = (
            "You are ColdHire AI, a specialist assistant. "
            "Answer questions ONLY based on the job description provided below. "
            "If the answer isn't in the job description, say so clearly. "
            "Be precise and cite specific details from the job posting. "
            "Use markdown formatting (bold, bullets) when helpful."
        )
        job_context = (
            f"Role: {job.get('role', 'N/A')}\n"
            f"Company: {job.get('company', 'N/A')}\n"
            f"Location: {job.get('location', 'N/A')}\n"
            f"Experience: {job.get('experience', 'N/A')}\n"
            f"Skills Required: {', '.join(job.get('skills', []))}\n"
            f"Salary: {job.get('salary', 'Not mentioned')}\n"
            f"Description: {str(job.get('description', ''))[:2000]}"
        )
        conversation = _build_history(history)
        prompt = PromptTemplate.from_template(
            "{system}\n\n### JOB DESCRIPTION:\n{job_context}\n\n"
            "### CONVERSATION:\n{conversation}User: {message}\nColdHire AI:"
        )
        res = (prompt | self.llm).invoke({
            "system":       system,
            "job_context":  job_context,
            "conversation": conversation,
            "message":      user_message,
        })
        return res.content.strip()


# ── Helper ────────────────────────────────────────────────────────────────────
def _build_history(history: list, limit: int = 8) -> str:
    out = ""
    for msg in history[-limit:]:
        label = "User" if msg["role"] == "user" else "ColdHire AI"
        out += f"{label}: {msg['content']}\n"
    return out


if __name__ == "__main__":
    print(os.getenv("GROQ_API_KEY"))