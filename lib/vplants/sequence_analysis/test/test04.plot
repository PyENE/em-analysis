set border 15 lw 0
set tics out
set xtics nomirror
set title "title"

plot [0:47] [0:114] "test01.dat" using 12 title "state 0 sojourn time frequency distribution" with impulses,\
"test01.dat" using 38 title "state 0 sojourn time distribution" with linespoints

pause -1 "<Return>: continue."

set ytics 0,1
plot [0:40] [0:3] "test01.dat" using 13 title "final run - state 0 sojourn time frequency distribution" with impulses
set ytics autofreq

pause -1 "<Return>: continue."

set xtics 0,1
plot [0:9] [0:77] "test01.dat" using 14 title "state 1 sojourn time frequency distribution" with impulses,\
"test01.dat" using 39 title "state 1 sojourn time distribution" with linespoints
set xtics autofreq

pause -1 "<Return>: continue."

set xtics 0,1
plot [0:6] [0:80] "test01.dat" using 15 title "state 2 sojourn time frequency distribution" with impulses,\
"test01.dat" using 40 title "state 2 sojourn time distribution" with linespoints
set xtics autofreq

pause -1 "<Return>: continue."

set xtics 0,1
plot [0:9] [0:56] "test01.dat" using 16 title "state 3 sojourn time frequency distribution" with impulses,\
"test01.dat" using 41 title "state 3 sojourn time distribution" with linespoints
set xtics autofreq

pause -1 "<Return>: continue."

plot [0:29] [0:35] "test01.dat" using 17 title "state 4 sojourn time frequency distribution" with impulses,\
"test01.dat" using 42 title "state 4 sojourn time distribution" with linespoints

pause 0 "End."
