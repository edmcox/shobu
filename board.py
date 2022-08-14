import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.patches import Circle
import itertools
import random as rand


class BoardState:
    def __init__(self):
        #  black = 1, white = 2, space = 0
        self.board = [[2] * 8]
        for i in range(2):
            self.board.append([0] * 8)
        self.board.append([1] * 8)
        self.board.append([2] * 8)
        for i in range(2):
            self.board.append([0] * 8)
        self.board.append([1] * 8)

        self.board_descriptions = {
            1: {
                "bounds": [[0, 3], [0, 3]],
                "home_colour": 2,
                "board_colour": 1,
            },  # white home, black board
            2: {
                "bounds": [[0, 3], [4, 7]],
                "home_colour": 2,
                "board_colour": 2,
            },  # white home, white board
            3: {
                "bounds": [[4, 7], [0, 3]],
                "home_colour": 1,
                "board_colour": 1,
            },  # black home, black board
            4: {
                "bounds": [[4, 7], [4, 7]],
                "home_colour": 1,
                "board_colour": 2,
            },  # black home, white board
        }

        self.current_turn = 1
        self.turn_no = 1
        self.game_over = False

    def plot_board(self):
        print("Plotting board")
        boards = [
            [0, 0, 0, 0, 1, 1, 1, 1],
            [0, 0, 0, 0, 1, 1, 1, 1],
            [0, 0, 0, 0, 1, 1, 1, 1],
            [0, 0, 0, 0, 1, 1, 1, 1],
            [0, 0, 0, 0, 1, 1, 1, 1],
            [0, 0, 0, 0, 1, 1, 1, 1],
            [0, 0, 0, 0, 1, 1, 1, 1],
            [0, 0, 0, 0, 1, 1, 1, 1],
        ]

        plt.matshow(boards, cmap=ListedColormap(["#725338", "#c3aa67"]))
        ax = plt.gca()
        ax.set_xticks([x - 0.5 for x in range(1, 8)], minor=True)
        ax.set_yticks([y - 0.5 for y in range(1, 8)], minor=True)
        plt.grid(which="minor", ls="-", lw=2)
        plt.grid(c="k", lw="2", which="minor")

        for y, row in enumerate(self.board):
            for x, piece in enumerate(row):
                if piece == 2:
                    circ = Circle((x, y), 0.3, facecolor="w")
                    ax.add_patch(circ)
                elif piece == 1:
                    circ = Circle((x, y), 0.3, facecolor="k")
                    ax.add_patch(circ)

        plt.savefig("static/images/board.png", bbox_inches="tight")

    def make_move(self, move_1, move_2, colour):
        print("Making move")
        print(move_1, move_2)
        print(colour)
        self.board_descriptions

        # check to see if moving same colour piece both moves
        if (
            self.board[move_1[0][0]][move_1[0][1]]
            == self.board[move_2[0][0]][move_2[0][1]]
            and self.board[move_1[0][0]][move_1[0][1]] == colour
        ):
            print("check to see if moving same colour piece both moves")
            piece = self.board[move_1[0][0]][move_1[0][1]]  # colour of piece

            # check length of move 1 doesn't exceed 2 squares and is straight/diagonal
            move_1_y_dist = move_1[1][0] - move_1[0][0]
            move_1_x_dist = move_1[1][1] - move_1[0][1]
            sum_moves_1 = abs(move_1_y_dist) + abs(move_1_x_dist)
            if (
                abs(move_1_y_dist) <= 2 and abs(move_1_x_dist) <= 2 and sum_moves_1 != 3
            ):  # and sum_moves_1 != 0:
                print(
                    "check length of move 1 doesn't exceed 2 squares and is straight/diagonal"
                )

                # check length of move 2 doesn't exceed 2 squares
                move_2_y_dist = move_2[1][0] - move_2[0][0]
                move_2_x_dist = move_2[1][1] - move_2[0][1]
                sum_moves_2 = abs(move_2_y_dist) + abs(move_2_x_dist)
                if (
                    abs(move_2_y_dist) <= 2
                    and abs(move_2_x_dist) <= 2
                    and sum_moves_2 != 3
                ):  # and sum_moves_2 != 0:
                    print("check length of move 2 doesn't exceed 2 squares")

                    # check to see if move 1 and move 2 are the same
                    if (
                        move_1_y_dist == move_2_y_dist
                        and move_1_x_dist == move_2_x_dist
                    ):
                        print("check to see if move 1 and move 2 are the same")

                        same_board_1 = False  # True if move 1 stays on same board
                        same_board_2 = False  # True if move 2 stays on same board
                        valid_board_1 = False  # True if move 2 is on home board
                        valid_board_2 = (
                            False  # True if move 2 is on opposite colour board
                        )

                        # check to see if move 1 stays on same board and is made on a home board
                        for board_id, desc in self.board_descriptions.items():
                            if all(
                                [
                                    move_1[0][0] >= desc["bounds"][0][0],
                                    move_1[0][0] <= desc["bounds"][0][1],
                                    move_1[0][1] >= desc["bounds"][1][0],
                                    move_1[0][1] <= desc["bounds"][1][1],
                                    move_1[1][0] >= desc["bounds"][0][0],
                                    move_1[1][0] <= desc["bounds"][0][1],
                                    move_1[1][1] >= desc["bounds"][1][0],
                                    move_1[1][1] <= desc["bounds"][1][1],
                                    piece == desc["home_colour"],
                                ]
                            ):

                                board_1 = board_id
                                same_board_1 = True
                                valid_board_1 = True
                                board_colour_1 = desc["board_colour"]
                                break

                        if valid_board_1 == True and same_board_1 == True:

                            # check to see if move 2 stays on same board and is made on a board of the opposite colour
                            for board_id, desc in self.board_descriptions.items():
                                if all(
                                    [
                                        move_2[0][0] >= desc["bounds"][0][0],
                                        move_2[0][0] <= desc["bounds"][0][1],
                                        move_2[0][1] >= desc["bounds"][1][0],
                                        move_2[0][1] <= desc["bounds"][1][1],
                                        move_2[1][0] >= desc["bounds"][0][0],
                                        move_2[1][0] <= desc["bounds"][0][1],
                                        move_2[1][1] >= desc["bounds"][1][0],
                                        move_2[1][1] <= desc["bounds"][1][1],
                                        board_colour_1 != desc["board_colour"],
                                    ]
                                ):

                                    board_2 = board_id
                                    same_board_2 = True
                                    valid_board_2 = True
                                    break

                            print(
                                f"same_board_1: {same_board_1} \nvalid_board_1: {valid_board_1} \nsame_board_2: {same_board_2} \nvalid_board_2: {valid_board_2}"
                            )

                            if (
                                same_board_1 == True
                                and valid_board_1 == True
                                and same_board_2 == True
                                and valid_board_2 == True
                            ):
                                print(
                                    "check to see if move 1 and move 2 stay on same board and is made on a home board"
                                )

                                # check to see if passive move 1 interacts with other stones
                                valid_passive = False

                                # moved one space
                                if abs(move_1_x_dist) == 1 or abs(move_1_y_dist) == 1:
                                    if self.board[move_1[1][0]][move_1[1][1]] == 0:
                                        valid_passive = True

                                # moved two spaces
                                elif abs(move_1_x_dist) == 2 or abs(move_1_y_dist) == 2:
                                    print("move 1 length 2")
                                    if (
                                        self.board[
                                            int(move_1[1][0] - move_1_y_dist / 2)
                                        ][int(move_1[1][1] - move_1_x_dist / 2)]
                                        == 0
                                        and self.board[move_1[1][0]][move_1[1][1]] == 0
                                    ):
                                        valid_passive = True

                                if valid_passive == True:
                                    print("valid passive")

                                    # check to see if move 2 either pushes no stones or pushes none of its own stones and max 1 stone
                                    valid_push = False

                                    # moved one space
                                    if (
                                        abs(move_2_x_dist) == 1
                                        or abs(move_2_y_dist) == 1
                                    ):
                                        # no push
                                        if self.board[move_2[1][0]][move_2[1][1]] == 0:
                                            valid_push = True

                                        # check if piece interacts with opponent piece
                                        elif (
                                            self.board[move_2[1][0]][move_2[1][1]]
                                            != self.board[move_2[0][0]][move_2[0][1]]
                                        ):

                                            # check if piece pushed off
                                            if any(
                                                [
                                                    move_2[1][0] + move_2_y_dist
                                                    < self.board_descriptions[board_2][
                                                        "bounds"
                                                    ][0][0],
                                                    move_2[1][0] + move_2_y_dist
                                                    > self.board_descriptions[board_2][
                                                        "bounds"
                                                    ][0][1],
                                                    move_2[1][1] + move_2_x_dist
                                                    < self.board_descriptions[board_2][
                                                        "bounds"
                                                    ][1][0],
                                                    move_2[1][1] + move_2_x_dist
                                                    > self.board_descriptions[board_2][
                                                        "bounds"
                                                    ][1][1],
                                                ]
                                            ):

                                                # remove piece
                                                self.board[move_2[1][0]][
                                                    move_2[1][1]
                                                ] = 0
                                                valid_push = True

                                            # check if pushed piece is not pushing other piece
                                            elif (
                                                self.board[
                                                    move_2[1][0] + move_2_y_dist
                                                ][move_2[1][1] + move_2_x_dist]
                                                == 0
                                            ):
                                                # push piece
                                                pushed_piece = self.board[move_2[1][0]][
                                                    move_2[1][1]
                                                ]
                                                self.board[move_2[1][0]][
                                                    move_2[1][1]
                                                ] = 0
                                                self.board[
                                                    move_2[1][0] + move_2_y_dist
                                                ][
                                                    move_2[1][1] + move_2_x_dist
                                                ] = pushed_piece
                                                valid_push = True

                                    # moved two spaces
                                    elif (
                                        abs(move_2_x_dist) == 2
                                        or abs(move_2_y_dist) == 2
                                    ):
                                        # no push
                                        if (
                                            self.board[
                                                int(move_2[1][0] - move_2_y_dist / 2)
                                            ][int(move_2[1][1] - move_2_x_dist / 2)]
                                            == 0
                                            and self.board[move_2[1][0]][move_2[1][1]]
                                            == 0
                                        ):
                                            print("no piece in path")
                                            valid_push = True

                                        # check if only one opponents piece is in pieces path
                                        elif any(
                                            [
                                                (
                                                    self.board[
                                                        int(
                                                            move_2[1][0]
                                                            - move_2_y_dist / 2
                                                        )
                                                    ][
                                                        int(
                                                            move_2[1][1]
                                                            - move_2_x_dist / 2
                                                        )
                                                    ]
                                                    == 0
                                                    and self.board[move_2[1][0]][
                                                        move_2[1][1]
                                                    ]
                                                    != self.board[move_2[0][0]][
                                                        move_2[0][1]
                                                    ]
                                                ),
                                                (
                                                    self.board[
                                                        int(
                                                            move_2[1][0]
                                                            - move_2_y_dist / 2
                                                        )
                                                    ][
                                                        int(
                                                            move_2[1][1]
                                                            - move_2_x_dist / 2
                                                        )
                                                    ]
                                                    != self.board[move_2[0][0]][
                                                        move_2[0][1]
                                                    ]
                                                    and self.board[move_2[1][0]][
                                                        move_2[1][1]
                                                    ]
                                                    == 0
                                                ),
                                            ]
                                        ):
                                            print("only one piece in path")

                                            # check if piece pushed off
                                            if any(
                                                [
                                                    int(
                                                        move_2[1][0] + move_2_y_dist / 2
                                                    )
                                                    < self.board_descriptions[board_2][
                                                        "bounds"
                                                    ][0][0],
                                                    int(
                                                        move_2[1][0] + move_2_y_dist / 2
                                                    )
                                                    > self.board_descriptions[board_2][
                                                        "bounds"
                                                    ][0][1],
                                                    int(
                                                        move_2[1][1] + move_2_x_dist / 2
                                                    )
                                                    < self.board_descriptions[board_2][
                                                        "bounds"
                                                    ][1][0],
                                                    int(
                                                        move_2[1][1] + move_2_x_dist / 2
                                                    )
                                                    > self.board_descriptions[board_2][
                                                        "bounds"
                                                    ][1][1],
                                                ]
                                            ):

                                                print("piece removed")
                                                # remove piece
                                                self.board[
                                                    int(
                                                        move_2[1][0] - move_2_y_dist / 2
                                                    )
                                                ][
                                                    int(
                                                        move_2[1][1] - move_2_x_dist / 2
                                                    )
                                                ] = 0
                                                self.board[move_2[1][0]][
                                                    move_2[1][1]
                                                ] = 0
                                                valid_push = True

                                            # check if pushed piece is not pushing other piece
                                            elif (
                                                self.board[
                                                    int(
                                                        move_2[1][0] + move_2_y_dist / 2
                                                    )
                                                ][int(move_2[1][1] + move_2_x_dist / 2)]
                                                == 0
                                            ):
                                                # push piece
                                                print("piece removed")
                                                pushed_piece = self.board[move_2[1][0]][
                                                    move_2[1][1]
                                                ]
                                                self.board[move_2[1][0]][
                                                    move_2[1][1]
                                                ] = 0
                                                self.board[
                                                    int(
                                                        move_2[1][0] + move_2_y_dist / 2
                                                    )
                                                ][
                                                    int(
                                                        move_2[1][1] + move_2_x_dist / 2
                                                    )
                                                ] = pushed_piece
                                                valid_push = True

                                    if valid_push == True:
                                        print("valid push")

                                        # move pieces
                                        piece_1 = self.board[move_1[0][0]][move_1[0][1]]
                                        self.board[move_1[0][0]][move_1[0][1]] = 0
                                        self.board[move_1[1][0]][move_1[1][1]] = piece_1

                                        piece_2 = self.board[move_2[0][0]][move_2[0][1]]
                                        self.board[move_2[0][0]][move_2[0][1]] = 0
                                        self.board[move_2[1][0]][move_2[1][1]] = piece_2

                                        if colour == 1:
                                            self.current_turn = 2
                                        else:
                                            self.current_turn = 1

                                        self.turn_no += 1

                                        return

        return "Illegal Move"

    def check_move(self, move_1, move_2, colour):

        # check to see if moving same colour piece both moves and specified colour
        if (
            self.board[move_1[0][0]][move_1[0][1]]
            == self.board[move_2[0][0]][move_2[0][1]]
            and self.board[move_1[0][0]][move_1[0][1]] == colour
        ):
            ###print('check to see if moving same colour piece both moves')
            piece = self.board[move_1[0][0]][move_1[0][1]]  # colour of piece

            # check length of move 1 doesn't exceed 2 squares and is straight/diagonal
            move_1_y_dist = move_1[1][0] - move_1[0][0]
            move_1_x_dist = move_1[1][1] - move_1[0][1]
            sum_moves_1 = abs(move_1_y_dist) + abs(move_1_x_dist)
            if (
                abs(move_1_y_dist) <= 2 and abs(move_1_x_dist) <= 2 and sum_moves_1 != 3
            ):  # and sum_moves_1 != 0:
                ###print("check length of move 1 doesn't exceed 2 squares and is straight/diagonal")

                # check length of move 2 doesn't exceed 2 squares
                move_2_y_dist = move_2[1][0] - move_2[0][0]
                move_2_x_dist = move_2[1][1] - move_2[0][1]
                sum_moves_2 = abs(move_2_y_dist) + abs(move_2_x_dist)
                if (
                    abs(move_2_y_dist) <= 2
                    and abs(move_2_x_dist) <= 2
                    and sum_moves_2 != 3
                ):  # and sum_moves_2 != 0:
                    ###print("check length of move 2 doesn't exceed 2 squares")

                    # check to see if move 1 and move 2 are the same
                    if (
                        move_1_y_dist == move_2_y_dist
                        and move_1_x_dist == move_2_x_dist
                    ):
                        ###print("check to see if move 1 and move 2 are the same")

                        same_board_1 = False  # True if move 1 stays on same board
                        same_board_2 = False  # True if move 2 stays on same board
                        valid_board_1 = False  # True if move 2 is on home board
                        valid_board_2 = (
                            False  # True if move 2 is on opposite colour board
                        )

                        # check to see if move 1 stays on same board and is made on a home board
                        for board_id, desc in self.board_descriptions.items():
                            if all(
                                [
                                    move_1[0][0] >= desc["bounds"][0][0],
                                    move_1[0][0] <= desc["bounds"][0][1],
                                    move_1[0][1] >= desc["bounds"][1][0],
                                    move_1[0][1] <= desc["bounds"][1][1],
                                    move_1[1][0] >= desc["bounds"][0][0],
                                    move_1[1][0] <= desc["bounds"][0][1],
                                    move_1[1][1] >= desc["bounds"][1][0],
                                    move_1[1][1] <= desc["bounds"][1][1],
                                    piece == desc["home_colour"],
                                ]
                            ):

                                board_1 = board_id
                                same_board_1 = True
                                valid_board_1 = True
                                board_colour_1 = desc["board_colour"]
                                break

                        if valid_board_1 == True and same_board_1 == True:

                            # check to see if move 2 stays on same board and is made on a board of the opposite colour
                            for board_id, desc in self.board_descriptions.items():
                                if all(
                                    [
                                        move_2[0][0] >= desc["bounds"][0][0],
                                        move_2[0][0] <= desc["bounds"][0][1],
                                        move_2[0][1] >= desc["bounds"][1][0],
                                        move_2[0][1] <= desc["bounds"][1][1],
                                        move_2[1][0] >= desc["bounds"][0][0],
                                        move_2[1][0] <= desc["bounds"][0][1],
                                        move_2[1][1] >= desc["bounds"][1][0],
                                        move_2[1][1] <= desc["bounds"][1][1],
                                        board_colour_1 != desc["board_colour"],
                                    ]
                                ):

                                    board_2 = board_id
                                    same_board_2 = True
                                    valid_board_2 = True
                                    break

                            ###print(f"same_board_1: {same_board_1} \nvalid_board_1: {valid_board_1} \nsame_board_2: {same_board_2} \nvalid_board_2: {valid_board_2}")

                            if (
                                same_board_1 == True
                                and valid_board_1 == True
                                and same_board_2 == True
                                and valid_board_2 == True
                            ):
                                ###print("check to see if move 1 and move 2 stay on same board and is made on a home board")

                                # check to see if passive move 1 interacts with other stones
                                valid_passive = False

                                # moved one space
                                if abs(move_1_x_dist) == 1 or abs(move_1_y_dist) == 1:
                                    if self.board[move_1[1][0]][move_1[1][1]] == 0:
                                        valid_passive = True

                                # moved two spaces
                                elif abs(move_1_x_dist) == 2 or abs(move_1_y_dist) == 2:
                                    ###print("move 1 length 2")
                                    if (
                                        self.board[
                                            int(move_1[1][0] - move_1_y_dist / 2)
                                        ][int(move_1[1][1] - move_1_x_dist / 2)]
                                        == 0
                                        and self.board[move_1[1][0]][move_1[1][1]] == 0
                                    ):
                                        valid_passive = True

                                if valid_passive == True:
                                    ###print('valid passive')

                                    # check to see if move 2 either pushes no stones or pushes none of its own stones and max 1 stone
                                    valid_push = False

                                    # moved one space
                                    if (
                                        abs(move_2_x_dist) == 1
                                        or abs(move_2_y_dist) == 1
                                    ):
                                        # no push
                                        if self.board[move_2[1][0]][move_2[1][1]] == 0:
                                            valid_push = True

                                        # check if piece interacts with opponent piece
                                        elif (
                                            self.board[move_2[1][0]][move_2[1][1]]
                                            != self.board[move_2[0][0]][move_2[0][1]]
                                        ):

                                            # check if piece pushed off
                                            if any(
                                                [
                                                    move_2[1][0] + move_2_y_dist
                                                    < self.board_descriptions[board_2][
                                                        "bounds"
                                                    ][0][0],
                                                    move_2[1][0] + move_2_y_dist
                                                    > self.board_descriptions[board_2][
                                                        "bounds"
                                                    ][0][1],
                                                    move_2[1][1] + move_2_x_dist
                                                    < self.board_descriptions[board_2][
                                                        "bounds"
                                                    ][1][0],
                                                    move_2[1][1] + move_2_x_dist
                                                    > self.board_descriptions[board_2][
                                                        "bounds"
                                                    ][1][1],
                                                ]
                                            ):

                                                # remove piece
                                                # board[move_2[1][0]][move_2[1][1]] = 0
                                                valid_push = True

                                            # check if pushed piece is not pushing other piece
                                            elif (
                                                self.board[
                                                    move_2[1][0] + move_2_y_dist
                                                ][move_2[1][1] + move_2_x_dist]
                                                == 0
                                            ):
                                                # push piece
                                                # pushed_piece = board[move_2[1][0]][move_2[1][1]]
                                                # board[move_2[1][0]][move_2[1][1]] = 0
                                                # board[move_2[1][0]+move_2_y_dist][move_2[1][1]+move_2_x_dist] = pushed_piece
                                                valid_push = True

                                    # moved two spaces
                                    elif (
                                        abs(move_2_x_dist) == 2
                                        or abs(move_2_y_dist) == 2
                                    ):
                                        # no push
                                        if (
                                            self.board[
                                                int(move_2[1][0] - move_2_y_dist / 2)
                                            ][int(move_2[1][1] - move_2_x_dist / 2)]
                                            == 0
                                            and self.board[move_2[1][0]][move_2[1][1]]
                                            == 0
                                        ):
                                            ###print('no piece in path')
                                            valid_push = True

                                        # check if only one opponents piece is in pieces path
                                        elif any(
                                            [
                                                (
                                                    self.board[
                                                        int(
                                                            move_2[1][0]
                                                            - move_2_y_dist / 2
                                                        )
                                                    ][
                                                        int(
                                                            move_2[1][1]
                                                            - move_2_x_dist / 2
                                                        )
                                                    ]
                                                    == 0
                                                    and self.board[move_2[1][0]][
                                                        move_2[1][1]
                                                    ]
                                                    != self.board[move_2[0][0]][
                                                        move_2[0][1]
                                                    ]
                                                ),
                                                (
                                                    self.board[
                                                        int(
                                                            move_2[1][0]
                                                            - move_2_y_dist / 2
                                                        )
                                                    ][
                                                        int(
                                                            move_2[1][1]
                                                            - move_2_x_dist / 2
                                                        )
                                                    ]
                                                    != self.board[move_2[0][0]][
                                                        move_2[0][1]
                                                    ]
                                                    and self.board[move_2[1][0]][
                                                        move_2[1][1]
                                                    ]
                                                    == 0
                                                ),
                                            ]
                                        ):
                                            ###print('only one piece in path')

                                            # check if piece pushed off
                                            if any(
                                                [
                                                    int(
                                                        move_2[1][0] + move_2_y_dist / 2
                                                    )
                                                    < self.board_descriptions[board_2][
                                                        "bounds"
                                                    ][0][0],
                                                    int(
                                                        move_2[1][0] + move_2_y_dist / 2
                                                    )
                                                    > self.board_descriptions[board_2][
                                                        "bounds"
                                                    ][0][1],
                                                    int(
                                                        move_2[1][1] + move_2_x_dist / 2
                                                    )
                                                    < self.board_descriptions[board_2][
                                                        "bounds"
                                                    ][1][0],
                                                    int(
                                                        move_2[1][1] + move_2_x_dist / 2
                                                    )
                                                    > self.board_descriptions[board_2][
                                                        "bounds"
                                                    ][1][1],
                                                ]
                                            ):

                                                ###print('piece removed')
                                                # remove piece
                                                # board[int(move_2[1][0]-move_2_y_dist/2)][int(move_2[1][1]-move_2_x_dist/2)] = 0
                                                # board[move_2[1][0]][move_2[1][1]] = 0
                                                valid_push = True

                                            # check if pushed piece is not pushing other piece
                                            elif (
                                                self.board[
                                                    int(
                                                        move_2[1][0] + move_2_y_dist / 2
                                                    )
                                                ][int(move_2[1][1] + move_2_x_dist / 2)]
                                                == 0
                                            ):
                                                # push piece
                                                ###print('piece removed')
                                                # pushed_piece = board[move_2[1][0]][move_2[1][1]]
                                                # board[move_2[1][0]][move_2[1][1]] = 0
                                                # board[int(move_2[1][0]+move_2_y_dist/2)][int(move_2[1][1]+move_2_x_dist/2)] = pushed_piece
                                                valid_push = True

                                    if valid_push == True:

                                        return [move_1, move_2]

        return

    def check_possible_moves(self, colour):
        possible_moves = []

        for comb in itertools.product(range(0, 8), repeat=8):
            moves = self.check_move(
                move_1=[[comb[0], comb[1]], [comb[2], comb[3]]],
                move_2=[[comb[4], comb[5]], [comb[6], comb[7]]],
                colour=colour,
            )

            if moves:
                possible_moves.append(moves)

        return possible_moves

    def random_move(self):
        colour = 2  # White
        possible_moves = self.check_possible_moves(colour)

        return possible_moves[rand.randint(0, len(possible_moves) - 1)]

    def check_win(self):
        for desc in self.board_descriptions.values():
            flat_board = []
            for row in range(desc["bounds"][0][0], desc["bounds"][0][1] + 1):
                for column in range(desc["bounds"][1][0], desc["bounds"][1][1] + 1):
                    flat_board.append(self.board[row][column])

            if len(set(flat_board)) != 3:
                self.game_over = True

        return
