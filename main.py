from flask import Flask, render_template, request
from slugify import slugify
from werkzeug.datastructures import CombinedMultiDict
import json


app = Flask(__name__)
MAX_QUESTIONS = 3 #non-inclusive since questions start at 0
data_memory = dict()

@app.route("/")
def main_page():
    return render_template("index.html", num=0, username=None)

@app.route("/next-question", methods=["POST"])
def next_question():
    print(request.form)
    question_num = int(request.form["question-num"])

    username = request.form["username"] if "username" in request.form else slugify(request.form["name"])
    if question_num == 0:
        data_memory[username] = {"name": request.form["name"], "username": username}
    else:
        for attribute in request.form:
            value = request.form.getlist(attribute)

            # we always get a list but want to flatten when only 1 item
            value = value if len(value) > 1 else value[0]
            data_memory[username][attribute] = value
    
    print("after merge", data_memory)

    if question_num >= MAX_QUESTIONS-1:
        save_to_file(data_memory[username])
        return "<p> all done! </p>"

    return render_template("question.html", num=min(question_num+1, MAX_QUESTIONS), username=username)

def save_to_file(data_multidict):
    filename = slugify(data_multidict["name"]) + ".json"
    print(f"Writing to file '{filename}'")

    with open(filename, 'w', encoding="utf-8") as f:
        json.dump(data_multidict, f, ensure_ascii=False)

if __name__ == "__main__":
    app.run()