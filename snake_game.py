import curses
import random
import time

def main(stdscr):

    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)  # Snake
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)    # Food
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)  # Text

    curses.curs_set(0)
    
    stdscr.clear()
    height, width = stdscr.getmaxyx()
    
    snake = [(height // 2, width // 4)]  
    direction = curses.KEY_RIGHT        
    food = (height // 2, width // 2)    
    score = 0
    speed = 0.1                         
    game_over = False
    
    win = curses.newwin(height, width, 0, 0)
    win.keypad(1)
    win.timeout(100)  
    
    
    win.border(0)
    
    
    while not game_over:
        
        win.addstr(0, 5, f" Score: {score} ")
        win.addstr(0, width - 20, " Press 'q' to quit ")
        
        win.addch(food[0], food[1], '*', curses.color_pair(2))
        
        for i, (y, x) in enumerate(snake):
            if i == 0:  # Snake head
                win.addch(y, x, '@', curses.color_pair(1))
            else:       # Snake body
                win.addch(y, x, 'O', curses.color_pair(1))
        
        key = win.getch()
        
        if key == ord('q'):
            break
        
        if key == curses.KEY_UP and direction != curses.KEY_DOWN:
            direction = curses.KEY_UP
        elif key == curses.KEY_DOWN and direction != curses.KEY_UP:
            direction = curses.KEY_DOWN
        elif key == curses.KEY_LEFT and direction != curses.KEY_RIGHT:
            direction = curses.KEY_LEFT
        elif key == curses.KEY_RIGHT and direction != curses.KEY_LEFT:
            direction = curses.KEY_RIGHT
        
        head_y, head_x = snake[0]
        if direction == curses.KEY_UP:
            head_y -= 1
        elif direction == curses.KEY_DOWN:
            head_y += 1
        elif direction == curses.KEY_LEFT:
            head_x -= 1
        elif direction == curses.KEY_RIGHT:
            head_x += 1
        
        snake.insert(0, (head_y, head_x))
        
        if (head_y == 0 or head_y == height - 1 or 
            head_x == 0 or head_x == width - 1):
            game_over = True
            continue
        
        if snake[0] in snake[1:]:
            game_over = True
            continue
        
        if snake[0] == food:
           
            score += 10
            
            while True:
                new_food = (random.randint(1, height - 2), 
                           random.randint(1, width - 2))
                
                if new_food not in snake:
                    food = new_food
                    break
        else:
            
            last = snake.pop()
            win.addch(last[0], last[1], ' ')
        
        win.refresh()
        time.sleep(speed)
    
    
    win.clear()
    win.border(0)
    message = "GAME OVER!"
    win.addstr(height // 2 - 1, (width - len(message)) // 2, message, curses.color_pair(3) | curses.A_BOLD)
    score_msg = f"Final Score: {score}"
    win.addstr(height // 2 + 1, (width - len(score_msg)) // 2, score_msg, curses.color_pair(3))
    exit_msg = "Press any key to exit"
    win.addstr(height // 2 + 3, (width - len(exit_msg)) // 2, exit_msg, curses.color_pair(3))
    win.refresh()
    win.getch()  

if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        pass
    finally:
        print("Thanks for playing Snake!")
