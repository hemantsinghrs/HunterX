import sys
sys.stdout.reconfigure(encoding='utf-8')

from flask import Flask, request, jsonify,render_template

from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
    return render_template("index.html")


# 👇 यहाँ अपनी Google Gemini API Key डालना
GEMINI_API_KEY = "AIzaSyCHGQXXIQ7_sjPpyCVB1WqOWfU3QMYsIz4"

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    question = data.get("question")

    if not question:
        return jsonify({"error": "❌ कोई सवाल नहीं मिला"}), 400

    try:
        response = requests.post(
            f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}",
            headers={"Content-Type": "application/json"},
            json={
                "contents": [
                    {"parts": [{"text": f"तू एक AI है जो इस सवाल को headings और parts में detail में explain करता है:\n{question}"}]}
                ]
            }
        )

        print("📩 Gemini Status:", response.status_code)
        print("📦 Raw Gemini Response:", response.text)

        result = response.json()

        if "candidates" not in result:
            return jsonify({"error": f"'candidates' not in response: {result}"}), 500

        answer = result['candidates'][0]['content']['parts'][0]['text']
        return jsonify({"answer": answer})

    except Exception as e:
        print("🔥 INTERNAL SERVER ERROR:", e)
        return jsonify({"error": str(e)}), 500
    

if __name__ == '__main__':
    app.run(debug=True)
