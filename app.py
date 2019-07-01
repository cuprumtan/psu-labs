from flask import Flask, render_template

app = Flask(__name__)


@app.route('/begin', methods=['GET', 'POST'])
def test_begin():
    return render_template('start.html')


@app.route('/testing', methods=['POST'])
def testing():
    return render_template('testing.html')


@app.route('/result', methods=['POST'])
def test_result():
    return render_template('result.html')


@app.route('/manage', methods=['GET', 'POST'])
def manage_server():
    return render_template('server.html')


if __name__ == '__main__':
    app.run()
