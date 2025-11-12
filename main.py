import threading
import winsound
import cv2
import imutils
import pywhatkit
import datetime
import time
import pyautogui

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 600)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 800)

_, start_frame = cap.read()
start_frame = imutils.resize(start_frame, width=500)
start_frame = cv2.cvtColor(start_frame, cv2.COLOR_BGR2GRAY)
start_frame = cv2.GaussianBlur(start_frame, (21, 21), 0)

alarm = False
alarm_mode = False
alarm_counter = 0

def beep_alarm():
    global alarm
    print("🔔 Alarm triggered!")
    for _ in range(10):
        winsound.Beep(2000, 1000)
    alarm = False


def send_whatsapp_alert():
    phone_number = "+917987419605"
    message = "🚨 Alert! motion detected check plzz..."

    try:
        print("📱 Opening WhatsApp Web...")
        pywhatkit.sendwhatmsg_instantly(phone_number, message, wait_time=15, tab_close=False)
        
        # Wait for WhatsApp to fully load and type the message
        time.sleep(12)  # may adjust to 10–15s depending on your internet speed
        
        # Press Enter to send
        pyautogui.hotkey("enter")
        print("✅ Message sent successfully!")
        
    except Exception as e:
        print(f"❌ Failed to send WhatsApp message: {e}")


while True:
    _, frame = cap.read()
    frame = imutils.resize(frame, width=500)

    if alarm_mode:
        frame_bw = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame_bw = cv2.GaussianBlur(frame_bw, (3, 3), 0)
        difference = cv2.absdiff(frame_bw, start_frame)
        threshold = cv2.threshold(difference, 25, 255, cv2.THRESH_BINARY)[1]
        start_frame = frame_bw

        if threshold.sum() > 1000000:
            alarm_counter += 1
        else:
            if alarm_counter > 0:
                alarm_counter -= 1

        cv2.imshow("Cam", threshold)
    else:
        cv2.imshow("Cam", frame)

    if alarm_counter > 20:
        if not alarm:
            alarm = True
            threading.Thread(target=beep_alarm, daemon=True).start()
            threading.Thread(target=send_whatsapp_alert, daemon=True).start()

    key_pressed = cv2.waitKey(30)
    if key_pressed == ord("s"):
        alarm_mode = not alarm_mode
        alarm_counter = 0
        print(f"Alarm mode: {'ON' if alarm_mode else 'OFF'}")
    if key_pressed == ord("q"):
        alarm_mode = False
        break

cap.release()
cv2.destroyAllWindows()

