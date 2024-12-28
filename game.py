import pygame
import sys

import cv2
import mediapipe as mp

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(1)
shoulder_yv = 0
shoulder_y_old = 0
def IsJump(landmarks):
    global shoulder_y_old
    global shoulder_yv

    left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
    right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
            
    #print("Left Shoulder: (", left_shoulder.x, ",", left_shoulder.y, ")")
    #print("Right Shoulder: (", right_shoulder.x, ",", right_shoulder.y, ")")
    shoulder_y = 1 - (left_shoulder.y + right_shoulder.y) / 2

    shoulder_yv = shoulder_y - shoulder_y_old
    if shoulder_y_old == 0:
        shoulder_y_old = shoulder_y
        return False
    else:
        shoulder_y_old = shoulder_y

        if shoulder_yv < 0:
            shoulder_yv = 0
        shoulder_yv = round(shoulder_yv * 10000, 2)

        if (shoulder_yv > 300):
            cv2.putText(frame, "Jump", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            return True
        else:
            cv2.putText(frame, str(shoulder_yv), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            return False

pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jump Rope Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Rope properties
rope_y = 0

rope_speed_init = 10
rope_speed = rope_speed_init

# Player properties
player_x = WIDTH // 2
player_y = HEIGHT // 2
player_width = 50
player_height = 50
player_color = RED

# Game loop
clock = pygame.time.Clock()
running = True
jumping = False
jump_height = 150
jump_speed = 5
jump_progress = 0

jump_count = 0
while running and cap.isOpened():

    ret, frame = cap.read()
    if not ret:
        break

    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(image)
        
    #cv2.imshow('MediaPipe Pose', frame)

    """
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    j = False
    if results.pose_landmarks:
        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        j = IsJump(results.pose_landmarks.landmark)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] or j and not jumping:
        jumping = True
        jump_progress = 0

    if jumping:
        jump_progress += jump_speed * 6  # Increase the jump speed multiplier
        if jump_progress >= jump_height * 2:
            jumping = False
            jump_count += 1
        else:
            scale_factor = 1 + (jump_height - abs(jump_height - jump_progress)) / jump_height
            player_width = int(50 * scale_factor)
            player_height = int(50 * scale_factor)
    else:
        player_width = 50
        player_height = 50

    # Update rope position
    rope_y += rope_speed
    if rope_y > HEIGHT:
        rope_speed = -rope_speed_init
    if rope_y < 0:
        rope_speed = rope_speed_init
    
    if rope_speed < 0:
        rope_speed -= 5
    if rope_speed > 0:
        rope_speed += 5

    # Check for collision
    
    if not jumping and player_y + player_height // 2 > rope_y and player_y - player_height // 2 < rope_y:
        font = pygame.font.Font(None, 74)
        text = font.render("Game Over", True, BLACK)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
        pygame.display.flip()
        pygame.time.wait(5000)
        running = False

    # Drawing
    screen.fill(WHITE)
    player_rect = pygame.Rect(player_x - player_width // 2, player_y - player_height // 2, player_width, player_height)
    pygame.draw.rect(screen, player_color, player_rect)
    pygame.draw.line(screen, BLACK, (0, rope_y), (WIDTH, rope_y), 5)

    # Display jump count
    font = pygame.font.Font(None, 108)
    jump_count_text = font.render(f"Jumps: {jump_count}", True, BLACK)
    screen.blit(jump_count_text, (10, 10))

    pygame.display.flip()

    clock.tick(30)

pygame.quit()
sys.exit()