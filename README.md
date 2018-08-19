# ChessViz
How to visualize 400 million games of chess (PGN text files) using Python and a (moderately) powered laptop.

Goals: 
1) Download PGN files from: https://database.lichess.org/
2) Split those PGN files into individual PGNs, each representing 1x game of chess
3) Use python-chess library to interesting data about the final board piece positions
4) Save this data to a .csv
5) Use some kind of multi-processing to speed everything up (total file size = ~400GB)
6) Create pivot table > heatmap using pandas and seaborn
