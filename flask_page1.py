
from flask import Flask, request, abort

app = Flask(__name__)

@app.route('/')
def homepage():
    return 'Hello, World!;lasjd;lfajsdf;lajsf;l'

@app.route('/test')
def in_test_page():
    return 'In test page'

if __name__ == "__main__":
    app.run()
