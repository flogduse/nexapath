import json
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import joblib
import os

class NexaPathJobMatcher:
    """
    AI Job & Skill Matcher for NexaPath.
    Matches users to optimal career paths based on skills, interests, and location.
    Uses TF-IDF + Cosine Similarity for skill-based matching.
    """

    def __init__(self, dataset_path):
        with open(dataset_path, 'r') as f:
            self.dataset = json.load(f)

        self.jobs = self.dataset['job_roles']
        self.cities = self.dataset['cities']
        self.courses = self.dataset['micro_courses']
        self.all_skills = self.dataset['skills']

        self.vectorizer = TfidfVectorizer(analyzer='word', token_pattern=r'[a-zA-Z0-9#+/.]+')
        self.job_vectors = None
        self._build_job_vectors()

    def _build_job_vectors(self):
        """Convert job required skills into TF-IDF vectors."""
        job_texts = []
        for job in self.jobs:
            skills_text = ' '.join(job['required_skills'] + job.get('nice_to_have', []))
            job_texts.append(skills_text)
        self.job_vectors = self.vectorizer.fit_transform(job_texts)

    def _compute_skill_match(self, user_skills, job):
        """Compute how well user skills match a job's requirements."""
        required = set(job['required_skills'])
        nice_to_have = set(job.get('nice_to_have', []))
        user_set = set(s.lower().strip() for s in user_skills)

        matched_required = user_set & required
        matched_nice = user_set & nice_to_have
        missing_required = required - user_set

        if len(required) == 0:
            required_score = 0
        else:
            required_score = len(matched_required) / len(required)

        nice_score = len(matched_nice) / max(len(nice_to_have), 1)

        overall_score = (required_score * 0.7) + (nice_score * 0.3)

        return {
            'score': round(overall_score * 100, 1),
            'required_score': round(required_score * 100, 1),
            'matched_required': sorted(list(matched_required)),
            'matched_nice': sorted(list(matched_nice)),
            'missing_required': sorted(list(missing_required)),
        }

    def _compute_location_match(self, user_city, job_remote_ok=True):
        """Check if the job is available in or near the user's city."""
        user_city_lower = user_city.lower().strip()

        city_data = None
        for city in self.cities:
            if city['name'].lower() == user_city_lower:
                city_data = city
                break

        if city_data:
            return {
                'available': True,
                'city': city_data['name'],
                'tier': city_data['tier'],
                'top_sectors': city_data['top_sectors'],
                'remote_option': job_remote_ok,
            }

        return {
            'available': True,
            'city': user_city,
            'tier': None,
            'top_sectors': [],
            'remote_option': True,
        }

    def _compute_interest_match(self, user_interests, job_category):
        """Check if job category aligns with user interests."""
        interest_mapping = {
            'Technology': ['Software Development', 'Cloud & Infrastructure', 'Cybersecurity', 'IT Support', 'Artificial Intelligence'],
            'Design': ['Design'],
            'Marketing': ['Marketing'],
            'Finance': ['Finance'],
            'Healthcare': [],
            'Education': ['Education'],
            'E-commerce': ['Software Development', 'Marketing', 'Sales'],
            'Fintech': ['Finance', 'Software Development'],
            'Edtech': ['Education', 'Software Development'],
            'Media': ['Media', 'Marketing', 'Design'],
            'Manufacturing': ['IT Support', 'Operations'],
            'Agriculture': [],
            'Government': ['IT Support', 'Finance'],
            'Startups': ['Software Development', 'Design', 'Marketing', 'Product & Management', 'Artificial Intelligence'],
            'Remote Work': ['Freelance', 'Software Development', 'Design', 'Marketing', 'Media'],
            'Artificial Intelligence': ['Artificial Intelligence', 'Software Development', 'Data & Analytics'],
            'Operations': ['Operations', 'Quality Assurance', 'Product & Management'],
            'Gaming': ['Software Development', 'Design', 'Media'],
            'Consulting': ['Product & Management', 'Finance', 'IT Support'],
            'Infrastructure': ['Cloud & Infrastructure', 'IT Support', 'Operations'],
        }

        for interest in user_interests:
            mapped_categories = interest_mapping.get(interest, [])
            if job_category in mapped_categories:
                return True
        return False

    def _get_skill_gap_courses(self, missing_skills):
        """Get recommended courses for missing skills."""
        recommendations = []
        for skill in missing_skills:
            skill_lower = skill.lower().strip()
            if skill_lower in self.courses:
                course = self.courses[skill_lower]
                recommendations.append({
                    'skill': skill,
                    'course': course['title'],
                    'platform': course['platform'],
                    'duration': course['duration'],
                    'url': course['url'],
                })
            else:
                recommendations.append({
                    'skill': skill,
                    'course': f"Learn {skill.title()}",
                    'platform': 'Various',
                    'duration': '2-6 weeks',
                    'url': 'coursera.org',
                })
        return recommendations

    def match_jobs(self, user_skills, user_city, user_interests=None, top_n=10):
        """
        Main matching function.
        Returns top N job recommendations ranked by match score.
        """
        if user_interests is None:
            user_interests = []

        results = []

        for i, job in enumerate(self.jobs):
            skill_match = self._compute_skill_match(user_skills, job)
            location_match = self._compute_location_match(user_city)
            interest_match = self._compute_interest_match(user_interests, job['category'])

            # Weighted final score
            final_score = (
                skill_match['score'] * 0.6 +
                (100 if interest_match else 30) * 0.2 +
                (80 if location_match['available'] else 20) * 0.2
            )

            # Experience range
            avg_exp = (job['min_exp'] + job['max_exp']) / 2

            results.append({
                'job_title': job['title'],
                'category': job['category'],
                'description': job['description'],
                'final_score': round(final_score, 1),
                'skill_match': skill_match,
                'location': location_match,
                'interest_match': interest_match,
                'salary_range': f"INR {job['salary_min']}L - {job['salary_max']}L per annum",
                'experience_required': f"{job['min_exp']}-{job['max_exp']} years",
                'growth_path': job['growth_path'],
                'recommended_courses': self._get_skill_gap_courses(skill_match['missing_required'][:3]),
            })

        results.sort(key=lambda x: x['final_score'], reverse=True)
        return results[:top_n]

    def get_skill_gap_analysis(self, user_skills, target_job_title):
        """Detailed skill gap analysis for a specific job."""
        target_job = None
        for job in self.jobs:
            if job['title'].lower() == target_job_title.lower():
                target_job = job
                break

        if not target_job:
            return {"error": f"Job '{target_job_title}' not found"}

        skill_match = self._compute_skill_match(user_skills, target_job)
        courses = self._get_skill_gap_courses(skill_match['missing_required'])

        return {
            'target_job': target_job['title'],
            'current_skills': sorted(list(set(s.lower().strip() for s in user_skills))),
            'required_skills': target_job['required_skills'],
            'matched_skills': skill_match['matched_required'],
            'missing_skills': skill_match['missing_required'],
            'match_percentage': skill_match['required_score'],
            'recommended_courses': courses,
            'estimated_time': f"{len(courses) * 3} weeks" if courses else "Already qualified!",
        }

    def save_model(self, path):
        """Save the trained model to disk."""
        joblib.dump({
            'vectorizer': self.vectorizer,
            'job_vectors': self.job_vectors,
            'dataset': self.dataset,
        }, path)
        print(f"Model saved to {path}")

    @classmethod
    def load_model(cls, path):
        """Load a saved model from disk."""
        data = joblib.load(path)
        instance = cls.__new__(cls)
        instance.dataset = data['dataset']
        instance.jobs = instance.dataset['job_roles']
        instance.cities = instance.dataset['cities']
        instance.courses = instance.dataset['micro_courses']
        instance.all_skills = instance.dataset['skills']
        instance.vectorizer = data['vectorizer']
        instance.job_vectors = data['job_vectors']
        return instance


