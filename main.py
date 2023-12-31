from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def main_page():
    return render_template("index.html")

@app.route("/next-question", methods=["POST"])
def next_question():
    print(request.get_data())
    print(request.form)
    return render_template("question.html", num=1)

if __name__ == "__main__":
    app.run()