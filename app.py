from flask import Flask, request, flash, render_template, redirect
from flask_debugtoolbar import DebugToolbarExtension
from surveys import surveys

app = Flask("__name__")
app.config['SECRET_KEY']="123"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS']=False
debug = DebugToolbarExtension(app)


response={}
survey_name = []
answer_comments={}

@app.route("/")
def select_survey():
    return render_template("home.html", surveys = surveys)

@app.route("/start")
def start_survey():
    name = request.args.get("survey")
    survey_name.append(name)
    survey = surveys[name]
    return render_template("start.html", survey = survey)

@app.route("/questions/<int:index>")
def survey_questions(index):
    name = survey_name[0]
    survey = surveys[name]
    questions = survey.questions
    i = len(response)
    if i<len(questions) and index != i:
        flash(u"You are trying to reach to the wrong question!", "error")
        flash(u"Redirecting...", "error")
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
    name = survey_name[0]
    survey = surveys[name]
    questions = survey.questions
    answer = request.form["choices"]
    # import pdb
    # pdb.set_trace()
    # print(response)
    index = len(response)
    q = questions[index]
    title = q.question
    response[title]=answer
    
    if q.allow_text:
        comment = request.form["comments"]
        answer_comments[title]=comment
    
    index = index + 1
    if index < len(questions):
        return redirect(f"/questions/{index}")
    else:
        return redirect("/completed")

@app.route("/completed")
def completed():
    name = survey_name[0]
    survey = surveys[name]
    questions = survey.questions
    return render_template("completed.html", response=response, comments=answer_comments)