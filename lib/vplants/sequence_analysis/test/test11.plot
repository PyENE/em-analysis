set border 15 lw 0
set tics out
set xtics nomirror
set title "title - smoothed observed probabilities"

plot [0:29] [0:1] "test10.dat" using 4 title "observed value 0" with linespoints,\
"test10.dat" using 5 title "observed value 1" with linespoints,\
"test10.dat" using 6 title "observed value 2" with linespoints

pause -1 "<Return>: continue."

set title "title"

plot [0:29] [0:1] "test10.dat" using 1 title "observed value 0" with linespoints,\
"test10.dat" using 2 title "observed value 1" with linespoints,\
"test10.dat" using 3 title "observed value 2" with linespoints

pause -1 "<Return>: continue."

set ytics 0,1
plot [0:30] [0:2] "test11.dat" using 1 title "sequence length frequency distribution" with impulses
set ytics autofreq

pause 0 "End."
