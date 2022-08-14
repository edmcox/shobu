from board import BoardState
from flask import Flask, request, render_template

board_state = BoardState()
colours = {1: "Black", 2: "White"}

app = Flask(__name__)


@app.route("/")
def home():
    board_state.__init__()
    board_state.plot_board()
    return render_template("home.html")


@app.route("/solo", methods=["GET", "POST"])
def solo():

    player_move = None

    move_1_start = request.form.get("move_1_start")
    move_1_end = request.form.get("move_1_end")
    move_2_start = request.form.get("move_2_start")
    move_2_end = request.form.get("move_2_end")

    if request.method == "POST" and not board_state.game_over:
        player_move = board_state.make_move(
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

        board_state.check_win()

        if not board_state.game_over and not player_move:
            random_move_1, random_move_2 = board_state.random_move()

            board_state.make_move(
                random_move_1, random_move_2, colour=board_state.current_turn
            )

            board_state.plot_board()
            board_state.turn_no -= 1

            board_state.check_win()

    colour = colours[board_state.current_turn]
    turn_no = board_state.turn_no

    return render_template(
        "game.html",
        colour=colour,
        turn_no=turn_no,
        url="/static/images/board.png",
        player_move=player_move,
        game_over=board_state.game_over,
    )


@app.route("/multi", methods=["GET", "POST"])
def multi():

    player_move = None

    move_1_start = request.form.get("move_1_start")
    move_1_end = request.form.get("move_1_end")
    move_2_start = request.form.get("move_2_start")
    move_2_end = request.form.get("move_2_end")

    if request.method == "POST" and not board_state.game_over:
        player_move = board_state.make_move(
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

        board_state.check_win()

    colour = colours[board_state.current_turn]
    turn_no = board_state.turn_no

    return render_template(
        "game.html",
        colour=colour,
        turn_no=turn_no,
        url="/static/images/board.png",
        player_move=player_move,
        game_over=board_state.game_over,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0")
