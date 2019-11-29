import serial
import time
import sqlite3
import RPi.GPIO as GPIO

GREEN_LED = 6
RED_LED = 5
BUZZER = 25
GPIO.setmode(GPIO.BCM)
GPIO.setup(GREEN_LED, GPIO.OUT)
GPIO.setup(RED_LED, GPIO.OUT)
GPIO.setup(BUZZER, GPIO.OUT)

# open sqlite database file
db = sqlite3.connect('tagreads.db')
cursor = db.cursor()

# check that the correct tables exists in database; create them if they do not
tables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND $
if len(tables) == 0 :
  cursor.execute("CREATE table tagreads (timestamp, tagid text PRIMARY KEY, ban$

# connect to serial port on which the RFID reader is attached
port = serial.Serial('/dev/ttyAMA0', 2400, timeout=1)

def rfid():

  count = 0
  try:
    while count < 100000:
      # attempt to read in a tag
      try:
        tagid = port.read(12)
          # if tag read success full, save it to database and wait half a secon$
        # else try again
        if(len(tagid) != 0):


          tagid = tagid.strip()
          timestamp = time.time()
          if (len(tagid) == 10):
            cursor.execute("SELECT banned from tagreads WHERE tagid = ?",[tagid$
            row = cursor.fetchall()
			if (len(row) == 0):
              print("Security Alert! Unauthorized access attempt!")
              GPIO.output(BUZZER, GPIO.HIGH)
              GPIO.output(RED_LED, GPIO.HIGH)
              time.sleep(1)
              GPIO.output(RED_LED, GPIO.LOW)
              GPIO.output(BUZZER, GPIO.LOW)
            else:
              tup = row[0]
			  num = tup[0]
			  print(num)
              if (num == 1):
                print("Security Alert! User is banned!")
                GPIO.output(RED_LED, GPIO.HIGH)
                GPIO.output(BUZZER, GPIO.HIGH)
                time.sleep(.5)
                GPIO.output(BUZZER, GPIO.LOW)
                GPIO.output(RED_LED, GPIO.LOW)
                time.sleep(.2)
                GPIO.output(RED_LED, GPIO.HIGH)
				 GPIO.output(BUZZER, GPIO.HIGH)
                time.sleep(.2)
                GPIO.output(RED_LED, GPIO.LOW)
                GPIO.output(BUZZER, GPIO.LOW)
              else:
                print("Welcome!")
                GPIO.output(GREEN_LED, GPIO.HIGH)
                time.sleep(1)
                GPIO.output(GREEN_LED, GPIO.LOW)
            print("Time:%s, Tag:%s" % (timestamp,tagid))
		except(OSError, serial.SerialException):
			port.close()
			time.sleep(2)
			port.open()




        time.sleep(2)

	count += 1

	except KeyboardInterrupt:
		port.close()
		db.commit()
		db.close()
		print ("Program interrupted")

	return
	
def add(decision):
  #lastid = ""
  #count = 0
  try:
    while True:
      # attempt to read in a tag
      try:
        tagid = port.read(12)
        # if tag read success full, save it to database and wait half a second;
        # else try again
		 print("Reading:",tagid)
        if(len(tagid) != 0) :


          tagid = tagid.strip()
          timestamp = time.time()

          if (len(tagid) == 10):

            try:
				cursor.execute("INSERT INTO tagreads VALUES (?,?,?);", (timestamp$

              if (decision == 0):
                print("User Inserted at: Time:%s, Tag:%s" % (timestamp,tagid))
                GPIO.output(GREEN_LED, GPIO.HIGH)
                time.sleep(1)
                GPIO.output(GREEN_LED, GPIO.LOW)
              else:
                print("User Banned at: Time:%s, Tag:%s" % (timestamp,tagid))
                GPIO.output(RED_LED, GPIO.HIGH)
				time.sleep(1)
                GPIO.output(RED_LED, GPIO.LOW)
            except sqlite3.IntegrityError as e:
                cursor.execute("UPDATE tagreads SET timestamp = ?, tagid = ?, ban$
                print("User ban has been updated")
                time.sleep(1)
            finally:
				db.commit()
				#lastid = tagid
				tagid = ""
				break
      except(OSError, serial.SerialException):
        port.close()
        time.sleep(2)
        port.open()



        time.sleep(2)

		#lastid = tagid
    #count += 1

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
        add(1)
      else:
        print("Scan user you would like to add.")
        add(0)

    else:
      break

	print("Reading RFID...")
	rfid()

	return


main()


