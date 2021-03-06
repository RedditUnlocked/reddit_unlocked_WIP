#
# -To be used for locally (localhost) testing the web server/website.
# -Installing the flask package on a virtual environment (instead of system-wide)
# is recommended by Flask devs.
#
# http://flask.pocoo.org/docs/0.12/quickstart/#
#
# -Isaac Park, keonp2
#


from flask import Flask, request, render_template, redirect, url_for, session
from flask_session import Session
from run import display_praw, stats_praw, body_to_graph, get_keyword_dict


app = Flask(__name__)
app.config['SECRET_KEY'] = 'insert super secret string here'
SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
Session(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'basic-url' in request.form:
            name = request.form['basic-url']
            info = stats_praw(name)
            session['info'] = info
            output = display_praw(name)
            session['output'] = output
            keywords = get_keyword_dict(output)
            graph_url = body_to_graph(keywords, name)
            session['graph_url'] = graph_url
            return redirect(url_for('program', name=name))
        else:
            return render_template('home.html')
            # TODO: Implement subreddit input validity checking AKA Fix blank input error
    else:
        return render_template('home.html')


@app.route('/docs/<section>')
def docs(section):
    if section == "findings":
        return render_template("docs_findings.html")
    else:
        if section == "team":
            return render_template("docs_team.html")
        else:
            if section == "tools":
                return render_template("docs_tools.html")
            else:
                return "This docs page does not exist. Maybe it was a typo? <br><br> -Isaac <br><br><a href='/'>Back to Reddit_Unlocked Home</a>"
                # TODO: if I have time, implement html template for page DNE message


@app.route('/program/<name>')
def program(name):
    output = session['output']
    info = session['info']
    graph_url = session['graph_url']
    return render_template('program.html', name=name, output=output, info=info, graph_url=graph_url)


@app.route('/examples')
def examples():
    return render_template('examples.html')


if __name__ == "__main__":
    app.run(debug=True)


# Use url_for method for links in the webpage; url_for generates URL
# based on the argument it is given (name of the function related to a URL.
#
# Example:
#
# @app.route('/user/<name>')
# def hello_user(name):
#   if name =='admin':
#      return redirect(url_for('hello_admin'))
#   else:
#      return redirect(url_for('hello_guest',guest = name))
#
