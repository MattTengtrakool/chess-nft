from flask import Flask, render_template, request, redirect
from jpeg_creator import *


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/confirmation',  methods=["GET", "POST"])
def confirmation():
    if request.method == "POST":
        #get outputs
        output = request.form.get("boardoutput")
        print(output)
        board = generate_board()
        board = place_icons(board, output)

        cv2.imwrite("/static/images/generated_img.png",board)

        return render_template('result.html', image = board)

    else:
        return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)