if __name__ == "__main__":
    dataset_path = "C:/Users/Adithya/NexaPath/backend/data/jobs_dataset.json"
    model_path = "C:/Users/Adithya/NexaPath/backend/models/nexapath_model.pkl"

    print("Initializing NexaPath Job Matcher...")
    matcher = NexaPathJobMatcher(dataset_path)

    print("Saving model...")
    matcher.save_model(model_path)

    # Test with a sample user
    print("\n--- Test Match ---")
    test_skills = ["python", "sql", "excel", "data analysis"]
    test_city = "Indore"
    test_interests = ["Technology", "Fintech"]

    results = matcher.match_jobs(test_skills, test_city, test_interests, top_n=5)

    for r in results:
        print(f"\n{r['job_title']} ({r['category']})")
        print(f"  Score: {r['final_score']}%")
        print(f"  Skill Match: {r['skill_match']['score']}%")
        print(f"  Salary: INR {r['salary_range']}")
        print(f"  Missing: {r['skill_match']['missing_required']}")
        if r['recommended_courses']:
            print(f"  Suggested: {r['recommended_courses'][0]['course']} ({r['recommended_courses'][0]['platform']})")

    # Test skill gap analysis
    print("\n--- Skill Gap Analysis ---")
    gap = matcher.get_skill_gap_analysis(test_skills, "Data Scientist")
    print(f"Target: {gap['target_job']}")
    print(f"Match: {gap['match_percentage']}%")
    print(f"Missing: {gap['missing_skills']}")
    print(f"Est. Time: {gap['estimated_time']}")
    for c in gap['recommended_courses']:
        print(f"  -> {c['course']} ({c['platform']}, {c['duration']})")
