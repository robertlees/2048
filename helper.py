import numpy as np
import tkinter as tk

# colors used for gui
colors = {
        "CANVAS_COLOR":"#faf8f0",
        "GRID_COLOR":"#9c8a7a",
        "EMPTY_CELL_COLOR":"#bdac97",
        "SCORE_BOARD_COLOR":"#eae7d9",
        "SCORE_NUMBER_COLOR":"#a19383",
        "SCORE_LABEL_FONT":("Verdana", 20),
        "SCORE_FONT":("Helvetica", 32, "bold"),
        "GAME_OVER_FONT":("Helvetica", 48, "bold"),
        "GAME_OVER_FONT_COLOR":"#ffffff",
        "GAME_OVER_BOARD_COLOR":"black",
        "WINNER_BG":"#ffcc00",
        "LOSER_BG":"#a39489",
        "CELL_COLORS":{
            2: "#fcefe6",
            4: "#f2e8cb",
            8: "#f5b682",
            16: "#f29446",
            32: "#ff775c",
            64: "#e64c2e",
            128: "#ede291",
            256: "#fce130",
            512: "#ffdb4a",
            1024: "#f0b922",
            2048: "#fad74d"
        },
        "CELL_NUMBER_COLORS":{
            2: "#695c57",
            4: "#695c57",
            8: "#ffffff",
            16: "#ffffff",
            32: "#ffffff",
            64: "#ffffff",
            128: "#ffffff",
            256: "#ffffff",
            512: "#ffffff",
            1024: "#ffffff",
            2048: "#ffffff"
        },
        "CELL_NUMBER_FONTS":{
            2: ("Helvetica", 55, "bold"),
            4: ("Helvetica", 55, "bold"),
            8: ("Helvetica", 55, "bold"),
            16: ("Helvetica", 50, "bold"),
            32: ("Helvetica", 50, "bold"),
            64: ("Helvetica", 50, "bold"),
            128: ("Helvetica", 45, "bold"),
            256: ("Helvetica", 45, "bold"),
            512: ("Helvetica", 45, "bold"),
            1024: ("Helvetica", 40, "bold"),
            2048: ("Helvetica", 40, "bold")
        }
}


class Game():

    def __init__(self,m,n):
        """

        Args:
            m (int): rows of board
            n (int): cols of board
        """
        self.state = np.zeros((m,n), int)
        self.score = 0
        
        idx = np.argwhere(self.state == 0)
        residx = idx[np.random.randint(len(idx))]
        self.state[tuple(residx)] = 2

        idx = np.argwhere(self.state == 0)
        residx = idx[np.random.randint(len(idx))]
        self.state[tuple(residx)] = 2
        
    def move_nums_to_left(self):
        """moving squares and merging, O(n) time complexity, and O(1) space complexity

        """
        m = len(self.state)
        n = len(self.state[0])
        # track if any move was made
        flag = False
        # move number to the left
        for row in self.state:
            # track empty spot
            p1 = 1
            # tarck number traverse
            p2 = 1
            # track mergerged cell, cannot merge twice
            p3 = 0
            
            while p2 < n and p1 < n:
                if row[p2] == 0:
                    p2 += 1
                    continue
                if row[p1 - 1] != 0:
                    if row[p1-1] == row[p2] and p3 <= p1 - 1:
                        row[p1 - 1] = row[p2] * 2
                        self.score += row[p1 - 1]
                        flag = True
                        row[p2] = 0
                        p2 += 1
                        p3 = p1
                    else:
                        p1 += 1
                        if p2 < p1:
                            p2 = p1
                else:
                    row[p1 - 1], row[p2] = row[p2], 0
                    flag = True
                    # p1 += 1
                    p2 += 1
                    
        # generate random new number
        idx = np.argwhere(self.state == 0)
        if len(idx) > 0 and flag:
            residx = idx[np.random.randint(len(idx))]
            self.state[tuple(residx)] = 2
        return flag
    
    def update_game_state(self):
        """check game state

        Args:

        Returns:
            int: if player can still make steps or game is over
        """
        m = len(self.state)
        n = len(self.state[0])
        state_test = np.pad(self.state, 1, mode='constant', constant_values=-1)
        if 1024 in state_test:
            return 1
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if state_test[i+1][j] == 0 or state_test[i+1][j] == state_test[i][j]:
                    return 0
                if state_test[i-1][j] == 0 or state_test[i-1][j] == state_test[i][j]:
                    return 0
                if state_test[i][j+1] == 0 or state_test[i][j+1] == state_test[i][j]:
                    return 0
                if state_test[i][j-1] == 0 or state_test[i][j-1] == state_test[i][j]:
                    return 0
        return -1
    
    def move(self, direction):
        """move squares based on input

        Args:
            direction (str): input direction

        Raises:
            ValueError: when have illegal description
        Returns:
            bool: if player actually make a move
        """
        direction = direction.lower()
        if direction == "w":
            self.state = self.state.T
            flag = self.move_nums_to_left()
            self.state = self.state.T
        elif direction == "a":
            flag = self.move_nums_to_left()
        elif direction == "s":
            self.state = np.flipud(self.state).T
            flag = self.move_nums_to_left()
            self.state = np.flipud(self.state.T)
        elif direction == "d":
            self.state = np.flip(self.state)
            flag = self.move_nums_to_left()
            self.state = np.flip(self.state)
        else:
            raise ValueError(f"Invalid input: {direction}. \n Supported Input: W, A, S, D")
        return flag
    
    def get_board(self):
        return self.state
    
    def get_score(self):
        return self.score

