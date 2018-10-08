set border 15 lw 0
set tics out
set xtics nomirror
set title "title"

set xtics 0,1
plot [0:3] [0:12] "test11.dat" using 8 title "value 0 sojourn time frequency distribution" with impulses
set xtics autofreq

pause -1 "<Return>: continue."

set xtics 0,1
set ytics 0,1
plot [0:5] [0:2] "test11.dat" using 9 title "final run - value 0 sojourn time frequency distribution" with impulses
set xtics autofreq
set ytics autofreq

pause -1 "<Return>: continue."

set xtics 0,1
set ytics 0,1
plot [0:4] [0:6] "test11.dat" using 10 title "value 1 sojourn time frequency distribution" with impulses
set xtics autofreq
set ytics autofreq

pause -1 "<Return>: continue."

set xtics 0,1
set ytics 0,1
plot [0:1] [0:2] "test11.dat" using 11 title "final run - value 1 sojourn time frequency distribution" with impulses
set xtics autofreq
set ytics autofreq

pause -1 "<Return>: continue."

set xtics 0,1
set ytics 0,1
plot [0:3] [0:5] "test11.dat" using 12 title "value 2 sojourn time frequency distribution" with impulses
set xtics autofreq
set ytics autofreq

pause 0 "End."
