from browser import document, ajax, bind
from minimax.helper_functions import NUM_IN_A_ROW
import json

ROWS = 6
COLS = 7
board = [['.'] * COLS for _ in range(ROWS)]
turn = 'r'

def draw_board():
    game_board = document['game-board']
    game_board.clear()

    for r in range(ROWS):
        for c in range(COLS):
            cell = document.createElement('div')  # Changed create_element to createElement
            cell.className = 'cell'  # Changed class_name to className
            cell.attrs['data-row'] = str(r)
            cell.attrs['data-col'] = str(c)
            cell.bind('click', handle_click)
            game_board <= cell

    update_board()

def update_board():
    cells = document.select('.cell')
    for cell in cells:
        row = int(cell.attrs['data-row'])
        col = int(cell.attrs['data-col'])
        cell.class_name = 'cell'
        if board[row][col] == 'r':
            cell.class_name += ' red'
        elif board[row][col] == 'y':
            cell.class_name += ' yellow'

@bind('.cell', 'click')
def handle_click(event):
    global turn
    if turn == 'r':
        col = int(event.target.attrs['data-col'])
        for r in range(ROWS - 1, -1, -1):
            if board[r][col] == '.':
                board[r][col] = turn
                break
        update_board()
        turn = 'y'
        check_winner()
        if not check_winner():
            computer_move()

from browser import ajax, console

def computer_move():
    global turn
    contents = ','.join([''.join(row) for row in board])

    def on_success(req):
        console.log(f"Received response with status: {req.status}")
        if req.status in [200, 204]:  # Success status codes
            try:
                global turn
                # Assuming the server responds with JSON like: {"bestMove": 3}
                response = json.loads(req.text)
                best_move = int(response['bestMove'])
                console.log(f"Success: Best move received is {best_move}")
                
                for r in range(ROWS - 1, -1, -1):
                    if board[r][best_move] == '.':
                        board[r][best_move] = turn
                        break
                update_board()
                turn = 'r'  # Assuming it switches to the other player
                check_winner()
            except Exception as e:
                console.error(f"Error processing the response: {e}")
        else:
            console.error(f"Error: {req.status} - {req.text}")

    # Prepare the data as a JSON object
    data = json.dumps({'contents': contents, 'turn': turn})
    ajax.post('/api/move', data=data, headers={'Content-Type': 'application/json'}, oncomplete=on_success)

# Note: Replace console.log/error with print if you prefer plain logging


def check_winner():
    result = document['result']
    if NUM_IN_A_ROW(board, 4, 'r') > 0:
        result.text = 'You win!'
        return True
    elif NUM_IN_A_ROW(board, 4, 'y') > 0:
        result.text = 'Computer wins!'
        return True
    return False

draw_board()