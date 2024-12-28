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
    shoulder_y_old = shoulder_y

    if shoulder_yv < 0:
        shoulder_yv = 0
    shoulder_yv = round(shoulder_yv * 10000, 2)

    if (shoulder_yv > 400):
        cv2.putText(frame, "Jump", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        return True
    else:
        cv2.putText(frame, str(shoulder_yv), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        return False

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(image)

    if results.pose_landmarks:
        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        j = IsJump(results.pose_landmarks.landmark)
        
    cv2.imshow('MediaPipe Pose', frame)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break
