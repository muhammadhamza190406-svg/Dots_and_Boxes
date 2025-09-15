import random
import tkinter as tk

#CONSTANTS
GRID_SIZE = 100  # distance between dots
DOT_RADIUS = 5   # size of each dot
MARGIN = 50
CANVAS_WIDTH = 400
CANVAS_HEIGHT = 400
LINE_WIDTH = 2
DEPTH = 2
AI_line_col = "red"
player_line_col = "green"
AI_box_fill_col = "red"
player_box_fill_col = "green"




class gameboard():
    def __init__(self,player,root):
        self.player = player
        self.p_score = 0
        self.AI_score = 0
        self.dots = ['a','b','c','d','e','f','g','h','i']
        self.dots_to_coords = {
        "a": (0, 0),
        "b": (1, 0),
        "c": (2, 0),
        "d": (0, 1),
        "e": (1, 1),
        "f": (2, 1),
        "g": (0, 2),
        "h": (1, 2),
        "i": (2, 2)}
        self.available_moves = [ "ab", "bc", "de", "ef", "gh", "hi","ad", "be", "cf", "dg", "eh", "fi"]
        self.boxes = [
        ["a", "b", "d", "e"],  # top-left
        ["b", "c", "e", "f"],  # top-right
        ["d", "e", "g", "h"],  # bottom-left
        ["e", "f", "h", "i"]   # bottom-right  
        ]
        self.moves_to_boxes = {
        "ab": [0],           # only top-left box
        "ad": [0],           # only top-left
        "de": [0, 2],        # belongs to both top-left & bottom-left
        "be": [0, 1],        # shared between top-left and top-right
        "bc": [1],
        "ef": [1, 3],
        "cf": [1],
        "dg": [2],
        "gh": [2],
        "eh": [2, 3],
        "fi": [3],
        "hi": [3] }
        self.box_counter = [4,4,4,4]
        self.canvas = tk.Canvas(root, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg="white")
        self.turn = ''
        self.draw_board()
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.user_click)

    def first_turn(self):
        toss = random.randint(0,1)
        if toss == 0:
            return 'AI'
        else:
            return self.player
        
    def draw_board(self):

        dots = ['a','b','c','d','e','f','g','h','i']

        for dot in self.dots:
            x, y = self.dots_to_coords[dot]
            x_pix = x * GRID_SIZE + MARGIN
            y_pix = y * GRID_SIZE + MARGIN
            self.canvas.create_oval(
                x_pix - DOT_RADIUS, y_pix - DOT_RADIUS,
                x_pix + DOT_RADIUS, y_pix + DOT_RADIUS,
                fill="black"
            )

    def start_game(self,):
        self.turn = self.first_turn()

        if self.turn == 'AI':
            self.AI_turn()
    
    def next_turn(self, ):
        if self.available_moves == []:
            self.game_over()
        else:
            if self.turn == 'AI':
                self.AI_turn()

    def draw_line(self,move):
        cord1 = self.dots_to_coords[move[0]]
        cord2 = self.dots_to_coords[move[1]]
        x1 = cord1[0] * GRID_SIZE + MARGIN
        y1 = cord1[1] * GRID_SIZE + MARGIN
        x2 = cord2[0] * GRID_SIZE + MARGIN
        y2 = cord2[1] * GRID_SIZE + MARGIN
        if self.turn == 'AI':
            self.canvas.create_line(x1, y1, x2, y2, width=LINE_WIDTH, fill=AI_line_col)
        else:
            self.canvas.create_line(x1, y1, x2, y2, width=LINE_WIDTH, fill=player_line_col)
    
    def draw_box(self,box_index):
        p1 = self.boxes[box_index][0]
        p2 = self.boxes[box_index][3]
        cord1 = self.dots_to_coords[p1]
        cord2 = self.dots_to_coords[p2]
        x1 = cord1[0] * GRID_SIZE + MARGIN
        y1 = cord1[1] * GRID_SIZE + MARGIN
        x2 = cord2[0] * GRID_SIZE + MARGIN
        y2 = cord2[1] * GRID_SIZE + MARGIN

        if self.turn == 'AI':
           self.canvas.create_rectangle(x1, y1, x2, y2, fill=AI_box_fill_col, outline="black", width=LINE_WIDTH)
        else:
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=player_box_fill_col, outline="black", width=LINE_WIDTH)

    def check_boxes(self, move): 
        boxes_formed = []
        for index in self.moves_to_boxes[move]:
            self.box_counter[index] -= 1
            if self.box_counter[index] == 0:
                boxes_formed.append(index)
            
        return boxes_formed
        
    def update_score(self,boxes_formed):
        points = len(boxes_formed)
        if self.turn == 'AI':
           self.AI_score+=points
        else:
            self.p_score+=points
              
    def game_over(self):
        self.canvas.unbind("<Button-1>")
        
        self.canvas.create_rectangle(50, 150, 350, 250, fill="white", outline="black", width=2)
        self.canvas.create_text(200, 180, text="GAME OVER", font=("Arial", 24, "bold"), fill="red")
        
        score_text = f"Player: {self.p_score}   AI: {self.AI_score}"
        self.canvas.create_text(200, 220, text=score_text, font=("Arial", 16))

    def user_click(self, event):
        x, y = event.x, event.y

        for move in self.available_moves:
            d1, d2 = move[0], move[1]
            x1, y1 = self.dots_to_coords[d1]
            x2, y2 = self.dots_to_coords[d2]

            x1 = x1 * GRID_SIZE + MARGIN
            y1 = y1 * GRID_SIZE + MARGIN
            x2 = x2 * GRID_SIZE + MARGIN
            y2 = y2 * GRID_SIZE + MARGIN

            # Midpoint
            mx, my = (x1 + x2) // 2, (y1 + y2) // 2

            # If click is close enough to midpoint → valid move
            if abs(x - mx) < GRID_SIZE // 3 and abs(y - my) < GRID_SIZE // 3:
                self.user_turn(move)
                return
        
    def user_turn(self,move):
        self.canvas.unbind("<Button-1>")
        self.draw_line(move)
        box_list = self.check_boxes(move)

        for index in box_list:
            self.draw_box(index)
        self.update_score(box_list)

        if len(box_list) == 0:
            self.turn = 'AI'
        else:
            self.turn = self.player
        
        if move in self.available_moves:
            self.available_moves.remove(move)
        self.canvas.bind("<Button-1>", self.user_click)
        self.next_turn()
    
    def minimax_check_boxes(self,box_list, move): #FOR MINIMAX FUNCTION MAKE A COPY OF THE BOX_COUNTER BEFORE PASSING IT IN
        boxes_formed = []
        boxes = self.moves_to_boxes[move] 
        for index in boxes:
            box_list[index] -= 1
            if box_list[index] == 0:
                boxes_formed.append(index)
            
        return boxes_formed
    
    def minimax_update_score(self,boxes_formed,score,AI):
        points = len(boxes_formed)
        if AI:
            return(score+points)
        else:
            return(score-points)
        
    def minimax(self,moves_left,box_list,depth,alpha,beta,score,AI):

        if (moves_left == []) or (depth == 0):
            return score
        
        if AI == True:
            max_score = -float('inf')
            for move in moves_left:
                new_moves = moves_left.copy()
                new_box_list = box_list.copy()

                boxes_formed = self.minimax_check_boxes(new_box_list,move)
                new_score = self.minimax_update_score(boxes_formed,score,AI)
                new_moves.remove(move)

                if len(boxes_formed) > 0:
                    future_score = self.minimax(new_moves,new_box_list,depth-1,alpha,beta,new_score,AI)
                else:
                    future_score = self.minimax(new_moves,new_box_list,depth-1,alpha,beta,new_score,not(AI))

                max_score = max(max_score,future_score)
                alpha = max(alpha,max_score)
                if beta <= alpha:
                    break
            return max_score
        
        else:
            min_score = float('inf')
            for move in moves_left:
                new_moves = moves_left.copy()
                new_box_list = box_list.copy()

                boxes_formed = self.minimax_check_boxes(new_box_list,move)
                new_score = self.minimax_update_score(boxes_formed,score,AI)
                new_moves.remove(move)

                if len(boxes_formed) > 0:
                    future_score = self.minimax(new_moves,new_box_list,depth-1,alpha,beta,new_score,AI)
                else:
                    future_score = self.minimax(new_moves,new_box_list,depth-1,alpha,beta,new_score,not(AI))


                min_score = min(min_score,future_score)
                beta = min(beta,min_score)
                if beta <= alpha:
                    break
            return min_score
        
    def best_AI_move(self):
        best_score = -float('inf')
        best_move = ''
        for move in self.available_moves:
            moves_left = self.available_moves.copy()
            box_list = self.box_counter.copy()

            boxes_formed = self.minimax_check_boxes(box_list,move)
            new_score = self.minimax_update_score(boxes_formed,0,True)
            moves_left.remove(move)

            if len(boxes_formed) > 0:
                new_score = self.minimax(moves_left,box_list,DEPTH-1,-float('inf'),float('inf'),new_score,True)
            else:
                new_score = self.minimax(moves_left,box_list,DEPTH-1,-float('inf'),float('inf'),new_score,False)

            if new_score > best_score:
                best_score = new_score
                best_move = move

        print('Move Chosen by AI:',best_move)   
        return best_move
    
    def AI_turn(self):
        self.canvas.unbind("<Button-1>")
        move = self.best_AI_move()
        self.draw_line(move)
        box_list = self.check_boxes(move)

        for index in box_list:
            self.draw_box(index)
        self.update_score(box_list)

        if len(box_list) == 0:
            self.turn = self.player
        else:
            self.turn = "AI"
        
        if move in self.available_moves:
            self.available_moves.remove(move)
        self.canvas.bind("<Button-1>", self.user_click)
        self.next_turn()

root = tk.Tk()
root.title("Dots and Boxes")
game = gameboard('Hamza',root)
game.start_game()
root.mainloop()








        








    
        