import cv2
import math

# Read video
cap = cv2.VideoCapture("parking_video.mp4")

# Location of entrance
ent = [(963, 13), (995, 31)]

# db to store cares
fake_db = {}

# lists for new detected objects
new_objects = []

# Number of the cars
car_num = 0

# Object detector for thrasholding
object_detector = cv2.createBackgroundSubtractorMOG2(history=150, varThreshold=20)

# Car Object, includes number plate, enter time, exit time, path
class Car:
    def __init__(self, id,cx,cy):
        self.id_count = id
        self.enter_time = None
        self.exit_time = None
        self.path = [(cx,cy)]

# Update the car position in the entrance
def update(objects):
    global car_num
    for obj in objects:
        x,y,w,h,cx,cy = obj
        same_object_detected = False
        for key in fake_db.keys():
            car = fake_db[key]
            # distance between cars and new detected object
            dist = math.hypot(cx - car.path[-1][0],cy - car.path[-1][1])
            # if distance < 10it is the same object
            if dist < 10:
                # append the new location to the path
                fake_db[key].path.append((cx,cy))
                same_object_detected = True
                break
        # else make a new object in fake_db
        if same_object_detected is False:
            fake_db[car_num] = Car(car_num,cx,cy)
            car_num += 1

# check if the object is in the fields
def is_in(cx,cy,fields):
    flag = False
    for field in fields:
        if field[0] <= cx <= field[1] and field[2] <= cy <= field[3]: flag = True
        if flag: break
    return flag


while True:
    # Read frame from video
    ret, frame = cap.read()

    # Thresholding
    mask = object_detector.apply(frame)
    _, frameThres = cv2.threshold(mask, 254, 255, cv2.THRESH_BINARY_INV)

    entrance = frameThres[13:31, 963:995]

    # Draw a rectangle and write number of pixels
    cv2.rectangle(frame, ent[0], ent[1], (255, 0, 0), 1)

    # Extract contours
    contours, _ = cv2.findContours(frameThres, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Make fields, where already existing cars are located
    fields = []
    for key in fake_db.keys():
        car = fake_db[key]
        cx, cy = car.path[-1]
        fields.append([cx - 30, cx + 30, cy - 30, cy + 30])

    # Tracking the objects
    for cnt in contours:
        # if there are enough contours
        if cv2.contourArea(cnt) > 200:
            # make a rectangle, x,y,width,height
            x, y, w, h = cv2.boundingRect(cnt)
            # get the center coordinate of the rectangle
            cx = (x + x + w) // 2
            cy = (y + y + h) // 2
            # check if the center coordinate is in the fields
            # i.e. if the new detected rectangle is an already existing car
            if is_in(cx, cy, fields):
                # if the object was an already existing car, search which car is it.
                for key in fake_db.keys():
                    car = fake_db[key]
                    dist = math.hypot(cx - car.path[-1][0], cy - car.path[-1][1])
                    # if distance < 20, it is the same object
                    if dist < 20:
                        fake_db[key].path.append((cx, cy))
                        break
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
    fields = []

    # Check if there is a new object in entrance
    for cnt in contours:
        if cv2.contourArea(cnt) > 200:
            x, y, w, h = cv2.boundingRect(cnt)
            cx = (x + x + w) // 2
            cy = (y + y + h) // 2
            if 963 <= cx <= 995 and 13 <= cy <= 31:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
                new_objects.append([x, y, w, h, cx, cy])

    # Filter the new objects
    update(new_objects)

    # Make the new_object empty
    new_object = []

    # Show the frames
    cv2.imshow("Frame", frame)
    cv2.imshow("imgThres", frameThres)
    cv2.imshow("entrance",entrance)

    key = cv2.waitKey(50)
    if key == ord('r'):
        pass
