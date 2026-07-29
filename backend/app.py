from flask import Flask, request, jsonify
from flask_cors import CORS
from models.job_matcher import NexaPathJobMatcher
from models.career_agent import CareerAgent
import os

app = Flask(__name__)
CORS(app)

DATASET_PATH = os.path.join(os.path.dirname(__file__), 'data', 'jobs_dataset.json')

print("Loading NexaPath model...")
matcher = NexaPathJobMatcher(DATASET_PATH)
agent = CareerAgent(matcher)
print("NexaPath AI Agent loaded.")


@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({
        "status": "ok",
        "message": "NexaPath AI Agent is running",
        "agent": "CareerAgent v2.0",
        "sdgs": ["SDG 4", "SDG 8", "SDG 10"],
    })


@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Main AI Agent endpoint.
    Request: {"message": "I know Python and SQL, I'm in Indore"}
    Response: {"response": "...", "state": {...}}
    """
    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({"error": "Message is required"}), 400

    user_message = data['message']
    response = agent.process_message(user_message)

    return jsonify({
        "response": response,
        "state": agent.conversation_state,
        "profile": agent._build_profile(agent.conversation_state),
    })


@app.route('/api/chat/reset', methods=['POST'])
def chat_reset():
    """Reset the agent conversation state."""
    agent.conversation_state = {}
    agent.session_log = []
    return jsonify({"status": "ok", "message": "Conversation reset"})


@app.route('/api/chat/history', methods=['GET'])
def chat_history():
    """Get conversation history."""
    return jsonify({
        "log": agent.session_log,
        "summary": agent.get_session_summary(),
    })


@app.route('/api/match', methods=['POST'])
def match_jobs():
    """Direct job matching endpoint (for non-conversational use)."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body is required"}), 400

    skills = data.get('skills', [])
    city = data.get('city', '')
    interests = data.get('interests', [])
    top_n = data.get('top_n', 10)

    if not skills or not city:
        return jsonify({"error": "Skills and city are required"}), 400

    results = matcher.match_jobs(skills, city, interests, top_n)
    return jsonify({"results": results, "count": len(results)})


@app.route('/api/skill-gap', methods=['POST'])
def skill_gap():
    """Direct skill gap analysis endpoint."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body is required"}), 400

    skills = data.get('skills', [])
    target_job = data.get('target_job', '')

    if not skills or not target_job:
        return jsonify({"error": "Skills and target job are required"}), 400

    result = matcher.get_skill_gap_analysis(skills, target_job)
    if 'error' in result:
        return jsonify(result), 404
    return jsonify(result)


@app.route('/api/skills', methods=['GET'])
def get_skills():
    return jsonify({"skills": matcher.all_skills, "count": len(matcher.all_skills)})


@app.route('/api/cities', methods=['GET'])
def get_cities():
    return jsonify({"cities": matcher.cities, "count": len(matcher.cities)})


@app.route('/api/jobs', methods=['GET'])
def get_jobs():
    jobs_brief = []
    for job in matcher.jobs:
        jobs_brief.append({
            "title": job['title'],
            "category": job['category'],
            "description": job['description'],
            "required_skills": job['required_skills'],
        })
    return jsonify({"jobs": jobs_brief, "count": len(jobs_brief)})


@app.route('/api/sdgs', methods=['GET'])
def get_sdgs():
    return jsonify({
        "sdgs": [
            {"id": "SDG 4", "name": "Quality Education", "description": "Personalized learning paths and skill development"},
            {"id": "SDG 8", "name": "Decent Work and Economic Growth", "description": "Connecting talent with opportunities in Tier-2/3 cities"},
            {"id": "SDG 10", "name": "Reduced Inequalities", "description": "Bridging the opportunity gap for non-metro talent"},
        ]
    })


if __name__ == '__main__':
    app.run(debug=True, port=5000)
