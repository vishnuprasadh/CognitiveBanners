from flask import request,render_template,Flask
app = Flask(__name__)

@app.route("/home")
def render_home_page:
    return render_template('../resources/AjioHome.html')


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=int(5002),debug=True)