import json
import random

# ============================================================
# NexaPath Dataset — Jobs, Skills, Career Paths (Tier-2/3 India)
# ============================================================

# All unique skills in the system
ALL_SKILLS = [
    # Programming
    "python", "javascript", "java", "c++", "c#", "php", "ruby", "go", "rust", "typescript",
    "swift", "kotlin", "scala", "r", "matlab", "sql", "nosql",
    # Web Development
    "html", "css", "react", "angular", "vue", "node.js", "django", "flask", "spring boot",
    "laravel", "express.js", "next.js", "tailwind css", "bootstrap", "wordpress",
    # Data & AI
    "machine learning", "deep learning", "nlp", "computer vision", "tensorflow", "pytorch",
    "pandas", "numpy", "scikit-learn", "data analysis", "data visualization",
    "power bi", "tableau", "excel", "google analytics", "sql queries",
    # Cloud & DevOps
    "aws", "azure", "gcp", "docker", "kubernetes", "jenkins", "git", "linux",
    "ci/cd", "terraform", "ansible", "nginx",
    # Mobile
    "android development", "ios development", "flutter", "react native",
    # Design
    "ui/ux design", "figma", "photoshop", "illustrator", "canva", "adobe xd",
    "wireframing", "prototyping", "user research",
    # Marketing
    "seo", "sem", "social media marketing", "content writing", "copywriting",
    "email marketing", "google ads", "facebook ads", "analytics",
    # Business
    "project management", "agile", "scrum", "product management", "business analysis",
    "stakeholder management", "risk management",
    # Soft Skills
    "communication", "leadership", "team management", "problem solving",
    "critical thinking", "time management", "presentation",
    # Domain
    "finance", "accounting", "banking", "healthcare", "education", "retail",
    "manufacturing", "logistics", "ecommerce", "fintech", "edtech", "healthtech",
    # Tools
    "jira", "slack", "notion", "trello", "salesforce", "hubspot", "zapier",
    "airtable", "google workspace", "microsoft office",
    # Security
    "cybersecurity", "network security", "ethical hacking", "penetration testing",
    "owasp", "soc2", "gdpr",
    # Other
    "blockchain", "iot", "ar/vr", "game development", "technical writing",
    "qa testing", "selenium", "automation testing", "manual testing",
]

# Tier-2/3 cities with hiring data
CITIES = [
    {"name": "Indore", "state": "MP", "tier": 2, "top_sectors": ["IT", "Finance", "Education"]},
    {"name": "Jaipur", "state": "Rajasthan", "tier": 2, "top_sectors": ["IT", "Tourism", "Gems"]},
    {"name": "Lucknow", "state": "UP", "tier": 2, "top_sectors": ["IT", "Government", "Education"]},
    {"name": "Kochi", "state": "Kerala", "tier": 2, "top_sectors": ["IT", "Shipping", "Tourism"]},
    {"name": "Coimbatore", "state": "Tamil Nadu", "tier": 2, "top_sectors": ["Manufacturing", "IT", "Textiles"]},
    {"name": "Nagpur", "state": "Maharashtra", "tier": 2, "top_sectors": ["Logistics", "Mining", "IT"]},
    {"name": "Bhopal", "state": "MP", "tier": 2, "top_sectors": ["IT", "Education", "Manufacturing"]},
    {"name": "Patna", "state": "Bihar", "tier": 3, "top_sectors": ["Government", "Education", "Agriculture"]},
    {"name": "Visakhapatnam", "state": "AP", "tier": 2, "top_sectors": ["Manufacturing", "IT", "Shipping"]},
    {"name": "Surat", "state": "Gujarat", "tier": 2, "top_sectors": ["Textiles", "Diamonds", "IT"]},
    {"name": "Dehradun", "state": "Uttarakhand", "tier": 3, "top_sectors": ["Education", "Tourism", "IT"]},
    {"name": "Mysuru", "state": "Karnataka", "tier": 2, "top_sectors": ["IT", "Tourism", "Education"]},
    {"name": "Mangalore", "state": "Karnataka", "tier": 3, "top_sectors": ["Banking", "IT", "Petroleum"]},
    {"name": "Thiruvananthapuram", "state": "Kerala", "tier": 2, "top_sectors": ["IT", "Space", "Education"]},
    {"name": "Agra", "state": "UP", "tier": 3, "top_sectors": ["Tourism", "Manufacturing", "Education"]},
    {"name": "Nashik", "state": "Maharashtra", "tier": 3, "top_sectors": ["Manufacturing", "Agriculture", "IT"]},
    {"name": "Ranchi", "state": "Jharkhand", "tier": 3, "top_sectors": ["Mining", "Government", "IT"]},
    {"name": "Guwahati", "state": "Assam", "tier": 3, "top_sectors": ["Government", "Oil", "Education"]},
    {"name": "Chandigarh", "state": "Chandigarh", "tier": 2, "top_sectors": ["IT", "Education", "Government"]},
    {"name": "Amritsar", "state": "Punjab", "tier": 3, "top_sectors": ["Tourism", "Textiles", "Education"]},
]

