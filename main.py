from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def main_page():
    return render_template("index.html", num=1)

@app.route("/next-question", methods=["POST"])
def next_question():
    print(request.get_data())
    print(request.form)
    question_num = request.form["question-num"]
    return render_template("index.html", num=min(int(question_num)+1, 10))

if __name__ == "__main__":
    app.run()