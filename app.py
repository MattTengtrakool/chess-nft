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
        print("here")
        output = request.form.get("boardoutput")
        tempArray = output.split(',')
        for x in range(len(tempArray)):
            if tempArray[x] == "":
                tempArray[x] = 0
            tempArray[x] = int(tempArray[x])
        instructionArray = []
        for i in range(8):
            tempRow = []
            for j in range(8):  
                tempRow.append(tempArray[j+(8*i)])
            instructionArray.append(tempRow)
        print(instructionArray)
        board = generate_board()
        board = place_icons(board, instructionArray)

        cv2.imwrite("/static/images/generated_img.png",board)

        return render_template('result.html', image = board)

    else:
        return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
