from flask import Flask, request, jsonify
from lib.generate import Chat
from flask_cors import CORS

app = Flask(__name__)
CORS(
    app,
    resources={
        r"/generate": {"origins": [
            "http://localhost:3000",
            "http://130.63.65.112:3000"]}
    },
)


@app.route("/generate", methods=["POST"])
def generate_answer_endpoint():
    try:
        data = request.get_json()
        question = data.get("question", "")
        language = data.get("language", "")

        if not question or not language:
            return jsonify({"error": "Question & language are required"}), 400

        Tool = Chat(model="Qwen2.5-32b")
        response = Tool.generate(question=question, language=language)
        return jsonify({
            "response": response["response"],
            "meta_data": response["meta_data"]})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=50001, debug=True)
