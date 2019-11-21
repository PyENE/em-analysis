set border 15 lw 0
set tics out
set xtics nomirror
set title "title - output process 1"

set xtics 0,1
plot [0:4] [0:1] "test11.dat" using 26 title "state 0 observation distribution" with linespoints
set xtics autofreq

pause -1 "<Return>: continue."

set xtics 0,1
plot [0:4] [0:0.42] "test11.dat" using 27 title "state 1 observation distribution" with linespoints
set xtics autofreq

pause -1 "<Return>: continue."

set xtics 0,1
plot [0:4] [0:0.42] "test11.dat" using 28 title "state 2 observation distribution" with linespoints
set xtics autofreq

pause -1 "<Return>: continue."

set xtics 0,1
plot [0:4] [0:0.42] "test11.dat" using 29 title "state 3 observation distribution" with linespoints
set xtics autofreq

pause -1 "<Return>: continue."

set xtics 0,1
plot [0:4] [0:0.42] "test11.dat" using 30 title "state 4 observation distribution" with linespoints
set xtics autofreq

pause -1 "<Return>: continue."

set xtics 0,1
plot [0:4] [0:0.42] "test11.dat" using 31 title "state 5 observation distribution" with linespoints
set xtics autofreq

pause -1 "<Return>: continue."

set xtics 0,1
plot [0:4] [0:0.42] "test11.dat" using 32 title "state 6 observation distribution" with linespoints
set xtics autofreq

pause -1 "<Return>: continue."

set xtics 0,1
plot [0:4] [0:1] "test11.dat" using 33 title "state 7 observation distribution" with linespoints
set xtics autofreq


pause 0 "End."
