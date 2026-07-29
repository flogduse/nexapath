"""
NexaPath AI Career Agent
An autonomous, conversational AI agent that guides users through
career exploration, skill gap analysis, and learning recommendations.
Aligned with SDG 4 (Quality Education), SDG 8 (Decent Work), SDG 10 (Reduced Inequalities).
"""

import json
import random
import re
from datetime import datetime


class CareerAgent:
    """
    Autonomous AI Career Agent that:
    - Conducts conversational career guidance
    - Autonomously decides next actions (tools)
    - Chains capabilities: profile -> match -> gap -> courses
    - Adapts responses based on user input
    """

    def __init__(self, job_matcher):
        self.matcher = job_matcher
        self.conversation_state = {}
        self.session_log = []

        # Available tools the agent can autonomously invoke
        self.tools = {
            "match_jobs": self._tool_match_jobs,
            "skill_gap_analysis": self._tool_skill_gap,
            "get_courses": self._tool_get_courses,
            "career_advice": self._tool_career_advice,
            "city_info": self._tool_city_info,
        }

        # Intent detection patterns
        self.intent_patterns = {
            "greeting": r"\b(hi|hello|hey|namaste|good\s*(morning|afternoon|evening))\b",
            "job_search": r"\b(find|search|match|recommend|suggest|show)\b.*\b(jobs?|career|role|position|opportunity)\b",
            "skill_gap": r"\b(skill|gap|missing|need|learn|improve|course|training)\b",
            "salary": r"\b(salary|pay|compensation|earn|income|package|lpa)\b",
            "career_advice": r"\b(advice|suggest|recommend|guidance|what\s*should|which\s*career|path|roadmap)\b",
            "city_info": r"\b(city|location|remote|relocate|tier)\b",
            "help": r"\b(help|what\s*can|how\s*do|options|menu|commands)\b",
            "resume": r"\b(resume|cv|portfolio|profile)\b",
            "thank": r"\b(thank|thanks|bye|goodbye|see\s*you|exit)\b",
        }

        # Greeting responses
        self.greetings = [
            "Welcome to NexaPath! I'm your AI Career Copilot. I'll help you discover the best career path based on your skills and location. Ready to get started?",
            "Hey there! I'm NexaPath AI - your personal career coach for Tier-2/3 India. I can find jobs, analyze skill gaps, and suggest courses. What brings you here today?",
            "Namaste! Welcome to NexaPath. I'm here to bridge the opportunity gap for you. Let's start - what skills do you have?",
        ]

        # SDG-aligned messages
        self.sdg_messages = {
            "SDG 4": "NexaPath supports SDG 4 (Quality Education) by recommending personalized learning paths.",
            "SDG 8": "NexaPath supports SDG 8 (Decent Work) by connecting talent with opportunities in Tier-2/3 cities.",
            "SDG 10": "NexaPath supports SDG 10 (Reduced Inequalities) by reducing the opportunity gap between metro and non-metro talent.",
        }

    def _detect_intent(self, user_input):
        """Detect user intent from input text."""
        user_input_lower = user_input.lower()
        detected = []

        for intent, pattern in self.intent_patterns.items():
            if re.search(pattern, user_input_lower):
                detected.append(intent)

        if not detected:
            detected.append("unknown")

        return detected

    def _extract_skills(self, user_input):
        """Extract skill mentions from user input."""
        user_input_lower = user_input.lower()
        found_skills = []

        for skill in self.matcher.all_skills:
            pattern = r'\b' + re.escape(skill.lower()) + r'\b'
            if re.search(pattern, user_input_lower):
                found_skills.append(skill)

        skill_aliases = {
            r"\bjs\b": "javascript", r"\bts\b": "typescript", r"\bpy\b": "python",
            r"\bml\b": "machine learning", r"\bdl\b": "deep learning",
            r"\bai\b": "machine learning", r"\bux\b": "ui/ux design",
            r"\bui\b": "ui/ux design", r"\bdevops\b": "docker",
            r"\breactjs\b": "react", r"\bnodejs\b": "node.js",
            r"\bvuejs\b": "vue", r"\bnextjs\b": "next.js",
        }
        for pattern, full_name in skill_aliases.items():
            if re.search(pattern, user_input_lower) and full_name not in found_skills:
                found_skills.append(full_name)

        return found_skills

    def _extract_city(self, user_input):
        """Extract city mention from user input."""
        user_input_lower = user_input.lower()
        for city_data in self.matcher.cities:
            if city_data["name"].lower() in user_input_lower:
                return city_data["name"]
        return None

    def _extract_job_title(self, user_input):
        """Extract job title mention from user input."""
        user_input_lower = user_input.lower()
        for job in self.matcher.jobs:
            if job["title"].lower() in user_input_lower:
                return job["title"]
        return None

    def _extract_interests(self, user_input):
        """Extract interest mentions from user input."""
        user_input_lower = user_input.lower()
        found = []
        for interest in self.matcher.dataset["interest_categories"]:
            if interest.lower() in user_input_lower:
                found.append(interest)
        return found

    def _tool_match_jobs(self, skills, city, interests=None, top_n=5):
        """Tool: Match jobs to user profile."""
        if not skills or not city:
            return {"error": "Need skills and city to match jobs"}
        return self.matcher.match_jobs(skills, city, interests or [], top_n)

    def _tool_skill_gap(self, skills, target_job):
        """Tool: Analyze skill gap for a target job."""
        if not skills or not target_job:
            return {"error": "Need skills and target job for gap analysis"}
        return self.matcher.get_skill_gap_analysis(skills, target_job)

    def _tool_get_courses(self, missing_skills):
        """Tool: Get course recommendations for missing skills."""
        return self.matcher._get_skill_gap_courses(missing_skills)

    def _tool_career_advice(self, skills, interests=None):
        """Tool: Generate career advice based on profile."""
        if not skills:
            return "I'd need to know your skills first!"

        category_scores = {}
        for job in self.matcher.jobs:
            skill_match = self.matcher._compute_skill_match(skills, job)
            cat = job["category"]
            if cat not in category_scores:
                category_scores[cat] = []
            category_scores[cat].append(skill_match["score"])

        avg_scores = {cat: sum(scores)/len(scores) for cat, scores in category_scores.items()}
        sorted_cats = sorted(avg_scores.items(), key=lambda x: x[1], reverse=True)

        advice = []
        for cat, score in sorted_cats[:3]:
            advice.append(f"{cat} ({score:.0f}% skill alignment)")

        return advice

    def _tool_city_info(self, city_name):
        """Tool: Get city-specific information."""
        for city in self.matcher.cities:
            if city["name"].lower() == city_name.lower():
                return city
        return None

    def _build_profile(self, state):
        """Build user profile summary from conversation state."""
        return {
            "skills": state.get("skills", []),
            "city": state.get("city", ""),
            "interests": state.get("interests", []),
            "target_job": state.get("target_job", ""),
        }

    def _format_job_results(self, results):
        """Format job matching results for conversational output."""
        if not results:
            return "No matching jobs found. Try adding more skills or changing your city."

        lines = []
        lines.append(f"Here are your top {len(results)} career matches:\n")

        for i, job in enumerate(results, 1):
            score_emoji = "+" * min(int(job["final_score"] / 20), 5)
            lines.append(f"**{i}. {job['job_title']}** ({job['category']})")
            lines.append(f"   Match Score: {job['final_score']}% {score_emoji}")
            lines.append(f"   Salary: {job['salary_range']}")
            lines.append(f"   Experience: {job['experience_required']}")
            lines.append(f"   {job['description']}")

            if job["skill_match"]["matched_required"]:
                lines.append(f"   Your matched skills: {', '.join(job['skill_match']['matched_required'][:5])}")
            if job["skill_match"]["missing_required"]:
                lines.append(f"   Skills to learn: {', '.join(job['skill_match']['missing_required'][:3])}")
            if job["recommended_courses"]:
                top_course = job["recommended_courses"][0]
                lines.append(f"   Suggested: {top_course['course']} ({top_course['platform']}, {top_course['duration']})")
            lines.append("")

        return "\n".join(lines)

    def _format_gap_analysis(self, gap):
        """Format skill gap analysis for conversational output."""
        if "error" in gap:
            return gap["error"]

        lines = []
        lines.append(f"**Skill Gap Analysis: {gap['target_job']}**\n")
        lines.append(f"Match Rate: {gap['match_percentage']}%")
        lines.append(f"Skills you have: {', '.join(gap['matched_skills'])}")
        lines.append(f"Skills you need: {', '.join(gap['missing_skills'])}")
        lines.append(f"Estimated learning time: {gap['estimated_time']}\n")

        if gap["recommended_courses"]:
            lines.append("**Recommended Learning Path:**")
            for c in gap["recommended_courses"]:
                lines.append(f"  - {c['course']} ({c['platform']}, {c['duration']})")

        return "\n".join(lines)

    def process_message(self, user_input):
        """
        Main agent loop. Processes user input, decides actions,
        invokes tools autonomously, and returns response.
        """
        self.session_log.append({"role": "user", "content": user_input, "time": datetime.now().isoformat()})

        state = self.conversation_state
        intents = self._detect_intent(user_input)
        skills = self._extract_skills(user_input)
        city = self._extract_city(user_input)
        interests = self._extract_interests(user_input)
        job_title = self._extract_job_title(user_input)

        # Update state
        if skills:
            existing = state.get("skills", [])
            state["skills"] = list(set(existing + skills))
        if city:
            state["city"] = city
        if interests:
            existing_i = state.get("interests", [])
            state["interests"] = list(set(existing_i + interests))
        if job_title:
            state["target_job"] = job_title

        # Autonomous decision making
        response = self._decide_action(intents, state, user_input)

        self.session_log.append({"role": "agent", "content": response, "time": datetime.now().isoformat()})
        return response

    def _decide_action(self, intents, state, user_input):
        """Autonomous decision engine - the agent decides what to do."""
        current_skills = state.get("skills", [])
        current_city = state.get("city", "")

        # Greeting
        if "greeting" in intents:
            return self._handle_greeting(state)

        # Help
        if "help" in intents:
            return self._handle_help()

        # Thank/Goodbye
        if "thank" in intents:
            return self._handle_goodbye(state)

        # Job search intent - explicit request for jobs
        if "job_search" in intents:
            if current_skills and current_city:
                results = self.tools["match_jobs"](current_skills, current_city, state.get("interests"))
                return self._format_job_results(results)
            elif current_skills and not current_city:
                return f"Great skills: {', '.join(current_skills[:5])}! Which city are you based in? I'll find matching jobs there."
            else:
                return "I'd love to find jobs for you! First, tell me - what are your skills?"

        # Skill gap intent
        if "skill_gap" in intents:
            if state.get("target_job") and current_skills:
                gap = self.tools["skill_gap_analysis"](current_skills, state["target_job"])
                return self._format_gap_analysis(gap)
            elif current_skills:
                suggested = self.tools["career_advice"](current_skills, state.get("interests"))
                lines = ["Based on your skills, here are your strongest career categories:\n"]
                for i, cat in enumerate(suggested, 1):
                    lines.append(f"  {i}. {cat}")
                lines.append("\nWhich one interests you? I'll analyze the skill gap for that role.")
                return "\n".join(lines)
            else:
                return "Tell me your skills first, and I'll analyze what you need to learn for your dream role!"

        # Salary intent
        if "salary" in intents:
            if current_skills and current_city:
                results = self.tools["match_jobs"](current_skills, current_city, state.get("interests"), 5)
                lines = ["**Salary Ranges for Your Profile:**\n"]
                for job in results:
                    lines.append(f"  - {job['job_title']}: {job['salary_range']}")
                lines.append("\nSalaries vary by company and experience. Want to see the full career matches?")
                return "\n".join(lines)
            else:
                return "Tell me your skills and city, and I'll show you salary ranges for matching roles!"

        # Career advice intent
        if "career_advice" in intents:
            if current_skills:
                suggested = self.tools["career_advice"](current_skills, state.get("interests"))
                lines = ["**Your Career Roadmap:**\n"]
                lines.append("Based on your skills, here are your best-fit career paths:\n")
                for i, cat in enumerate(suggested, 1):
                    lines.append(f"  {i}. {cat}")
                if current_city:
                    lines.append(f"\nIn {current_city}, I can find specific job openings. Want me to search?")
                else:
                    lines.append("\nWhich city are you in? I'll find matching opportunities.")
                return "\n".join(lines)
            else:
                return "Let's start with your skills! What technologies or tools do you know?"

        # Resume intent
        if "resume" in intents:
            if current_skills:
                lines = ["**Resume Tips for Your Profile:**\n"]
                lines.append("Based on your skills, here's how to optimize your resume:\n")
                lines.append(f"- Highlight these skills prominently: {', '.join(current_skills[:5])}")
                if current_city:
                    lines.append(f"- Mention your location: {current_city} (emphasize remote readiness)")
                lines.append("- Use ATS-friendly format: clean headers, bullet points, keywords")
                lines.append("- Tailor your resume for each application")
                lines.append("\nI can also analyze skill gaps for specific roles to help you build a targeted resume.")
                return "\n".join(lines)
            else:
                return "Tell me your skills and I'll give you tailored resume tips!"

        # City info / city change
        if "city_info" in intents:
            is_change = bool(re.search(r'\b(change|update|new|switch|move|shift|different)\b', user_input.lower()))
            if current_city:
                city_data = self.tools["city_info"](current_city)
                if city_data:
                    if is_change:
                        ack = f"City updated to **{city_data['name']}**!"
                        if current_skills:
                            results = self.tools["match_jobs"](current_skills, current_city, state.get("interests"))
                            return ack + "\n\n" + self._format_job_results(results)
                        return ack + f" What skills do you have? I'll find jobs in {city_data['name']}."
                    if not current_skills:
                        return f"**{city_data['name']}, {city_data['state']}** (Tier-{city_data['tier']})\nTop sectors: {', '.join(city_data['top_sectors'])}\nWhat skills do you have? I'll find matching jobs here."
            if not current_city:
                cities_list = [c["name"] for c in self.matcher.cities[:10]]
                return f"I support these Tier-2/3 cities: {', '.join(cities_list)}, and more.\nWhich city are you in?"

        # If both skills and city are available, proactively match
        if current_skills and current_city:
            results = self.tools["match_jobs"](current_skills, current_city, state.get("interests"))
            return self._format_job_results(results)

        # If we have skills but no city
        if current_skills and not current_city:
            return f"I see you have skills in: {', '.join(current_skills[:6])}. Which city are you based in? I'll find the best career matches for you."

        # If we have city but no skills
        if current_city and not current_skills:
            return f"Great, you're in {current_city}! What skills do you have? I'll match you with the best opportunities."

        # Default: guide the user
        return self._handle_default(state)

    def _handle_greeting(self, state):
        if state.get("skills") and state.get("city"):
            return random.choice([
                f"Welcome back! Ready to explore more careers in {state['city']}?",
                f"Hey! Your profile has {len(state['skills'])} skills from {state['city']}. Want to search for jobs?",
            ])
        return random.choice(self.greetings)

    def _handle_help(self):
        return """**Here's what I can do:**

1. **Find Jobs** - Say "find jobs" or "recommend careers"
2. **Skill Gap Analysis** - Say "skill gap" or "what do I need to learn"
3. **Career Advice** - Say "suggest a career path" or "what should I do"
4. **Salary Info** - Say "what's the salary for..."
5. **Resume Tips** - Say "resume tips" or "help me with my CV"
6. **City Info** - Say "jobs in Indore" or "what's in Jaipur"

**How to use me:**
- Tell me your skills: "I know Python, SQL, Excel"
- Tell me your city: "I'm in Indore"
- I'll autonomously find the best matches!

**Example:** "I know Python and SQL, I'm in Kochi, find me jobs" """

    def _handle_goodbye(self, state):
        profile = self._build_profile(state)
        if profile["skills"]:
            return random.choice([
                f"Goodbye! You're on a great path with {', '.join(profile['skills'][:3])}. Keep learning and growing!",
                "Thanks for using NexaPath! Remember, every skill you learn brings you closer to your dream career. All the best!",
                "See you! Remember: Tier-2/3 talent deserves Tier-1 opportunities. NexaPath is here whenever you need us.",
            ])
        return "Goodbye! Come back when you're ready to explore careers. NexaPath is always here for you!"

    def _proactive_suggest(self, state):
        """Agent proactively suggests actions when it has enough data."""
        skills = state.get("skills", [])
        city = state.get("city", "")

        lines = [f"I have your profile: {', '.join(skills[:5])} in {city}.\n"]
        lines.append("**What would you like to do?**\n")
        lines.append("1. Find matching careers")
        lines.append("2. Analyze skill gaps for a specific role")
        lines.append("3. Get career advice and learning path")
        lines.append("4. See salary ranges")
        lines.append("\nJust type 1-4 or describe what you want!")

        return "\n".join(lines)

    def _handle_default(self, state):
        if not state.get("skills"):
            return "I'm your AI Career Copilot! To get started, tell me:\n\n1. **Your skills** - e.g., 'I know Python, SQL, Excel'\n2. **Your city** - e.g., 'I'm in Indore'\n\nThen I'll find the best career paths for you!"
        return "I'm not sure what you mean. Try saying 'find jobs', 'skill gap', or 'career advice'. Type 'help' to see all options."

    def get_session_summary(self):
        """Return summary of the conversation session."""
        return {
            "total_messages": len(self.session_log),
            "profile": self._build_profile(self.conversation_state),
            "log": self.session_log,
            "sdg_alignment": ["SDG 4", "SDG 8", "SDG 10"],
        }
