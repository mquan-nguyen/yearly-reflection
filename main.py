from flask import Flask, render_template, request, redirect, url_for
from slugify import slugify
import json
import glob


app = Flask(__name__)
MAX_QUESTIONS = 7 #non-inclusive since questions start at 0
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
        return render_template("ending.html")

    return render_template("question.html", num=min(question_num+1, MAX_QUESTIONS), username=username)

@app.route("/everyone")
def view_all_names():
    # it's probably a better pattern to only access the names
    # but i have a feeling that I might use more data in the future
    people = get_all_data()

    print(people)
    return render_template("everyone.html", people=people.values())

@app.route("/<string:username>")
def profile(username: str):
    people = get_all_data()

    if username not in people:
        return render_template("404.html", code=404)
    
    return render_template("person.html", person=people[username])

def get_all_data() -> dict[str, dict[str, str]]:
    json_files = get_all_data_filenames()
    people = dict() # username -> person
    for filename in json_files:
        with open(filename, 'r') as f:
            person = json.load(f) 
        people[person["username"]] = person

    return people

def get_all_data_filenames() -> list[str]:
    directory_path = "data/"
    json_files = glob.glob(f"{directory_path}/*.json")
    print(json_files)
    return json_files

def save_to_file(data_multidict):
    filename = slugify(data_multidict["name"]) + ".json"
    print(f"Writing to file '{filename}'")

    with open(f"data/{filename}", 'w', encoding="utf-8") as f:
        json.dump(data_multidict, f, ensure_ascii=False)

if __name__ == "__main__":
    app.run()