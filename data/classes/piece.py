import pygame

class Piece:
    def __init__(self, pos, color, board, does_stand):
        self.pos = pos
        self.x = pos[0]
        self.y = pos[1]
        self.color = color
        self.standing = does_stand
        img_path = 'data/imgs/' + color + '_standing.png' if self.standing else 'data/imgs/' + color + '_laying.png'
        self.img = pygame.image.load(img_path)
        self.img = pygame.transform.scale(self.img, (board.square_width - 20, board.square_height - 20))




    def move(self, square, board):
        # Check if the move is valid
        prev_square = board.get_square_from_coord(self.pos)

        if square in self.valid:
            # Move the piece
            # if len(prev_square.pieces) > 1:
            #     prev_square.move_stack(square)
            
            if len(prev_square.pieces) > 1:
                prev_square_stack = prev_square.pieces
                prev_square.pieces = [prev_square_stack.pop(0)]
                prev_square.occupying_piece = prev_square.pieces[-1] 
                for passed_square in prev_square.all_squares_between(square, board):
                    print("hi")
                    bottom_piece = prev_square_stack[0]
                    bottom_piece.pos = passed_square.pos
                    bottom_piece.x = passed_square.x
                    bottom_piece.y = passed_square.y
                    passed_square.occupying_piece = bottom_piece
                    passed_square.pieces.append(bottom_piece)
                    prev_square_stack.pop(0)
                if(prev_square_stack):
                    for new_piece in prev_square_stack:
                        new_piece.x = square.x
                        new_piece.y = square.y
                        new_piece.pos = square.pos
                    square.pieces.extend(prev_square_stack)
                    square.occupying_piece = prev_square_stack[-1]
                
            else:
                square.pieces.extend(prev_square.pieces)
                square.occupying_piece = self
                self.pos = square.pos
                self.x = square.x
                self.y = square.y
                prev_square.pieces = []
                prev_square.occupying_piece = None  # Clear the starting square

            
            
            for squares in board.squares:
              squares.highlight = False
            self.valid = []
            return True  # Indicate the move was successful
        else:
            print("Invalid move")
            return False
        
    def valid_move(self,board):
        valid = []
        if self is None or self.standing:
            print('invalid move in valid move')
            return None
        selected_square = board.get_square_from_coord(self.pos)
        is_stack = len(selected_square.pieces) > 1
        neighbours = selected_square.stack_neighbours() if is_stack else selected_square.neighbours()
        invalid_move_direction = []
        highest_amount_of_steps = 0

        for piece in selected_square.pieces:
            if piece.color == board.color:
                highest_amount_of_steps += 1
            else: 
                break
        if(len(selected_square.pieces) == highest_amount_of_steps and is_stack):
            highest_amount_of_steps -= 1
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
                                invalid_move_direction.append(move_direction)
        self.valid = valid

        

    
    #moves the piece based on previous function
    #def move(self, pos):

    #returns whether the piece is standing or not
    def is_standing(self):
        return self.standing
