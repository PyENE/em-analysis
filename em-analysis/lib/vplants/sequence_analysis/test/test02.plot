set border 15 lw 0
set tics out
set xtics nomirror
set title "title"

plot [0:42] [0:13] "test01.dat" using 2 title "time up to the first occurrence of state 0 frequency distribution" with impulses,\
"test01.dat" using 28 title "time up to the first occurrence of state 0 distribution" with linespoints

pause -1 "<Return>: continue."

plot [0:50] [0:6] "test01.dat" using 3 title "time up to the first occurrence of state 1 frequency distribution" with impulses,\
"test01.dat" using 29 title "time up to the first occurrence of state 1 distribution" with linespoints

pause -1 "<Return>: continue."

plot [0:137] [0:6] "test01.dat" using 4 title "time up to the first occurrence of state 2 frequency distribution" with impulses,\
"test01.dat" using 30 title "time up to the first occurrence of state 2 distribution" with linespoints

pause -1 "<Return>: continue."

plot [0:86] [0:5] "test01.dat" using 5 title "time up to the first occurrence of state 3 frequency distribution" with impulses,\
"test01.dat" using 31 title "time up to the first occurrence of state 3 distribution" with linespoints

pause -1 "<Return>: continue."

plot [0:98] [0:3] "test01.dat" using 6 title "time up to the first occurrence of state 4 frequency distribution" with impulses,\
"test01.dat" using 32 title "time up to the first occurrence of state 4 distribution" with linespoints

pause 0 "End."
