from flask import Flask,render_template, send_from_directory

app = Flask(__name__, static_url_path='')

@app.route('/')
def main():
    return render_template('hybrid.html')

if __name__ == "__main__":
    app.run(debug = True)