from random import randint
from math import dist

gato =  r"""
 _._     _,-'""`-._
 (,-.`._,'(       |\`-/|
     `-.-' \ )-`( , o o)
          `-    \`_`"'-
"""

rata = r"""
          _   _
         (_)/` |
       _(_) ^ /
       >\|  -;   _
       \_/    \_/<
        /    ,__/
       ;     |
       |    .-.
       |       )_
     .-\______;__>
    (__..._      _
           `--''` )

"""

def crear(n):
    matrix = []
    for i in range(n):
        row = []
        for j in range(n):
            row.append('-------')  
        matrix.append(row)
    return matrix

def cat_moves(pos):
    x, y = pos
    moves = []
    offsets = [(2,1),(2,-1),(-2,1),(-2,-1),
               (1,2),(1,-2),(-1,2),(-1,-2)]
    
    for dx, dy in offsets:
        nx, ny = x + dx, y + dy
        if 0 <= nx < N and 0 <= ny < N:  
            moves.append((nx, ny))
    return moves

def rat_moves(pos, cat=None, max_range=4):
    x, y = pos
    moves = []
    directions = [(1,0),(-1,0),(0,1),(0,-1),
                  (1,1),(1,-1),(-1,1),(-1,-1)]
    
    for dx, dy in directions:
        nx, ny = x, y
        steps = 0
        while steps < max_range and 0 <= nx+dx < N and 0 <= ny+dy < N:
            nx, ny = nx + dx, ny + dy
            moves.append((nx, ny))
            steps += 1
            if (nx, ny) == cat:
                break
    return moves

def mega_knight(a, b):
    ax, ay = a
    bx, by = b
    return max(abs(ax - bx), abs(ay - by))

def is_captured(cat, rat):
    return mega_knight(cat, rat) <= 1

def evaluate(cat, rat):
    if cat == rat:
        return -1000
    return dist(cat, rat)

def ajd(coordenada:list):
    x, y = coordenada
    ajedrez = [chr(x+97), y+1]  
    return ajedrez
 
def dja(ajedrez:list):
    x, y = ajedrez
    coordenada = [ord(x)-97, y-1]
    return coordenada

def minimax(cat, rat, depth, maximizing):
    if depth == 0 or is_captured(cat, rat):
        return evaluate(cat, rat), (cat if not maximizing else rat)

    # Turno de la rata
    if maximizing:  
        best_val = float("-inf")
        best_move = rat
        for mov in rat_moves(rat, cat):
            val, _ = minimax(cat, mov, depth-1, False)
            if val > best_val:
                best_val = val
                best_move = mov
        return best_val, best_move
    
    # Turno del gato
    else:  
        worst_val = float("inf")
        best_move = cat
        for mov in cat_moves(cat):
            val, _ = minimax(mov, rat, depth-1, True)
            if val < worst_val:
                worst_val = val
                best_move = mov
        return worst_val, best_move

def mostrar(matrix):
    n = len(matrix)
    for j in range(n):
        etiqueta = n - j
        print(etiqueta, end='    ')
        for k in range(n):
            col = k
            fila_idx = n - 1 - j
            celda = matrix[col][fila_idx]
            end = '\n' if k == n-1 else ' '
            print(celda, end=end)
    print('X', end='    ')
    for k in range(n):
        print(f'   {chr(97+k)}    ', end='')
    print()

def jugar(n, max_turns):
    board = crear(n)
    global N
    N = n
    cat = [0, 0]          
    rat = [n-1, n-1]      

    for turn in range(1, max_turns+1):
        print(f"\n--- Turno N°: {turn} ---")
        
        board = crear(n)
        board[cat[0]][cat[1]] = "=^-_-^="
        board[rat[0]][rat[1]] = "<:3 )~~"
        mostrar(board)

        if is_captured(cat, rat):
            print("La rata fue atrapada!!!")
            print(gato)
            return
        
        # Movimiento del gato
        legal_moves = cat_moves(tuple(cat))
        print("Movimientos posibles:", [ajd(m) for m in legal_moves])

        valid = False
        while not valid:
            mov = input("Su movimiento: ").lower()
            if len(mov) == 2 and mov[0].isalpha() and mov[1].isdigit():
                col, row = mov[0], int(mov[1])
                chosen = dja([col, row]) 

                if tuple(chosen) in legal_moves:
                    cat = chosen
                    valid = True
                else:
                    print("❌ Movimiento invalido, pruebe otra vez")
            else:
                print("❌ Input invalido, use notacion de ajedrez")

        if is_captured(cat, rat):
            print("La rata fue atrapada!!!")
            print(gato)
            return
        
        # Movimiento de la rata (IA)
        _, best_rat = minimax(tuple(cat), tuple(rat), depth=3, maximizing=True)
        rat = list(best_rat)
        print("La rata se escapa a:", ajd(rat))
        
        if is_captured(cat, rat):
            print("La rata fue atrapada!!!")
            print(gato)
            return
    
    print(f"La rata sobrevivio {max_turns} turnos y escapo")
    print(rata)



jugar(8,4)
