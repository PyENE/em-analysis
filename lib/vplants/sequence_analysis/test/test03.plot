set border 15 lw 0
set tics out
set xtics nomirror
set title "title"

plot [0:33] [0:780] "test01.dat" using 7 title "state 0 recurrence time frequency distribution" with impulses,\
"test01.dat" using 33 title "state 0 recurrence time distribution" with linespoints

pause -1 "<Return>: continue."

plot [0:121] [0:98] "test01.dat" using 8 title "state 1 recurrence time frequency distribution" with impulses,\
"test01.dat" using 34 title "state 1 recurrence time distribution" with linespoints

pause -1 "<Return>: continue."

plot [0:135] [0:45] "test01.dat" using 9 title "state 2 recurrence time frequency distribution" with impulses,\
"test01.dat" using 35 title "state 2 recurrence time distribution" with linespoints

pause -1 "<Return>: continue."

plot [0:65] [0:48] "test01.dat" using 10 title "state 3 recurrence time frequency distribution" with impulses,\
"test01.dat" using 36 title "state 3 recurrence time distribution" with linespoints

pause -1 "<Return>: continue."

plot [0:53] [0:308] "test01.dat" using 11 title "state 4 recurrence time frequency distribution" with impulses,\
"test01.dat" using 37 title "state 4 recurrence time distribution" with linespoints

pause 0 "End."
