set border 15 lw 0
set tics out
set xtics nomirror
set title "title - smoothed observed probabilities"

plot [0:90] [0:1] "test00.dat" using 11 title "observed state 0" with linespoints,\
"test00.dat" using 1 title "theoretical state 0" with linespoints,\
"test00.dat" using 12 title "observed state 1" with linespoints,\
"test00.dat" using 2 title "theoretical state 1" with linespoints,\
"test00.dat" using 13 title "observed state 2" with linespoints,\
"test00.dat" using 3 title "theoretical state 2" with linespoints,\
"test00.dat" using 14 title "observed state 3" with linespoints,\
"test00.dat" using 4 title "theoretical state 3" with linespoints,\
"test00.dat" using 15 title "observed state 4" with linespoints,\
"test00.dat" using 5 title "theoretical state 4" with linespoints

pause -1 "<Return>: continue."

set title "title"

plot [0:90] [0:1] "test00.dat" using 6 title "observed state 0" with linespoints,\
"test00.dat" using 1 title "theoretical state 0" with linespoints,\
"test00.dat" using 7 title "observed state 1" with linespoints,\
"test00.dat" using 2 title "theoretical state 1" with linespoints,\
"test00.dat" using 8 title "observed state 2" with linespoints,\
"test00.dat" using 3 title "theoretical state 2" with linespoints,\
"test00.dat" using 9 title "observed state 3" with linespoints,\
"test00.dat" using 4 title "theoretical state 3" with linespoints,\
"test00.dat" using 10 title "observed state 4" with linespoints,\
"test00.dat" using 5 title "theoretical state 4" with linespoints

pause -1 "<Return>: continue."

set ytics 0,1
plot [0:97] [0:3] "test01.dat" using 1 title "sequence length frequency distribution" with impulses
set ytics autofreq

pause 0 "End."
