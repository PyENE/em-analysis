set border 15 lw 0
set tics out
set xtics nomirror
set title "title"

plot [0:24] [0:4] "test01.dat" using 18 title "number of runs of state 0 per sequence frequency distribution" with impulses,\
"test01.dat" using 43 title "mixture of number of runs of state 0 per sequence distribution" with linespoints

pause -1 "<Return>: continue."

plot [0:92] [0:3] "test01.dat" using 19 title "number of occurrences of state 0 per sequence frequency distribution" with impulses,\
"test01.dat" using 44 title "mixture of number of occurrences of state 0 per sequence distribution" with linespoints

pause -1 "<Return>: continue."

plot [0:19] [0:6] "test01.dat" using 20 title "number of runs of state 1 per sequence frequency distribution" with impulses,\
"test01.dat" using 45 title "mixture of number of runs of state 1 per sequence distribution" with linespoints

pause -1 "<Return>: continue."

plot [0:41] [0:3] "test01.dat" using 21 title "number of occurrences of state 1 per sequence frequency distribution" with impulses,\
"test01.dat" using 46 title "mixture of number of occurrences of state 1 per sequence distribution" with linespoints

pause -1 "<Return>: continue."

plot [0:17] [0:9] "test01.dat" using 22 title "number of runs of state 2 per sequence frequency distribution" with impulses,\
"test01.dat" using 47 title "mixture of number of runs of state 2 per sequence distribution" with linespoints

pause -1 "<Return>: continue."

plot [0:29] [0:5] "test01.dat" using 23 title "number of occurrences of state 2 per sequence frequency distribution" with impulses,\
"test01.dat" using 48 title "mixture of number of occurrences of state 2 per sequence distribution" with linespoints

pause -1 "<Return>: continue."

plot [0:17] [0:7] "test01.dat" using 24 title "number of runs of state 3 per sequence frequency distribution" with impulses,\
"test01.dat" using 49 title "mixture of number of runs of state 3 per sequence distribution" with linespoints

pause -1 "<Return>: continue."

plot [0:31] [0:5] "test01.dat" using 25 title "number of occurrences of state 3 per sequence frequency distribution" with impulses,\
"test01.dat" using 50 title "mixture of number of occurrences of state 3 per sequence distribution" with linespoints

pause -1 "<Return>: continue."

plot [0:15] [0:5] "test01.dat" using 26 title "number of runs of state 4 per sequence frequency distribution" with impulses,\
"test01.dat" using 51 title "mixture of number of runs of state 4 per sequence distribution" with linespoints

pause -1 "<Return>: continue."

plot [0:75] [0:5] "test01.dat" using 27 title "number of occurrences of state 4 per sequence frequency distribution" with impulses,\
"test01.dat" using 52 title "mixture of number of occurrences of state 4 per sequence distribution" with linespoints

pause -1 "<Return>: continue."

set ytics 0,1
plot [0:97] [0:3] "test01.dat" using 1 title "sequence length frequency distribution" with impulses
set ytics autofreq

pause 0 "End."
