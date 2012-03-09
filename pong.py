import pygame, sys

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PADDLE_START_X = 10
PADDLE_START_Y = 20
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 100
BALL_SPEED = 10
BALL_WIDTH_HEIGHT = 16

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pong")

# Rect that contains the ball at the beginning it is set in the center of the screen
ball_rect = pygame.Rect((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2), (BALL_WIDTH_HEIGHT, BALL_WIDTH_HEIGHT))

# Speed of the ball (x, y)
ball_speed = [BALL_SPEED, BALL_SPEED]
paddle_sound = 'Memo.wav'

# Your paddle vertically centered on the left side
paddle_rect = pygame.Rect((PADDLE_START_X, PADDLE_START_Y), (PADDLE_WIDTH, PADDLE_HEIGHT))
paddle2_rect = pygame.Rect((SCREEN_WIDTH - PADDLE_WIDTH - PADDLE_START_X, SCREEN_HEIGHT - PADDLE_HEIGHT - PADDLE_START_Y), (PADDLE_WIDTH, PADDLE_HEIGHT))

# Scoring: 1 point if you hit the ball, -5 point if you miss the ball
score = 0
opponent_score = 0
# Load the font for displaying the score
font = pygame.font.Font(None, 30)
player1 = False
player2 = False
screen_id = 0


# Game loop
while True:
	if screen_id == 0:
		if score == 11 or opponent_score == 11:
			screen_id = 1
			score = 0
			opponent_score = 0
			if score == 11:
				player1 = True
			if opponent_score == 11:
				player2  = True
	# Event handler
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit(0)
				pygame.quit()
		# Control the paddle with the mouse
			elif event.type == pygame.MOUSEMOTION:
				paddle_rect.centery = event.pos[1]
			# correct paddle position if it's going out of window
				if paddle_rect.top < 0:
					paddle_rect.top = 0
				elif paddle_rect.bottom >= SCREEN_HEIGHT:
					paddle_rect.bottom = SCREEN_HEIGHT

	# This test if up or down keys are pressed; if yes, move the paddle
		if pygame.key.get_pressed()[pygame.K_w] and paddle_rect.top > 0:
			paddle_rect.top -= BALL_SPEED
		elif pygame.key.get_pressed()[pygame.K_s] and paddle_rect.bottom < SCREEN_HEIGHT:
			paddle_rect.top += BALL_SPEED
		elif pygame.key.get_pressed()[pygame.K_ESCAPE]:
			sys.exit(0)
			pygame.quit()
		if pygame.key.get_pressed()[pygame.K_UP] and paddle2_rect.top > 0:
			paddle2_rect.top -= BALL_SPEED
		elif pygame.key.get_pressed()[pygame.K_DOWN] and paddle2_rect.bottom < SCREEN_HEIGHT:
			paddle2_rect.top += BALL_SPEED

	
		
	# Update ball position
		ball_rect.left += ball_speed[0]
		ball_rect.top += ball_speed[1]

	# Ball collision with rails
		if ball_rect.top <= 0 or ball_rect.bottom >= SCREEN_HEIGHT:
			ball_speed[1] = -ball_speed[1]
		if ball_rect.right >= SCREEN_WIDTH or ball_rect.left <= 0:
			ball_speed[0] = -ball_speed[0]
			if ball_rect.left <= 0:
				opponent_score += 1
				ball_rect.left = (SCREEN_WIDTH / 2)
				ball_rect.top = (SCREEN_HEIGHT / 2)
			if ball_rect.right >= SCREEN_WIDTH:
				score += 1
				ball_rect.left = (SCREEN_WIDTH / 2)
				ball_rect.top = (SCREEN_HEIGHT / 2)
	# Test if the ball is hit by the paddle; if yes reverse speed and add a point
		if paddle_rect.colliderect(ball_rect):
			ball_speed[0] = -ball_speed[0]
			pygame.mixer.music.load('pluck.wav')
                       	pygame.mixer.music.play()
		if paddle2_rect.colliderect(ball_rect):
			ball_speed[0] = -ball_speed[0]
			pygame.mixer.music.load('pluck.wav')
			pygame.mixer.music.play()
	
	# Render the ball, the paddle, and the score
		pygame.draw.rect(screen, (0, 0, 0), paddle_rect) # Your paddle
		pygame.draw.rect(screen, (0, 0, 0), paddle2_rect) 
		pygame.draw.circle(screen, (0, 0, 0), ball_rect.center, ball_rect.width / 2) # The ball
		opponent_text =  font.render(str(opponent_score), True, (0, 0, 0))
   		screen.blit(opponent_text, (3*(SCREEN_WIDTH / 4) - font.size(str(opponent_score))[0] / 2, 5)) 
		score_text = font.render(str(score), True, (0, 0, 0))
		screen.blit(score_text, ((SCREEN_WIDTH / 4) - font.size(str(score))[0] / 2, 5)) # The score
		pygame.draw.line(screen, (0,0,0), (SCREEN_WIDTH / 2, 0), (SCREEN_WIDTH/2, SCREEN_HEIGHT), 8)	
		pygame.draw.aaline(screen, (255,0,0), (SCREEN_WIDTH / 2 - 10, 0), (SCREEN_WIDTH/2 - 10, SCREEN_HEIGHT), 4)
		pygame.draw.aaline(screen, (255,0,0), (SCREEN_WIDTH / 2 + 10, 0), (SCREEN_WIDTH/2 + 10, SCREEN_HEIGHT), 4)
	# Update screen and wait 20 milliseconds
	pygame.display.flip()
	pygame.time.delay(20)
	screen.fill((255, 255, 255))

	if screen_id == 1:
		if player1:
			text = "Player 1 wins! Play again? Press (y/n)"
		else:
			text = "Player 2 wins! Play again? Press (y/n)"
		score_text = font.render(text, True, (0, 0, 0))
		screen.blit(score_text, (SCREEN_WIDTH/2 - 175, SCREEN_HEIGHT/2 - 30))
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit(0)
				pygame.quit()
		if pygame.key.get_pressed()[pygame.K_y]:
			screen_id = 0
		elif pygame.key.get_pressed()[pygame.K_n]:
			sys.exit(0)
			pygame.quit()
