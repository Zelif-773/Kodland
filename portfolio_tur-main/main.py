# Import
from flask import Flask, render_template,request, redirect



app = Flask(__name__)

# İçerik sayfasını çalıştırma
@app.route('/')
def index():
    return render_template('index.html')


# Dinamik beceriler
@app.route('/', methods=['POST'])
def process_form():
    button_unity = request.form.get('button_unity')
    button_oneshot = request.form.get('button_oneshot')
    button_undertale = request.form.get('button_undertale')
    button_hk = request.form.get('button_hk')

    return render_template('index.html', button_unity=button_unity, button_oneshot=button_oneshot, button_undertale=button_undertale, button_hk=button_hk)


if __name__ == "__main__":
    app.run(debug=True)
