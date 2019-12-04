import serial
import time
import sqlite3
import RPi.GPIO as GPIO

GREEN_LED_PIN = 6
RED_LED_PIN = 5
BUZZER_PIN = 25
TOTAL_BITS = 12
STRIPPED_BITS = 10
BAN_USER = 1
ADD_USER = 0
SECONDS = 2
HERTZ = 2400
DATABASE = 'tagreads.db'

GPIO.setmode(GPIO.BCM)
GPIO.setup(GREEN_LED, GPIO.OUT)
GPIO.setup(RED_LED, GPIO.OUT)
GPIO.setup(BUZZER, GPIO.OUT)

# open sqlite database file
db = sqlite3.connect(DATABASE)
cursor = db.cursor()

# check that the correct tables exists in database; create them if they do not
tables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND (name='tagreads');").fetchall()
if len(tables) == 0 :
cursor.execute("CREATE table tagreads (timestamp, tagid text PRIMARY KEY, banned)")

# connect to serial port on which the RFID reader is attached
port = serial.Serial('/dev/ttyAMA0', HERTZ, timeout=1)

def rfid_read():

count = 0
try:
while true:
  # attempt to read in a tag
  try:
	tagid = port.read(TOTAL_BITS)
	if(len(tagid) != 0):


	  tagid = tagid.strip()
	  timestamp = time.time()
	  if (len(tagid) == STRIPPED_BITS):
		cursor.execute("SELECT banned from tagreads WHERE tagid = ?",[tagid])
		row = cursor.fetchall()
					if (len(row) == 0):
		  print("Security Alert! Unauthorized access attempt!")
		  GPIO.output(BUZZER_PIN, GPIO.HIGH)
		  GPIO.output(RED_LED_PIN, GPIO.HIGH)
		  time.sleep(1)
		  GPIO.output(RED_LED_PIN, GPIO.LOW)
		  GPIO.output(BUZZER_PIN, GPIO.LOW)
		else:
		  tup = row[0]
					  num = tup[0]
					  print(num)
		  if (num == 1):
			print("Security Alert! User is banned!")
			GPIO.output(RED_LED_PIN, GPIO.HIGH)
			GPIO.output(BUZZER_PIN, GPIO.HIGH)
			time.sleep(.5)
			GPIO.output(BUZZER, GPIO.LOW)
			GPIO.output(RED_LED_PIN, GPIO.LOW)
			time.sleep(.2)
			GPIO.output(RED_LED_PIN, GPIO.HIGH)
							 GPIO.output(BUZZER_PIN, GPIO.HIGH)
			time.sleep(.2)
			GPIO.output(RED_LED_PIN, GPIO.LOW)
			GPIO.output(BUZZER_PIN, GPIO.LOW)
		  else:
			print("Welcome!")
			GPIO.output(GREEN_LED_PIN, GPIO.HIGH)
			time.sleep(1)
			GPIO.output(GREEN_LED_PIN, GPIO.LOW)
		print("Time:%s, Tag:%s" % (timestamp,tagid))
			except(OSError, serial.SerialException):
					port.close()
					time.sleep(SECONDS)
					port.open()




	time.sleep(2)

	count += 1

	except KeyboardInterrupt:
			port.close()
			db.commit()
			db.close()
			print ("Program interrupted")

	return

def add_user(decision):
try:
while True:
  try:
	tagid = port.read(TOTAL_BITS)
			 print("Reading:",tagid)
	if(len(tagid) != 0) :


	  tagid = tagid.strip()
	  timestamp = time.time()

	  if (len(tagid) == STRIPPED_BITS):

		try:
			cursor.execute("INSERT INTO tagreads VALUES (?,?,?);", (timestamp, tagid, banned))

		  if (decision == ADD_USER):
			print("User Inserted at: Time:%s, Tag:%s" % (timestamp,tagid))
			GPIO.output(GREEN_LED_PIN, GPIO.HIGH)
			time.sleep(1)
			GPIO.output(GREEN_LED_PIN, GPIO.LOW)
		  else:
			print("User Banned at: Time:%s, Tag:%s" % (timestamp,tagid))
			GPIO.output(RED_LED_PIN, GPIO.HIGH)
							time.sleep(1)
			GPIO.output(RED_LED_PIN, GPIO.LOW)
		except sqlite3.IntegrityError as e:
			cursor.execute("UPDATE tagreads SET timestamp = ?, tagid = ?, ban = ?, [timestamp, tagid, decision]")
			print("User ban has been updated")
			time.sleep(1)
		finally:
			db.commit()
			tagid = ""
			break
  except(OSError, serial.SerialException):
	port.close()
	time.sleep(SECONDS)
	port.open()



	time.sleep(SECONDS)


except KeyboardInterrupt:
port.close()
db.commit()
db.close()
print ("Program interrupted")

return


def main():


while (True):
	decision = input("Would you like to add a user?: (Y/N) ")
	if decision == "Y" or decision == "y":
		decision2 = input("Would you like to ban users?: (Y/N) ")
		if decision2 == "Y" or decision2 == "y":
			print("Scan user you would like to ban.")
			add_user(BAN_USER)
		else:
			print("Scan user you would like to add.")
			add_user(ADD_USER)

	else:
		break

print("Reading RFID...")
rfid_read()

return


main()