class GUI():
    def __init__(self, m, n):
        self.m = m
        self.n = n
        self.game = Game(m,n)
        self.board = [[None] * self.n for _ in range(m)]
        self.lscore = None
        self.root = tk.Frame(bg=colors["CANVAS_COLOR"])
        self.root.grid()
        self.root.master.title("2048")
        self.main_frame = tk.Frame(self.root, bg=colors["GRID_COLOR"], bd=3, width=800, height=800)
        # greeting = tk.Label(text="Hello, Tkinter")
        self.main_frame.grid(
            pady=(120, 150), 
            padx=(80,80)
        )

        self.show_board()
        self.show_score()
        self.result = None
        self.show_button()
        self.render_gui()

        self.root.master.bind("<w>", self.game_move)
        self.root.master.bind("<s>", self.game_move)
        self.root.master.bind("<a>", self.game_move)
        self.root.master.bind("<d>", self.game_move)

        self.root.mainloop()

    def show_board(self):
        """show board
        """
        
        for i in range(self.m):
            for j in range(self.n):
                num_frame = tk.Frame(
                    self.main_frame,
                    bg=colors["EMPTY_CELL_COLOR"],
                    width=150,
                    height=150
                )
                num_frame.grid(
                    row=i,
                    column=j,
                    padx=5,
                    pady=5
                )
                lnum = tk.Label(self.main_frame,bg=colors["EMPTY_CELL_COLOR"])
                lnum.grid(
                    row=i,
                    column=j
                )
                self.board[i][j] = [num_frame, lnum]
                
        
    def show_score(self):
        """show score
        """
        score = tk.Frame(
            self.root,
            bg=colors["SCORE_BOARD_COLOR"],
            width=80,
            height=60
        )
        score.place(anchor="center", relx=0.5, rely=0.06)
        tk.Label(
            score,
            text="SCORE",
            font=colors["SCORE_LABEL_FONT"],
            bg=colors["SCORE_BOARD_COLOR"],
            fg=colors["SCORE_NUMBER_COLOR"]
        ).grid(row=0)
        self.lscore = tk.Label(
            score,
            text="0",
            font=colors["SCORE_FONT"],
            fg=colors["SCORE_NUMBER_COLOR"],
            bg=colors["SCORE_BOARD_COLOR"]
        )
        self.lscore.grid(row=1)
    
    def restart(self):
        """restart game
        """
        self.game = Game(self.m,self.n)
        if self.result:
            self.result.destroy()
            self.result = None
        self.render_gui()


    def show_button(self):
        """reset button used to restart game
        """
        button = tk.Button(
            self.root, 
            text='RESET', 
            width=50, 
            command=self.restart,
            font=colors["SCORE_LABEL_FONT"],
            fg=colors["GAME_OVER_FONT_COLOR"],
            bg=colors["GRID_COLOR"])
        button.place(anchor="center", relx=0.5, rely=0.9, width=200)
        # button.pack()

    
    def show_result(self, txt):
        """show game result

        Args:
            txt (str): result message
        """
        self.result = tk.Frame(
            self.root,
            bg=colors["SCORE_BOARD_COLOR"],
            width=100,
            height=100
        )
        self.result.place(anchor="center", relx=0.5, rely=0.5)
        tk.Label(
            self.result,
            text=txt,
            font=colors["GAME_OVER_FONT"],
            bg=colors["GAME_OVER_BOARD_COLOR"],
            fg=colors["GAME_OVER_FONT_COLOR"]
        ).grid(row=0)
    
    def render_gui(self):
        """render gui based on game states
        """
        state = self.game.get_board()
        # print(state)
        for i in range(self.m):
            for j in range(self.n):
                cval = state[i][j]
                if cval != 0:
                    self.board[i][j][0].configure(
                        bg=colors["CELL_COLORS"][cval]
                    )
                    self.board[i][j][1].configure(
                        fg=colors["CELL_NUMBER_COLORS"][cval],
                        font=colors["CELL_NUMBER_FONTS"][cval],
                        bg=colors["CELL_COLORS"][cval],
                        text=str(cval)
                    )
                else:
                    self.board[i][j][0].configure(
                        bg=colors["EMPTY_CELL_COLOR"]
                    )
                    self.board[i][j][1].configure(
                        text="",
                        bg=colors["EMPTY_CELL_COLOR"]

                    )

        self.lscore.config(
            text = str(self.game.get_score())
        )
        if self.game.update_game_state() == 1:
            self.show_result("Congrats! You WIN!!")
        elif self.game.update_game_state() == -1:
            self.show_result("GAME OVER")
            
        self.root.update_idletasks()
    
    def game_move(self, event):
        """event handler for game control

        Args:
            event (event): user input
        """
        try:
            self.game.move(event.keysym)
            self.render_gui()
        except Exception as e:
            print(e)
            self.render_gui()