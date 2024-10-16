import pygame

class Piece:
    def __init__(self, pos, color, board, does_stand):
        self.pos = pos
        self.x = pos[0]
        self.y = pos[1]
        self.color = color
        self.standing = does_stand
        self.valid = []
        img_path = 'data/imgs/' + color + '_standing.png' if self.standing else 'data/imgs/' + color + '_laying.png'
        self.img = pygame.image.load(img_path)
        self.img = pygame.transform.scale(self.img, (board.square_width - 20, board.square_height - 20))
        self.stack_piece_index = None 

    
    def update_pos(self, new_pos):
            self.pos = new_pos
            self.x = new_pos[0]
            self.y = new_pos[1]

    def move(self, new_square, board):
        """
        Moves piece to new square. Move depends on whether we try to move stack or piece. Returns True if succesful
        """

        current_square = board.get_square_from_coord(self.pos)
        if new_square in self.valid:
            
            #We are moving a stack
            if len(current_square.pieces) > 1:
                self.move_stack(new_square, current_square, board)
            #we are moving a piece  
            else:
                new_square.pieces.extend(current_square.pieces)
                new_square.occupying_piece = self
                self.update_pos(new_square.pos)
                current_square.pieces = []
                current_square.occupying_piece = None  # Clear the starting square

            #Reset valid move highlight for all squares.
            for square in board.squares:
              square.highlight = False
            self.valid = []
            return True  # Indicate the move was successful
        else:
            print("Nånting med move stack är fel")
            return False


    def move_stack(self, new_square , current_square, board):
        """
        Function for moving a stack, takes the current square that hlds the stack, 
        the new square it wants to move the stack to and the play board as arguement 
        """
        #First move we split the stack based on which piece in the stack that the player want to move
        stack = current_square.pieces[self.stack_piece_index:]
        current_square.pieces = current_square.pieces[:self.stack_piece_index]
        if(current_square.pieces):
            current_square.occupying_piece = current_square.pieces[-1]
        else: 
            current_square.occupying_piece = None

        #For every square between new and current square we drop the bottom piece and updates its position
        for passed_square in current_square.all_squares_between(new_square, board):
            bottom_piece = stack[0]
            bottom_piece.update_pos(passed_square.pos)
            passed_square.occupying_piece = bottom_piece
            passed_square.pieces.append(bottom_piece)
            print("moved stack to square: ", passed_square.pos)
            stack.pop(0)
        
        #at new square we update all remaining pieces location and append to new squares pieces.
        if(stack):
            for new_piece in stack:
                new_piece.update_pos(new_square.pos)
            new_square.pieces.extend(stack)
            new_square.occupying_piece = stack[-1]
        self.stack_piece_index = None 



    def valid_move(self,board):
        """
        looks for and highlight all valid moves for a stack or piece.
        """
        valid = []
        if self is None or self.standing:
            print('invalid move in valid move')
            return None
        selected_square = board.get_square_from_coord(self.pos)
        is_stack = len(selected_square.pieces) > 1
        highest_amount_of_steps = 1
        neighbours = selected_square.neighbours()

        #Stacks can move further than pieces and therefore have other initial values
        if(is_stack):
            neighbours = selected_square.stack_neighbours()
            stack = selected_square.pieces[self.stack_piece_index:]
            highest_amount_of_steps = 0
            for piece in stack:
                if piece.color == board.color:
                    highest_amount_of_steps += 1
                else: 
                    break

        #The two arrays tracks how many steps left each direction has as well as if a piece/stack can go futher in one direction
        invalid_move_direction = []
        directions_steps_left = [highest_amount_of_steps,highest_amount_of_steps,highest_amount_of_steps,highest_amount_of_steps]


        for neighbour in neighbours:
                    pos, move_direction = neighbour
                    x,y = pos
                    for square in board.squares:
                        if square.x == x and square.y == y and move_direction not in invalid_move_direction and directions_steps_left[move_direction] > 0:
                            if square.valid_square():
                                valid.append(square)
                                square.highlight = True
                                directions_steps_left[move_direction] -= 1
                            else:
                                #if square isn't valid we can no longer move in that direction
                                invalid_move_direction.append(move_direction)
        self.valid = valid

        

    
    #moves the piece based on previous function
    #def move(self, pos):

    #returns whether the piece is standing or not
    def is_standing(self):
        return self.standing