# Job roles with required skills, salary range, experience
JOB_ROLES = [
    # ---- Tech / Software ----
    {"title": "Frontend Developer", "category": "Software Development",
     "required_skills": ["javascript", "react", "html", "css", "git", "responsive design"],
     "nice_to_have": ["typescript", "next.js", "tailwind css", "vue", "angular"],
     "min_exp": 0, "max_exp": 5, "salary_min": 3, "salary_max": 12,
     "description": "Build user interfaces for web applications",
     "growth_path": ["Senior Frontend Dev", "UI Architect", "Full Stack Dev"]},

    {"title": "Backend Developer", "category": "Software Development",
     "required_skills": ["python", "django", "sql", "rest api", "git", "linux"],
     "nice_to_have": ["docker", "aws", "redis", "celery", "postgresql"],
     "min_exp": 0, "max_exp": 5, "salary_min": 3.5, "salary_max": 14,
     "description": "Build server-side logic and APIs",
     "growth_path": ["Senior Backend Dev", "Backend Architect", "Tech Lead"]},

    {"title": "Full Stack Developer", "category": "Software Development",
     "required_skills": ["javascript", "react", "node.js", "sql", "html", "css", "git"],
     "nice_to_have": ["typescript", "docker", "aws", "mongodb", "next.js"],
     "min_exp": 1, "max_exp": 6, "salary_min": 4, "salary_max": 16,
     "description": "Build complete web applications end-to-end",
     "growth_path": ["Senior Full Stack", "Tech Lead", "CTO"]},

    {"title": "Mobile App Developer", "category": "Software Development",
     "required_skills": ["flutter", "dart", "android development", "firebase", "git"],
     "nice_to_have": ["react native", "ios development", "swift", "kotlin"],
     "min_exp": 0, "max_exp": 5, "salary_min": 3.5, "salary_max": 13,
     "description": "Build mobile applications for Android/iOS",
     "growth_path": ["Senior Mobile Dev", "Mobile Architect", "Product Lead"]},

    {"title": "Python Developer", "category": "Software Development",
     "required_skills": ["python", "flask", "sql", "rest api", "git"],
     "nice_to_have": ["django", "docker", "aws", "celery", "redis"],
     "min_exp": 0, "max_exp": 5, "salary_min": 3, "salary_max": 12,
     "description": "Build Python-based applications and automation",
     "growth_path": ["Senior Python Dev", "Backend Lead", "Architect"]},

    # ---- Data & AI ----
    {"title": "Data Analyst", "category": "Data & Analytics",
     "required_skills": ["sql", "excel", "python", "data analysis", "data visualization"],
     "nice_to_have": ["power bi", "tableau", "google analytics", "pandas", "statistics"],
     "min_exp": 0, "max_exp": 4, "salary_min": 3, "salary_max": 10,
     "description": "Analyze data and create business insights",
     "growth_path": ["Senior Data Analyst", "Data Scientist", "Analytics Lead"]},

    {"title": "Data Scientist", "category": "Data & Analytics",
     "required_skills": ["python", "machine learning", "sql", "pandas", "numpy", "scikit-learn"],
     "nice_to_have": ["deep learning", "tensorflow", "pytorch", "nlp", "tableau"],
     "min_exp": 1, "max_exp": 6, "salary_min": 5, "salary_max": 18,
     "description": "Build ML models and extract insights from data",
     "growth_path": ["Senior Data Scientist", "ML Engineer", "Head of AI"]},

    {"title": "Machine Learning Engineer", "category": "Data & Analytics",
     "required_skills": ["python", "machine learning", "tensorflow", "pytorch", "docker"],
     "nice_to_have": ["deep learning", "kubernetes", "aws", "mlops", "nlp"],
     "min_exp": 1, "max_exp": 6, "salary_min": 6, "salary_max": 20,
     "description": "Deploy and optimize ML models in production",
     "growth_path": ["Senior ML Engineer", "ML Architect", "Head of AI"]},

    {"title": "Business Intelligence Analyst", "category": "Data & Analytics",
     "required_skills": ["sql", "power bi", "tableau", "excel", "data analysis"],
     "nice_to_have": ["python", "data visualization", "google analytics", "dax"],
     "min_exp": 0, "max_exp": 4, "salary_min": 3, "salary_max": 9,
     "description": "Create dashboards and business reports",
     "growth_path": ["Senior BI Analyst", "BI Manager", "Analytics Director"]},

    # ---- Cloud & DevOps ----
    {"title": "DevOps Engineer", "category": "Cloud & Infrastructure",
     "required_skills": ["linux", "docker", "jenkins", "git", "aws", "ci/cd"],
     "nice_to_have": ["kubernetes", "terraform", "ansible", "python", "nginx"],
     "min_exp": 1, "max_exp": 6, "salary_min": 5, "salary_max": 16,
     "description": "Manage CI/CD pipelines and cloud infrastructure",
     "growth_path": ["Senior DevOps", "Cloud Architect", "Infrastructure Lead"]},

    {"title": "Cloud Engineer", "category": "Cloud & Infrastructure",
     "required_skills": ["aws", "linux", "docker", "python", "networking"],
     "nice_to_have": ["azure", "gcp", "kubernetes", "terraform", "ansible"],
     "min_exp": 1, "max_exp": 5, "salary_min": 5, "salary_max": 15,
     "description": "Design and manage cloud infrastructure",
     "growth_path": ["Senior Cloud Engineer", "Cloud Architect", "VP Engineering"]},

    {"title": "Site Reliability Engineer", "category": "Cloud & Infrastructure",
     "required_skills": ["linux", "python", "docker", "kubernetes", "monitoring"],
     "nice_to_have": ["aws", "terraform", "grafana", "prometheus", "go"],
     "min_exp": 2, "max_exp": 7, "salary_min": 7, "salary_max": 22,
     "description": "Ensure system reliability and uptime",
     "growth_path": ["Senior SRE", "Platform Lead", "VP Infrastructure"]},

    # ---- Cybersecurity ----
    {"title": "Security Analyst", "category": "Cybersecurity",
     "required_skills": ["cybersecurity", "network security", "linux", "siem", "incident response"],
     "nice_to_have": ["ethical hacking", "owasp", "python", "soc2", "gdpr"],
     "min_exp": 0, "max_exp": 5, "salary_min": 4, "salary_max": 12,
     "description": "Monitor and respond to security threats",
     "growth_path": ["Senior Security Analyst", "Security Architect", "CISO"]},

    {"title": "Ethical Hacker", "category": "Cybersecurity",
     "required_skills": ["ethical hacking", "penetration testing", "network security", "linux", "owasp"],
     "nice_to_have": ["python", "burp suite", "metasploit", "web security"],
     "min_exp": 1, "max_exp": 6, "salary_min": 5, "salary_max": 15,
     "description": "Test systems for vulnerabilities",
     "growth_path": ["Senior Pentester", "Security Consultant", "Security Lead"]},

    # ---- Design ----
    {"title": "UI/UX Designer", "category": "Design",
     "required_skills": ["ui/ux design", "figma", "wireframing", "prototyping", "user research"],
     "nice_to_have": ["adobe xd", "photoshop", "illustrator", "canva", "css"],
     "min_exp": 0, "max_exp": 5, "salary_min": 3, "salary_max": 10,
     "description": "Design user interfaces and experiences",
     "growth_path": ["Senior UX Designer", "Design Lead", "Head of Design"]},

    {"title": "Graphic Designer", "category": "Design",
     "required_skills": ["photoshop", "illustrator", "canva", "graphic design"],
     "nice_to_have": ["figma", "after effects", "premiere pro", "indesign"],
     "min_exp": 0, "max_exp": 4, "salary_min": 2.5, "salary_max": 7,
     "description": "Create visual content for brands",
     "growth_path": ["Senior Designer", "Art Director", "Creative Director"]},

    {"title": "Product Designer", "category": "Design",
     "required_skills": ["ui/ux design", "figma", "prototyping", "user research", "wireframing"],
     "nice_to_have": ["product management", "data analysis", "css", "html"],
     "min_exp": 1, "max_exp": 6, "salary_min": 5, "salary_max": 14,
     "description": "Design end-to-end product experiences",
     "growth_path": ["Senior Product Designer", "Design Manager", "VP Design"]},

    # ---- Marketing ----
    {"title": "Digital Marketing Specialist", "category": "Marketing",
     "required_skills": ["seo", "sem", "social media marketing", "google ads", "analytics"],
     "nice_to_have": ["content writing", "email marketing", "facebook ads", "copywriting"],
     "min_exp": 0, "max_exp": 4, "salary_min": 2.5, "salary_max": 8,
     "description": "Manage digital marketing campaigns",
     "growth_path": ["Senior Marketer", "Marketing Manager", "CMO"]},

    {"title": "SEO Specialist", "category": "Marketing",
     "required_skills": ["seo", "google analytics", "content writing", "keyword research"],
     "nice_to_have": ["sem", "html", "wordpress", "copywriting"],
     "min_exp": 0, "max_exp": 4, "salary_min": 2.5, "salary_max": 7,
     "description": "Optimize websites for search engines",
     "growth_path": ["Senior SEO", "SEO Manager", "Head of Growth"]},

    {"title": "Content Writer", "category": "Marketing",
     "required_skills": ["content writing", "copywriting", "seo", "research"],
     "nice_to_have": ["social media marketing", "wordpress", "canva"],
     "min_exp": 0, "max_exp": 3, "salary_min": 2, "salary_max": 6,
     "description": "Create written content for brands",
     "growth_path": ["Senior Writer", "Content Manager", "Content Director"]},

    {"title": "Social Media Manager", "category": "Marketing",
     "required_skills": ["social media marketing", "content writing", "analytics", "canva"],
     "nice_to_have": ["seo", "copywriting", "facebook ads", "instagram"],
     "min_exp": 0, "max_exp": 4, "salary_min": 2.5, "salary_max": 7,
     "description": "Manage brand social media presence",
     "growth_path": ["Senior SMM", "Marketing Lead", "Brand Manager"]},

    # ---- QA / Testing ----
    {"title": "QA Engineer", "category": "Quality Assurance",
     "required_skills": ["manual testing", "qa testing", "test cases", "jira"],
     "nice_to_have": ["selenium", "automation testing", "python", "sql"],
     "min_exp": 0, "max_exp": 4, "salary_min": 2.5, "salary_max": 8,
     "description": "Test software for quality and bugs",
     "growth_path": ["Senior QA", "QA Lead", "QA Manager"]},

    {"title": "Automation Test Engineer", "category": "Quality Assurance",
     "required_skills": ["selenium", "automation testing", "python", "java", "qa testing"],
     "nice_to_have": ["cypress", "appium", "docker", "ci/cd"],
     "min_exp": 1, "max_exp": 5, "salary_min": 4, "salary_max": 12,
     "description": "Build automated test frameworks",
     "growth_path": ["Senior Automation QA", "Test Architect", "QA Manager"]},

    # ---- Product & Project ----
    {"title": "Project Manager", "category": "Product & Management",
     "required_skills": ["project management", "agile", "scrum", "jira", "communication"],
     "nice_to_have": ["risk management", "stakeholder management", "budgeting"],
     "min_exp": 2, "max_exp": 8, "salary_min": 6, "salary_max": 18,
     "description": "Manage projects and delivery timelines",
     "growth_path": ["Senior PM", "Program Manager", "VP Product"]},

    {"title": "Product Manager", "category": "Product & Management",
     "required_skills": ["product management", "agile", "user research", "data analysis", "communication"],
     "nice_to_have": ["sql", "figma", "sql", "market research"],
     "min_exp": 2, "max_exp": 7, "salary_min": 7, "salary_max": 22,
     "description": "Define product strategy and roadmap",
     "growth_path": ["Senior PM", "Director of Product", "CPO"]},

    {"title": "Business Analyst", "category": "Product & Management",
     "required_skills": ["business analysis", "sql", "excel", "requirements gathering", "communication"],
     "nice_to_have": ["jira", "power bi", "python", "process mapping"],
     "min_exp": 0, "max_exp": 5, "salary_min": 3.5, "salary_max": 10,
     "description": "Bridge business needs and technical solutions",
     "growth_path": ["Senior BA", "Product Owner", "Consultant"]},

    # ---- IT Support ----
    {"title": "IT Support Specialist", "category": "IT Support",
     "required_skills": ["windows", "linux", "networking", "troubleshooting", "hardware"],
     "nice_to_have": ["active directory", "aws", "python", "scripting"],
     "min_exp": 0, "max_exp": 3, "salary_min": 2, "salary_max": 5,
     "description": "Provide technical support to users",
     "growth_path": ["Senior IT Support", "IT Admin", "IT Manager"]},

    {"title": "Network Engineer", "category": "IT Support",
     "required_skills": ["networking", "ccna", "linux", "firewall", "troubleshooting"],
     "nice_to_have": ["python", "aws", "vpn", "dns"],
     "min_exp": 0, "max_exp": 5, "salary_min": 3, "salary_max": 9,
     "description": "Manage and maintain network infrastructure",
     "growth_path": ["Senior Network Eng", "Network Architect", "IT Director"]},

    # ---- Finance & Accounting ----
    {"title": "Financial Analyst", "category": "Finance",
     "required_skills": ["excel", "financial modeling", "accounting", "finance", "data analysis"],
     "nice_to_have": ["sql", "power bi", "python", "advanced excel"],
     "min_exp": 0, "max_exp": 4, "salary_min": 3, "salary_max": 9,
     "description": "Analyze financial data and create reports",
     "growth_path": ["Senior FA", "Finance Manager", "CFO"]},

    {"title": "Accountant", "category": "Finance",
     "required_skills": ["accounting", "tally", "excel", "gst", "taxation"],
     "nice_to_have": ["finance", "audit", "erp", "compliance"],
     "min_exp": 0, "max_exp": 5, "salary_min": 2.5, "salary_max": 7,
     "description": "Manage financial records and compliance",
     "growth_path": ["Senior Accountant", "Accounts Manager", "Finance Director"]},

    # ---- Sales ----
    {"title": "Sales Executive", "category": "Sales",
     "required_skills": ["sales", "communication", "crm", "negotiation", "ms office"],
     "nice_to_have": ["salesforce", "hubspot", "lead generation"],
     "min_exp": 0, "max_exp": 3, "salary_min": 2, "salary_max": 6,
     "description": "Generate leads and close deals",
     "growth_path": ["Senior Sales", "Sales Manager", "Sales Director"]},

    {"title": "Business Development Executive", "category": "Sales",
     "required_skills": ["business development", "communication", "negotiation", "market research"],
     "nice_to_have": ["sales", "crm", "presentation", "ms office"],
     "min_exp": 0, "max_exp": 4, "salary_min": 2.5, "salary_max": 7,
     "description": "Identify and develop new business opportunities",
     "growth_path": ["Senior BDE", "BD Manager", "VP Sales"]},

    # ---- HR ----
    {"title": "HR Executive", "category": "Human Resources",
     "required_skills": ["recruitment", "communication", "ms office", "employee relations"],
     "nice_to_have": ["hris", "payroll", "compliance", "training"],
     "min_exp": 0, "max_exp": 3, "salary_min": 2.5, "salary_max": 6,
     "description": "Manage hiring and employee relations",
     "growth_path": ["Senior HR", "HR Manager", "HR Director"]},

    # ---- Remote / Freelance ----
    {"title": "Freelance Web Developer", "category": "Freelance",
     "required_skills": ["html", "css", "javascript", "wordpress", "responsive design"],
     "nice_to_have": ["react", "php", "seo", "figma"],
     "min_exp": 0, "max_exp": 5, "salary_min": 2, "salary_max": 15,
     "description": "Build websites for clients independently",
     "growth_path": ["Agency Owner", "Tech Consultant"]},

    {"title": "Freelance Content Writer", "category": "Freelance",
     "required_skills": ["content writing", "copywriting", "seo", "research"],
     "nice_to_have": ["blogging", "technical writing", "social media"],
     "min_exp": 0, "max_exp": 5, "salary_min": 1.5, "salary_max": 8,
     "description": "Write content for clients independently",
     "growth_path": ["Content Agency", "Editor", "Content Director"]},

    {"title": "Freelance Graphic Designer", "category": "Freelance",
     "required_skills": ["photoshop", "illustrator", "canva", "graphic design"],
     "nice_to_have": ["figma", "after effects", "video editing"],
     "min_exp": 0, "max_exp": 5, "salary_min": 1.5, "salary_max": 8,
     "description": "Design visuals for clients independently",
     "growth_path": ["Design Agency", "Art Director"]},

    {"title": "Remote Data Entry Operator", "category": "Freelance",
     "required_skills": ["ms office", "excel", "typing", "data entry"],
     "nice_to_have": ["google workspace", "attention to detail"],
     "min_exp": 0, "max_exp": 2, "salary_min": 1.5, "salary_max": 3.5,
     "description": "Enter and manage data remotely",
     "growth_path": ["Data Analyst", "Office Admin"]},

    {"title": "Remote Customer Support", "category": "Freelance",
     "required_skills": ["communication", "customer service", "ms office", "email"],
     "nice_to_have": ["crm", "zendesk", "intercom", "chat support"],
     "min_exp": 0, "max_exp": 3, "salary_min": 1.5, "salary_max": 4,
     "description": "Provide customer support remotely",
     "growth_path": ["Support Lead", "Customer Success Manager"]},

    # ---- Journalism / OSINT (Secondary Segment) ----
    {"title": "Digital Journalist", "category": "Media",
     "required_skills": ["content writing", "research", "social media", "communication"],
     "nice_to_have": ["video editing", "photoshop", "data analysis", "investigative skills"],
     "min_exp": 0, "max_exp": 5, "salary_min": 2.5, "salary_max": 8,
     "description": "Report news for digital media platforms",
     "growth_path": ["Senior Journalist", "Editor", "Media Director"]},

    {"title": "OSINT Researcher", "category": "Media",
     "required_skills": ["osint", "research", "data analysis", "python", "social media"],
     "nice_to_have": ["cybersecurity", "nlp", "investigative skills", "linux"],
     "min_exp": 1, "max_exp": 5, "salary_min": 4, "salary_max": 12,
     "description": "Gather intelligence from open sources",
     "growth_path": ["Senior OSINT Analyst", "Intelligence Lead"]},

    {"title": "Data Journalist", "category": "Media",
     "required_skills": ["data analysis", "python", "sql", "data visualization", "content writing"],
     "nice_to_have": ["tableau", "power bi", "investigative skills", "statistics"],
     "min_exp": 1, "max_exp": 5, "salary_min": 3.5, "salary_max": 10,
     "description": "Use data to tell stories and uncover insights",
     "growth_path": ["Senior Data Journalist", "Editor", "Analytics Director"]},
]

