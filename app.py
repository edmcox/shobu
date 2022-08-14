from board import BoardState
from check import check_move, check_win
from flask import Flask, request, render_template

board_state = BoardState()
colours = {1: "Black", 2: "White"}
multiplayer = False

app = Flask(__name__)


@app.route("/")
def home():
    board_state.plot_board()
    return render_template("home.html")


@app.route("/game", methods=["GET", "POST"])
def game():

    move_1_start = request.form.get("move_1_start")
    move_1_end = request.form.get("move_1_end")
    move_2_start = request.form.get("move_2_start")
    move_2_end = request.form.get("move_2_end")

    if request.method == "POST":
        board_state.make_move(
            move_1=[
                [int(x.strip()) for x in move_1_start.split(",")],
                [int(x.strip()) for x in move_1_end.split(",")],
            ],
            move_2=[
                [int(x.strip()) for x in move_2_start.split(",")],
                [int(x.strip()) for x in move_2_end.split(",")],
            ],
            colour=board_state.current_turn,
        )

        board_state.plot_board()

        if not multiplayer:
            random_move_1, random_move_2 = board_state.random_move()[0]
            board_state.make_move(
                random_move_1, random_move_2, colour=board_state.current_turn
            )

    colour = colours[board_state.current_turn]
    turn_no = board_state.turn_no

    return render_template(
        "game.html", colour=colour, turn_no=turn_no, url="/static/images/board.png"
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0")
