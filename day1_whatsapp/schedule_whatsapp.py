# save as schedule_whatsapp.py
import pywhatkit as kit
from datetime import datetime, timedelta

def schedule_message(phone, message, delay_minutes=2):
    # ensure at least 2 minutes in future (pywhatkit needs a small buffer)
    if delay_minutes < 2:
        delay_minutes = 2
    send_time = datetime.now() + timedelta(minutes=delay_minutes)
    hour = send_time.hour
    minute = send_time.minute
    print(f"Scheduling message to {phone} at {hour:02d}:{minute:02d} (current time {datetime.now().strftime('%H:%M:%S')})")
    # This will open browser and send the message at given hour:minute
    kit.sendwhatmsg(phone, message, hour, minute)
    print("Browser opened. Wait for the message to send at scheduled time.")

if __name__ == "__main__":
    phone = input("Enter phone (with country code), e.g. +91XXXXXXXXXX: ").strip()
    message = input("Enter message: ").strip()
    delay = input("Send after how many minutes from now? (>=2, default 2): ").strip()
    try:
        delay = int(delay) if delay else 2
    except:
        delay = 2
    schedule_message(phone, message, delay)
