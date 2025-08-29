from flask import Flask, request, Response
import json
from collections import OrderedDict


app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

FULL_NAME = "v_kamal_jerome"
DOB = "15092004"
EMAIL = "kamaljerome.v2022@vitstudent.ac.in"
ROLL_NUMBER = "22BAI1212"


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
        payload = request.get_json()

        # ✅ Case 1: No JSON body or missing "data"
        if not payload or "data" not in payload:
            error_resp = OrderedDict([
                ("is_success", False),
                ("message", "Missing 'data' field in request body.")
            ])
            return Response(
                json.dumps(error_resp, ensure_ascii=False, sort_keys=False),
                mimetype="application/json",
                status=400
            )

        data = payload["data"]

        # ✅ Case 2: "data" exists but is not a list
        if not isinstance(data, list):
            error_resp = OrderedDict([
                ("is_success", False),
                ("message", "Invalid input. 'data' must be an array.")
            ])
            return Response(
                json.dumps(error_resp, ensure_ascii=False, sort_keys=False),
                mimetype="application/json",
                status=400
            )

        # Normal processing
        even_numbers = []
        odd_numbers = []
        alphabets = []
        special_chars = []
        total_sum = 0

        for item in data:
            if isinstance(item, str) and item.isdigit():
                num = int(item)
                if num % 2 == 0:
                    even_numbers.append(item)
                else:
                    odd_numbers.append(item)
                total_sum += num
            elif isinstance(item, str) and item.isalpha():
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

        return Response(
            json.dumps(response, ensure_ascii=False, sort_keys=False),
            mimetype="application/json",
            status=200
        )

    except Exception as e:
        error_resp = OrderedDict([
            ("is_success", False),
            ("message", "Server error"),
            ("error", str(e))
        ])
        return Response(
            json.dumps(error_resp, ensure_ascii=False, sort_keys=False),
            mimetype="application/json",
            status=500
        )

@app.route("/", methods=["GET"])
def home():
    return "BFHL API running!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
