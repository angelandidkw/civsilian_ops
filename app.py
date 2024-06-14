from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

@app.route('/get_user_id', methods=['POST'])
def get_user_id():
    username = request.json.get('username')

    if not username:
        return jsonify({"error": "Username not provided"})

    result = get_roblox_user_id(username)
    return jsonify(result)

def get_roblox_user_id(username):
    url = "https://users.roblox.com/v1/usernames/users"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "usernames": [username]
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()  # Raise HTTPError for bad responses

        data = response.json()

        # Check if the user exists
        if not data['data']:
            return {"error": f"No user found with username: {username}"}

        # Assuming the first result is the most relevant one
        user_info = data['data'][0]
        user_id = user_info['id']

        return {"username": username, "user_id": user_id}

    except requests.exceptions.HTTPError as http_err:
        return {"error": f"HTTP error occurred: {http_err}"}
    except Exception as err:
        return {"error": f"An error occurred: {err}"}

if __name__ == '__main__':
    app.run(debug=True)
