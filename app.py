from flask import Flask, request, jsonify
from collections import OrderedDict


app = Flask(__name__)

# Your details
FULL_NAME = "john_doe"   # lowercase
DOB = "17091999"         # ddmmyyyy
EMAIL = "john@xyz.com"
ROLL_NUMBER = "ABCD123"


def alternating_caps_reverse_concat(alphabets):
    concat_str = "".join(alphabets)
    reversed_str = concat_str[::-1]

    result = ""
    for i, ch in enumerate(reversed_str):
        if i % 2 == 0:
            result += ch.upper()
        else:
            result += ch.lower()
    return result


@app.route("/bfhl", methods=["POST"])
def bfhl():
    try:
        data = request.get_json().get("data", [])

        if not isinstance(data, list):
            return jsonify(OrderedDict([
                ("is_success", False),
                ("message", "Invalid input. 'data' must be an array.")
            ])), 400

        even_numbers = []
        odd_numbers = []
        alphabets = []
        special_chars = []
        total_sum = 0

        for item in data:
            if item.isdigit():
                num = int(item)
                if num % 2 == 0:
                    even_numbers.append(item)
                else:
                    odd_numbers.append(item)
                total_sum += num
            elif item.isalpha():
                alphabets.append(item.upper())
            else:
                special_chars.append(item)

        response = OrderedDict([
            ("is_success", True),
            ("user_id", f"{FULL_NAME}_{DOB}"),
            ("email", EMAIL),
            ("roll_number", ROLL_NUMBER),
            ("odd_numbers", odd_numbers),
            ("even_numbers", even_numbers),
            ("alphabets", alphabets),
            ("special_characters", special_chars),
            ("sum", str(total_sum)),
            ("concat_string", alternating_caps_reverse_concat(alphabets))
        ])

        return jsonify(response), 200

    except Exception as e:
        return jsonify(OrderedDict([
            ("is_success", False),
            ("message", "Server error"),
            ("error", str(e))
        ])), 500

@app.route("/", methods=["GET"])
def home():
    return "BFHL API running!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