# Micro-courses for skill gap analysis
MICRO_COURSES = {
    "python": {"title": "Python for Beginners", "platform": "NPTEL", "duration": "4 weeks", "url": "nptel.ac.in"},
    "javascript": {"title": "JavaScript Essentials", "platform": "Coursera", "duration": "3 weeks", "url": "coursera.org"},
    "react": {"title": "React - The Complete Guide", "platform": "Udemy", "duration": "6 weeks", "url": "udemy.com"},
    "machine learning": {"title": "ML Foundations", "platform": "Coursera", "duration": "8 weeks", "url": "coursera.org"},
    "sql": {"title": "SQL for Data Analysis", "platform": "Khan Academy", "duration": "3 weeks", "url": "khanacademy.org"},
    "figma": {"title": "Figma for Beginners", "platform": "YouTube", "duration": "2 weeks", "url": "youtube.com"},
    "aws": {"title": "AWS Cloud Practitioner", "platform": "AWS Training", "duration": "6 weeks", "url": "aws.training"},
    "docker": {"title": "Docker for Beginners", "platform": "Udemy", "duration": "4 weeks", "url": "udemy.com"},
    "seo": {"title": "SEO Fundamentals", "platform": "Google", "duration": "3 weeks", "url": "learndigital.withgoogle.com"},
    "power bi": {"title": "Power BI Masterclass", "platform": "Coursera", "duration": "4 weeks", "url": "coursera.org"},
    "data analysis": {"title": "Data Analytics Professional", "platform": "Google", "duration": "6 weeks", "url": "coursera.org"},
    "ui/ux design": {"title": "UX Design Professional", "platform": "Google", "duration": "8 weeks", "url": "coursera.org"},
    "cybersecurity": {"title": "Cybersecurity Fundamentals", "platform": "Coursera", "duration": "6 weeks", "url": "coursera.org"},
    "content writing": {"title": "Content Strategy", "platform": "HubSpot", "duration": "3 weeks", "url": "academy.hubspot.com"},
    "project management": {"title": "Project Management Professional", "platform": "Google", "duration": "6 weeks", "url": "coursera.org"},
    "flask": {"title": "Flask Web Development", "platform": "Udemy", "duration": "4 weeks", "url": "udemy.com"},
    "django": {"title": "Django for Everybody", "platform": "Coursera", "duration": "5 weeks", "url": "coursera.org"},
    "tensorflow": {"title": "Deep Learning with TensorFlow", "platform": "Coursera", "duration": "8 weeks", "url": "coursera.org"},
    "git": {"title": "Git & GitHub Fundamentals", "platform": "Udemy", "duration": "2 weeks", "url": "udemy.com"},
    "linux": {"title": "Linux Administration", "platform": "Udemy", "duration": "4 weeks", "url": "udemy.com"},
    "tableau": {"title": "Tableau for Beginners", "platform": "Coursera", "duration": "4 weeks", "url": "coursera.org"},
    "google analytics": {"title": "Google Analytics Certification", "platform": "Google", "duration": "3 weeks", "url": "skillshop.withgoogle.com"},
    "social media marketing": {"title": "Social Media Marketing", "platform": "HubSpot", "duration": "3 weeks", "url": "academy.hubspot.com"},
    "excel": {"title": "Advanced Excel Skills", "platform": "Coursera", "duration": "3 weeks", "url": "coursera.org"},
    "selenium": {"title": "Selenium WebDriver with Python", "platform": "Udemy", "duration": "4 weeks", "url": "udemy.com"},
    "kubernetes": {"title": "Kubernetes for Beginners", "platform": "Udemy", "duration": "5 weeks", "url": "udemy.com"},
    "terraform": {"title": "Terraform Fundamentals", "platform": "HashiCorp", "duration": "4 weeks", "url": "developer.hashicorp.com"},
    "penetration testing": {"title": "Ethical Hacking & Pen Testing", "platform": "Udemy", "duration": "8 weeks", "url": "udemy.com"},
    "communication": {"title": "Business Communication Skills", "platform": "Coursera", "duration": "3 weeks", "url": "coursera.org"},
    "agile": {"title": "Agile with Atlassian Jira", "platform": "Coursera", "duration": "3 weeks", "url": "coursera.org"},
}

