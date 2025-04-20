from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# 국어기초사전 API 설정
API_KEY = "ED5A9F18DA7C6BD26CD1FDDDD18D70D5"
API_URL = "https://krdict.korean.go.kr/api/search"

@app.route("/word", methods=["GET"])
def search_word():
    word = request.args.get("word")

    if not word:
        return jsonify({"error": "검색할 단어를 입력해주세요."}), 400

    params = {
        "key": API_KEY,
        "q": word,
        "req_type": "json"  # 응답을 JSON으로 받기
    }

    response = requests.get(API_URL, params=params)

    if response.status_code != 200:
        return jsonify({"error": "외부 API 요청 실패"}), 500

    data = response.json()

    if "channel" not in data or "item" not in data["channel"]:
        return jsonify({"error": "단어를 찾을 수 없습니다."}), 404

    results = []
    for item in data["channel"]["item"]:
        results.append({
            "word": item.get("word"),
            "pos": item.get("pos"),
            "definition": item["sense"][0]["definition"] if "sense" in item else ""
        })

    return jsonify({"results": results})

if __name__ == "__main__":
    app.run(debug=True)
