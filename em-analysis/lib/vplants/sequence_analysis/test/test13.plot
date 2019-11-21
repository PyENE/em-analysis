set border 15 lw 0
set tics out
set xtics nomirror
set title "title"

set xtics 0,1
plot [0:8] [0:12] "test11.dat" using 5 title "value 0 recurrence time frequency distribution" with impulses
set xtics autofreq

pause -1 "<Return>: continue."

set xtics 0,1
plot [0:7] [0:16] "test11.dat" using 6 title "value 1 recurrence time frequency distribution" with impulses
set xtics autofreq

pause -1 "<Return>: continue."

set ytics 0,1
plot [0:16] [0:9] "test11.dat" using 7 title "value 2 recurrence time frequency distribution" with impulses
set ytics autofreq

pause 0 "End."
