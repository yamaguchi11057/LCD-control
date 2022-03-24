#import 
import RPi.GPIO as GPIO
import time
 
# 各種ピン配列を入力
LCD_RS = 7
LCD_E  = 8
LCD_DB = {"DB7":18, "DB6":23, "DB5":24, "DB4":25,
          "DB3":4, "DB2":17, "DB1":27, "DB0":22}

# 機器情報の入力
LCD_WIDTH = 16    # Maximum characters per line
LCD_CHR = True    # 文字データ入力モード
LCD_CMD = False   # コマンド入力モード
 
LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line
# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005
 
def main():
  # Main program block
  GPIO.setwarnings(False)
  GPIO.setmode(GPIO.BCM)       # Use BCM GPIO numbers
  GPIO.setup(LCD_E, GPIO.OUT)  # E
  GPIO.setup(LCD_RS, GPIO.OUT) # RS
  for i in LCD_DB.values():
    GPIO.setup(i, GPIO.OUT)
    print(f"npin={i}は{GPIO.OUT}に設定されました")

  # Initialise display
  lcd_init()
 
  while True:
 
    # Send some test
    lcd_string("Rasbperry Pi",LCD_LINE_1)
    lcd_string("16x2 LCD Test",LCD_LINE_2)
 
    time.sleep(3) # 3 second delay
 
    # Send some text
    lcd_string("1234567890123456",LCD_LINE_1)
    lcd_string("abcdefghijklmnop",LCD_LINE_2)
 
    time.sleep(3) # 3 second delay
 
    # Send some text
    lcd_string("RaspberryPi-spy",LCD_LINE_1)
    lcd_string(".co.uk",LCD_LINE_2)
 
    time.sleep(3)
 
    # Send some text
    lcd_string("Follow me on",LCD_LINE_1)
    lcd_string("Twitter @RPiSpy",LCD_LINE_2)
 
    time.sleep(3)
 
def lcd_init():
  # Initialise display
  lcd_byte(0x30,LCD_CMD) # 0011 0011 Initialise
  lcd_byte(0x30,LCD_CMD) # 0011 0011 Initialise  
  lcd_byte(0x30,LCD_CMD) # 0011 0011 Isnitialise
  lcd_byte(0x06,LCD_CMD) # 0000 0110 Cursor move direction
  lcd_byte(0x0C,LCD_CMD) # 0000 1100 Display On,Cursor Off, Blink Off
  lcd_byte(0x38,LCD_CMD) # 0011 1000 Data length, number of lines, font size
  lcd_byte(0x01,LCD_CMD) # 0000 0001 Clear display
  time.sleep(E_DELAY)
 
def lcd_byte(bits, mode):
  # Send byte to data pins
  # bits = data
  # mode = True  for character
  #        False for command
 
  GPIO.output(LCD_RS, mode) # RS
 
  #全てのピンをオフ
  for i in LCD_DB.values():
    GPIO.output(i, False)

  #DB0から順番にピン出力を決定していく
  for i in range(len(LCD_DB)):
    if bits&0x01<<i == 0x01<<i:
      pin = f'DB{i}'
      GPIO.output(LCD_DB[pin], True)
  # Toggle 'Enable' pin
  lcd_toggle_enable()
 
def lcd_toggle_enable():
  # Toggle enable
  time.sleep(E_DELAY)
  GPIO.output(LCD_E, True)
  time.sleep(E_PULSE)
  GPIO.output(LCD_E, False)
  time.sleep(E_DELAY)
 
def lcd_string(message,line):
  # Send string to display
 
  message = message.ljust(LCD_WIDTH," ")
 
  lcd_byte(line, LCD_CMD)
 
  for i in range(LCD_WIDTH):
    lcd_byte(ord(message[i]),LCD_CHR)
 
if __name__ == '__main__':
 
  try:
    main()
  except KeyboardInterrupt:
    pass
  finally:
    lcd_byte(0x01, LCD_CMD)
    lcd_string("Goodbye!",LCD_LINE_1)
    GPIO.cleanup()
    print("control+cが押されたため動作を終了しました。")