# Interest categories for users
INTEREST_CATEGORIES = [
    "Technology", "Design", "Marketing", "Finance", "Healthcare",
    "Education", "E-commerce", "Fintech", "Edtech", "Media",
    "Manufacturing", "Agriculture", "Government", "Startups", "Remote Work"
]


def save_dataset():
    dataset = {
        "skills": ALL_SKILLS,
        "cities": CITIES,
        "job_roles": JOB_ROLES,
        "micro_courses": MICRO_COURSES,
        "interest_categories": INTEREST_CATEGORIES,
        "metadata": {
            "total_skills": len(ALL_SKILLS),
            "total_cities": len(CITIES),
            "total_jobs": len(JOB_ROLES),
            "total_courses": len(MICRO_COURSES),
            "version": "1.0",
            "focus": "Tier-2/3 India"
        }
    }

    with open("C:/Users/Adithya/NexaPath/backend/data/jobs_dataset.json", "w") as f:
        json.dump(dataset, f, indent=2)

    print(f"Dataset created:")
    print(f"  Skills: {len(ALL_SKILLS)}")
    print(f"  Cities: {len(CITIES)}")
    print(f"  Job Roles: {len(JOB_ROLES)}")
    print(f"  Micro Courses: {len(MICRO_COURSES)}")
    print(f"  Interest Categories: {len(INTEREST_CATEGORIES)}")


if __name__ == "__main__":
    save_dataset()
