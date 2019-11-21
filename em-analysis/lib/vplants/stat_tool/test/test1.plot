set border 15 lw 0
set tics out
set xtics nomirror
set title "title"

set xtics 0,1
set ytics 0,1
plot [0:1] [0:3] "test1.dat" using 1 title "variable 1 marginal frequency distribution" with impulses
set xtics autofreq
set ytics autofreq

pause -1 "<Return>: continue."

set xlabel "variable 1"
set ylabel "variable 2"
set xtics 0,1
set ytics 0,1
set label "1" at 1,2
set label "1" at 1,3
plot [1:2] [2:3] "test0.dat" using 1:2 notitle with points
unset label
set xlabel
set ylabel
set xtics autofreq
set ytics autofreq

pause -1 "<Return>: continue."

set xlabel "variable 1"
set ylabel "variable 3"
set xtics 0,1
set ytics 0,1
set label "1" at 1,1
set label "1" at 1,3
plot [1:2] [1:3] "test0.dat" using 1:3 notitle with points
unset label
set xlabel
set ylabel
set xtics autofreq
set ytics autofreq


pause 0 "End."
