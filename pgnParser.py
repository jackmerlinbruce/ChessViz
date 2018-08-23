import os
import sys
import chess.pgn as pychess
from chess.pgn import read_game
from chess import square_name
from chess import SQUARE_NAMES, BB_SQUARES
import ChessFuncs
from ChessFuncs import end_board
import bz2
import time
from io import StringIO
from multiprocessing import Process
import time
from time import sleep
import time

#Create list of PGN files
pgns = [file for file in os.listdir() if "lichess" in file]
out_path = "test-results.txt"
out_paths = ["PARSED_"+pgn for pgn in pgns]

#the thing which will run simultaneously
def main(pgn_file, out_path):
    '''
    Takes in one long/concatenated PGN file and spits out the end king squares to an output file.
    '''
    
    def end_board(parsed_pgn_file):
        '''Moves the py-chess board obj to the final move.'''
        current_board = parsed_pgn_file.board()
        for move in parsed_pgn_file.main_line():
            current_board.push(move)    
        return current_board
    
    def does_q_checkmate_k(board, winner, loser):
        #obv, only accounts for when a queen is DIRECTLY attacking a checkmated king,
        #not accounting for the lines of attack which PREVENT the king from moving
        try:
            #uses .attackers() to find which squares are attacking out checkmated king?
            board_string = str(board.attackers(winner, board.king(loser))).replace(" ","")[::-1] #removes whitespace and reverses str
            board_string = board_string.split("\n") #split in ranks (horizontally)
            board_string = [b[::-1] for b in board_string] #reverse each rank because h8 is the final sq
            board_string = "".join(board_string) #rejoin list
            board_string = list(enumerate(board_string)) #enumerate list as this is the way squares are counted (but in reverse)

            #is a queen on one of those squares?
            queen_num = board.queen(winner)
            does_q_checkmate_k = board_string[queen_num][1] is not '.' #is there a piece at the index which the queen is in
            return does_q_checkmate_k
        except:
            return False
    
    with open(pgn_file) as bigfile:
        pgn = []
        then = time.time()
        for line in bigfile:
            
            #Every 20 minutes, sleep for 2 minutes
            elapsed = time.time() - then
            if elapsed > 1200:
                print("Sleeping for 2 minutes")
                sleep(120)
                then = time.time()
        
            if line.startswith("[Event"):
                pgn.append(line)
            elif line.startswith("1. "):
                pgn.append(line)
                pgn = "".join(pgn)
                pgn = StringIO(pgn)
                pgn = read_game(pgn)
                result = pgn.headers["Result"]
                board = end_board(pgn)
                 
                if result in ["1-0","0-1"] and board.is_checkmate():
                    if result == "1-0":
                        winner = 1 # WHITE wins
                        loser = 0
                        king_num = board.king(loser) # BLACK loses
                        queen_num = 99
                    if result == "0-1":
                        winner = 0 # BLACK wins
                        loser = 1
                        king_num = board.king(loser) # WHITE loses
                        queen_num = 99
                    if does_q_checkmate_k(board,winner,loser):
                        queen_num = board.queen(winner)
                    with open(out_path, "a") as results:
                        results.write("%i,%i,%i\n" % (winner,king_num,queen_num))     
                else:
                    winner = 2 # DRAW
                    with open(out_path, "a") as results:
                        results.write("%i,%i-%i,\n" % (winner,board.king(1),board.king(0)))
                        
                pgn = []
                
            else:
                pgn.append(line)
                
def multi_parse(pgn_file_list, out_path):
    #TO DO:
        #stagger multiprocess by number of cores
        #e.g. 8 files with 2 cores runs 4 times
        #e.g. 8 files with 4 cores runs 2 times
    '''
    Takes in a list of long/concatenated pgn files.
    Passes each file into a multiprocessing unit for the main_parse() function.
    Read multiples pgn files at once and write to same output file.
    
    Basically a for-looped version of this:    
        def multi():
            start = time.time()
            p1 = Process(target=main, args=(pgn1,))
            p2 = Process(target=main, args=(pgn2,))
            p3 = Process(target=main, args=(pgn3,))
            p4 = Process(target=main, args=(pgn4,))
            p1.start()
            p2.start()
            p3.start()
            p4.start()
            p1.join()
            p2.join()
            p3.join()
            p4.join()
            processtime = time.time() - start
            return processtime
    
    '''
    start = time.time()
    
    process_list = []
    for i,pgn_file in enumerate(pgn_file_list):
        process = Process(target=main, args=(pgn_file,out_paths[i]))
        process_list.append(process)
    for process in process_list:
        process.start()
    for p in process_list:
        process.join()

    processtime = time.time() - start
    print("MultiParser took %i seconds to run" % round(processtime,2))
    return processtime

if __name__ == "__main__":
    multi_parse(pgns, out_path)