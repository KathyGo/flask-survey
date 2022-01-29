from flask import Flask, request, flash, render_template, redirect
from flask_debugtoolbar import DebugToolbarExtension
from surveys import surveys

app = Flask("__name__")
app.config['SECRET_KEY']="123"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS']=False
debug = DebugToolbarExtension(app)


response=[]

@app.route("/")
def start_survey():
    survey = surveys["satisfaction"]
    return render_template("start.html", survey = survey)

@app.route("/questions/<int:index>")
def survey_questions(index):
    survey = surveys["satisfaction"]
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
    return render_template("questions.html", question=q, index=index, choices=choices)

@app.route("/answer", methods=["POST"])
def answer():
    survey = surveys["satisfaction"]
    questions = survey.questions
    answer = request.form["choices"]
    response.append(answer)
    # import pdb
    # pdb.set_trace()
    print(response)
    index = len(response)
    if index < len(questions):
        return redirect(f"/questions/{index}")
    else:
        return redirect("/completed")

@app.route("/completed")
def completed():
    return render_template("completed.html")