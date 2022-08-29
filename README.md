# Parking Lot Car Tracker Using OpenCV

## Motivation
I got interested in Computer Vision after learning it in a class. I saw some projects in internet, counting free spaces in a parking lot using OpenCV. I thought, it could be a complete parking lot management system, if there were a tracker that tracks the location of the cars. Many people forget the location of their car after parking in a public parking lot and spends time to find their car. But using the car location provided by the tracker, the owner of the car can check easily the location of his/her car. The computer vision based parking lot management system can also reduce the cost needed for making a parking lot. Because it doesn't need any sensors which were used to determine the availability of the parking space. It's also appliable to the small parking lots. Because this parking lot management system only needs a video recorded by a CCTV. This parking lot car tracker is a subproject of the parking lot management system.

## Overview
<img src="https://user-images.githubusercontent.com/62208537/187294376-8e58eea1-ab91-48d1-9b05-a12e83afafa9.png" width="800" height="400"/>
Program flow is as follows: 
<li> User inputs the video and encodes the location of the entrance.
<li> the program tracks the car which went through the entrance(it doesn't track the already existing cars).

## How it works
First we have to threshold the video. Exactly each frame of the video. <br>
We will use this codes.
```
object_detector = cv2.createBackgroundSubtractorMOG2(history=150, varThreshold=20)
```
```
_, frameThres = cv2.threshold(mask, 254, 255, cv2.THRESH_BINARY_INV)
```
The result is <br>
 <img src="https://user-images.githubusercontent.com/62208537/187294781-d06215cd-723d-43a8-9c6d-49e43f07a4b2.png" width="800" height="400"/>
 <br>
If there are enough contours in the entrace we will assume that there is a new car comming to the parking lot and make a new car class.
Detected cars are stored as an car object. 
```
class Car:
  def __init__(self, id,cx,cy):
      self.id_count = id
      self.enter_time = None
      self.exit_time = None
      self.path = [(cx,cy)]
```
 After the deteciton, the program will keep tracking the car. To implement this function, we'll search frame by frame the fields around the center of the car location and check if a new object is detected. If the distance between the new object and the car is enough clode, we assume the car moved to the location during one frame and the location will be appended it to the self.path.
```
 # distance between cars and new detected object
 dist = math.hypot(cx - car.path[-1][0],cy - car.path[-1][1])
 # if distance < 10it is the same object
     if dist < 10:
     # append the new location to the path
          fake_db[key].path.append((cx,cy))
          same_object_detected = True
          break
```
The last step is drawing the location of the car. 
 ```
 cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
 ```
 
 ## Future Work
 <li> The thresholding could be in a better way. Because the object in a thresholded frame disappears sometimes when it stops.
 <li> The tracking of the cars could be more efficient by calculating the distance between the center coordinate of a car and other objects. Not using a 'field',
