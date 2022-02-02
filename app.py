from flask import Flask, request, flash, render_template, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import surveys

app = Flask("__name__")
app.config['SECRET_KEY']="123"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS']=False
debug = DebugToolbarExtension(app)

@app.route("/")
def select_survey():
    return render_template("home.html", surveys = surveys)

@app.route("/", methods=["POST"])
def set_response():
    name = request.form.get("survey")

    if session.get(f"completed_{name}"):
        return redirect("/completed")

    session["curr_survey"] = name 
    session["responses"] = {}
    session["comments"] = {}
    return redirect("/start")

@app.route("/start")
def start_survey():
    name = session["curr_survey"]
    # survey_name.append(name)
    survey = surveys[name]
    return render_template("start.html", survey = survey)

@app.route("/questions/<int:index>")
def survey_questions(index):
    name = session["curr_survey"]
    survey = surveys[name]
    questions = survey.questions
    response = session["responses"]
    i = len(response)
    if i<len(questions) and index != i:
        flash("You were trying to reach to the wrong question!", "error")
        flash("Redirecting back...", "error")
        index = i
        return redirect(f"/questions/{index}")
    elif i==len(questions):
        return redirect("/completed")

    q = questions[index]
    choices = q.choices
    comment = q.allow_text
    return render_template("questions.html", question=q, index=index, choices=choices, allow_text=comment)

@app.route("/answer", methods=["POST"])
def answer():
    name = session["curr_survey"]
    survey = surveys[name]
    questions = survey.questions
    answer = request.form["choices"]
    # import pdb
    # pdb.set_trace()
    # print(response)
    response = session["responses"]
    index = len(response)
    q = questions[index]
    title = q.question
    response[title]=answer
    session["responses"] = response
    
    if q.allow_text:
        comment = request.form["comments"]
        comments = session.get("comments")
        comments[title] = comment
        session["comments"] = comments
    
    index = index + 1
    if index < len(questions):
        return redirect(f"/questions/{index}")
    else:
        return redirect("/completed")

@app.route("/completed")
def completed():
    name = session["curr_survey"]
    session[f"completed_{name}"] = True
    survey = surveys[name]
    questions = survey.questions
    response = session["responses"]
    return render_template("completed.html", response=response, comments=session.get("comments"))