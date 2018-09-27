## TDT4136 AI Assignment 2 © by Petter Rein & Balázs Orbán @ NTNU - 2018

Available flags are:

    --help, -h - Show help
    --source, -s - Specify the source file for the input
    --show-checked, -C - Show the checked blocks
    --show-board, -B - Show the original board
    --mode, -m - Specify the algorithm to run. Possible values are:
        Default: If mode is omitted, A* without cost is run.
        bfs - Run Best-First Search
        dijkstra - Run Dijkstra's algorithm
        cost - Run A* with cost

Block types:
    representation - name - cost to pass

    🏁  - goal - Ø
    🚩  - start - Ø
    👠  - found path - Ø
    🛤  - road - 1
    🌱  - grassland - 5 
    🌳  - forest - 10
    ⛰  - mountain - 50
    🌊  - water - 100
    ❔  - checked - Ø
    🚧  - obstacle - not passable

    Ø - There is no point in measuring the cost to pass