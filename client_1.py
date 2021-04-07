from time import sleep
from sense_hat import SenseHat
import random
from network import Network

sense = SenseHat()
ball_position = [4, 4]
ball_speed = [-1, -1]

class Player():
    def __init__(self,x,y,color):
        self.x = x
        self.y = y
        self.c = color
        
    def draw_player(self):
        sense.set_pixel(self.x, self.y, self.c)
        sense.set_pixel(self.x, self.y + 1, self.c)
        sense.set_pixel(self.x, self.y - 1, self.c)
    
    def move_up(self, event):
        if self.y > 1 and self.y < 7 and event.action== 'pressed':
            self.y -= 1
        
    def move_down(self, event):
        if self.y > 0 and self.y < 6 and event.action== 'pressed':
            self.y += 1


class Game:
    def __init__(self):
        self.net = Network()
        self.player = Player(0, 4,(255,255,255))
        self.player2 = Player(7, 4,(255,255,255))
        sense.stick.direction_up = self.player.move_up
        sense.stick.direction_down = self.player.move_down
        

    def ball_play(self):
        # Sets ball position and color
        sense.set_pixel(ball_position[0], ball_position[1], 0, 0, 255)

        # Moves ball diagonally depening on the ball_speed list         
        ball_position[0] += ball_speed[0]
        ball_position[1] += ball_speed[1]

        # If ball hit the top or bottom side
        if ball_position[1] == 0 or ball_position[1] == 7:
            # Reverese the y direction of the ball
            ball_speed[1] = -ball_speed[1]

        # If ball hits the other player base
        if ball_position[0] == 7 and self.player2.y-1 <= ball_position[1] <= self.player2.y+1:
            # Reverese the x direction of the ball
            ball_speed[0] = -ball_speed[0]

        # If ball hits player's base
        if ball_position[0] == 1 and self.player.y-1 <= ball_position[1] <= self.player.y+1:
            # Reverese the x direction of the ball
            ball_speed[0] = -ball_speed[0]
        
        # If player didn't catch the ball
        if ball_position[0] == 0:
            sense.show_message("P1 Lose", text_colour=(255, 0, 0))
            self.reset_game()
            return False
        
        # If the other player didn't catch the ball
        if ball_position[0] == 8:
            sense.show_message("P2 Lose", text_colour=(255, 0, 0))
            self.reset_game()
            return False
        
        sleep(0.3)
        return True
    
    def reset_game(self):
        global ball_position, ball_speed
        self.player.y = 4
        self.player2.y = 4
        ball_position = [4, 4]
        ball_speed = [-1, -1]
        self.run()
        
    def run(self):
        while self.ball_play():
            # clear sense hat display
            sense.clear()
            
            # Get other player's position
            self.player2.x, self.player2.y = self.parse_data(self.send_data())
            
            self.player.draw_player()
            self.player2.draw_player()

    # Send player's position to server
    def send_data(self):
        data = str(self.net.id) + ":" + str(self.player.x) + "," + str(self.player.y)
        reply = self.net.send(data)
        return reply

    @staticmethod
    def parse_data(data):
        try:
            d = data.split(":")[1].split(",")
            return int(d[0]), int(d[1])
        except:
            return 0,0