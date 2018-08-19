def get_loser(parsed_pgn_file):
    
    result = parsed_pgn_file.headers["Result"]
    
    white_win = '1-0'
    black_win = '0-1'
    
    loser = None
    if result == white_win:
        loser =  0 # is BLACK
    if result == black_win:
        loser =  1 # is WHITE
    
    return loser

def get_check_mate_pos(parsed_pgn_file, loser):
    '''
    takes in a py-chess board obj, and a black (0) or white (1) loser, spits out check_mate_pos as a number
    '''
    check_mate_pos = parsed_pgn_file.board().king(loser)
    return check_mate_pos

def get_check_mate_pos_2(parsed_pgn_file, loser):
    '''
    takes in a py-chess board obj, and a black (0) or white (1) loser, spits out check_mate_pos as a number
    '''
    
    current_board = parsed_pgn_file.board()
    for move in parsed_pgn_file.main_line():
        current_board.push(move)    
    
    check_mate_pos = current_board.king(loser)
    return check_mate_pos
    
def get_check_mate_pos_3(parsed_pgn_file):
    '''
    takes in a pgn py-chess obj
    finds who lost the match
    returns the final king square (as a number) of the loser
    (NOTE: doesn't check for checkmate - do separately)
    '''
    result = parsed_pgn_file.headers["Result"]
    white_win = '1-0'
    black_win = '0-1'
    draw = '1/2-1/2'
    loser = ''
    if result == white_win:
        loser = 0 # is BLACK
    if result == black_win:
        loser = 1 # is WHITE
    if result == draw:
        loser = 0 # is TEMP placeholder
    
    current_board = parsed_pgn_file.board()
    for move in parsed_pgn_file.main_line(): 
        current_board.push(move) # get to final stage of match
        
    check_mate_pos = current_board.king(loser)
    return check_mate_pos        
        
def end_board(parsed_pgn_file):
    current_board = parsed_pgn_file.board()
    for move in parsed_pgn_file.main_line():
        current_board.push(move)    
    
    return current_board
   
def split_pgn(pgn_file):
    '''
    takes a long pgn_file pathname (".txt") and cuts the file every 18 lines
    '''
    
    lines_per_file = 18
    smallfile = None

    with open(pgn_file) as bigfile:
        for lineno, line in enumerate(bigfile):
            if lineno % lines_per_file == 0:
                if smallfile:
                    smallfile.close()
                small_filename = 'small_file_{}.txt'.format( int((lineno + lines_per_file)/lines_per_file) )
                smallfile = open(small_filename, "w")
            smallfile.write(line)
        if smallfile:
            smallfile.close()
            
def split_pgn_2(pgn_file):
    '''
    takes a long pgn_file pathname (".txt") and cuts the file at "[Event"
    '''
    
    lines_per_file = 18
    smallfile = None
            
    with open(pgn_file) as bigfile:
        for lineno, line in enumerate(bigfile):
            if line.startswith("[Event"): #cuts file at this type of line
                if smallfile:
                    smallfile.close()
                small_filename = PGN_DIR+'small_file_{}.txt'.format( int((lineno + lines_per_file)/lines_per_file) )
                smallfile = open(small_filename, "w")
            smallfile.write(line)
        if smallfile:
            smallfile.close()
            
def remove_pgns(directory, file_name_identifier):
    for file in os.listdir(directory):
        if file_name_identifier in file:
            os.remove(directory+f)
            
if __name__ == "__main__":
    print("\nHere are some chess functions.\n")