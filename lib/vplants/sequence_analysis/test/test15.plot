set border 15 lw 0
set tics out
set xtics nomirror
set title "title"

set xtics 0,1
set ytics 0,1
plot [0:6] [0:2] "test11.dat" using 13 title "number of runs of value 0 per sequence frequency distribution" with impulses
set xtics autofreq
set ytics autofreq

pause -1 "<Return>: continue."

set ytics 0,1
plot [0:11] [0:2] "test11.dat" using 14 title "number of occurrences of value 0 per sequence frequency distribution" with impulses
set ytics autofreq

pause -1 "<Return>: continue."

set xtics 0,1
set ytics 0,1
plot [0:8] [0:2] "test11.dat" using 15 title "number of runs of value 1 per sequence frequency distribution" with impulses
set xtics autofreq
set ytics autofreq

pause -1 "<Return>: continue."

set ytics 0,1
plot [0:15] [0:2] "test11.dat" using 16 title "number of occurrences of value 1 per sequence frequency distribution" with impulses
set ytics autofreq

pause -1 "<Return>: continue."

set xtics 0,1
set ytics 0,1
plot [0:3] [0:2] "test11.dat" using 17 title "number of runs of value 2 per sequence frequency distribution" with impulses
set xtics autofreq
set ytics autofreq

pause -1 "<Return>: continue."

set xtics 0,1
set ytics 0,1
plot [0:7] [0:2] "test11.dat" using 18 title "number of occurrences of value 2 per sequence frequency distribution" with impulses
set xtics autofreq
set ytics autofreq

pause -1 "<Return>: continue."

set ytics 0,1
plot [0:30] [0:2] "test11.dat" using 1 title "sequence length frequency distribution" with impulses
set ytics autofreq

pause 0 "End."
