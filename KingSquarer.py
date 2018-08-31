'''
Creates the heatmaps for the parsed pgn files
<<<CURENTLY UNFINISHED>>>
'''

def create_dataframe():
    check_df = pd.DataFrame(SQUARE_NAMES,columns=['king_square_name'])
    check_df.index = check_df['king_square_name']
    check_df['frequency'] = 0

    stale_df = pd.DataFrame(SQUARE_NAMES,columns=['king_square_name'])
    stale_df.index = stale_df['king_square_name']
    stale_df['frequency'] = 0
    
    return check_df

def populate_dataframe(csv_paths, dataframe):
    '''Takes the parsed pgn csv/txt files and sorts them into their equivalent spaces in a len=64 dataframe'''
    
    for path in csv_paths:
        with open(path,'r') as file: 
            for line in file:
                result,king,queen = line.split(',')

                if result == '1' or result == '0': # if checkmate
                    king_square = square_name(int(king))                
                    dataframe.at[king_square,'frequency'] += 1 

                else: # if stalemate
                    pass # this takes 6-10x longer
        #             king_square_white,king_square_black = [square_name(int(king)) for king in king.split('-')]
        #             stale_df.at[king_square_white,'frequency'] += 1 
        #             stale_df.at[king_square_black,'frequency'] += 1 
        
    return dataframe

if __name__ == '__main__':
    for path in paths: 
        check_df = create_dataframe()
        check_df = populate_dataframe(csv_paths=paths, dataframe=check_df)
        heatmap = create_heatmap(dataframe=check_df)
