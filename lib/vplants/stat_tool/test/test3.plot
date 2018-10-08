set border 15 lw 0
set tics out
set xtics nomirror
set title "title"

set xtics 0,1
set ytics 0,1
plot [0:3] [0:2] "test3.dat" using 1 title "variable 3 marginal frequency distribution" with impulses
set xtics autofreq
set ytics autofreq

pause -1 "<Return>: continue."

set xlabel "variable 3"
set ylabel "variable 1"
set xtics 0,1
set ytics 0,1
set label "1" at 1,1
set label "1" at 3,1
plot [1:3] [1:2] "test0.dat" using 3:1 notitle with points
unset label
set xlabel
set ylabel
set xtics autofreq
set ytics autofreq

pause -1 "<Return>: continue."

set xlabel "variable 3"
set ylabel "variable 2"
set xtics 0,1
set ytics 0,1
set label "1" at 1,3
set label "1" at 3,2
plot [1:3] [2:3] "test0.dat" using 3:2 notitle with points
unset label
set xlabel
set ylabel
set xtics autofreq
set ytics autofreq


pause 0 "End."
