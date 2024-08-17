import cv2
import threading
import queue
import time

# Setup the queue for thread-safe communication
frame_queue = queue.Queue()

classNames = []
classFile = "Object_Detection_Files/coco.names"
with open(classFile, "rt") as f:
    classNames = f.read().rstrip("\n").split("\n")

configPath = "Object_Detection_Files/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"
weightsPath = "Object_Detection_Files/frozen_inference_graph.pb"

net = cv2.dnn_DetectionModel(weightsPath, configPath)
net.setInputSize(320, 320)
net.setInputScale(1.0 / 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)

move = 0

def detectObject(frame_queue):
    count = 0
    global move
    cap = cv2.VideoCapture(0)

    
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        exit()
        
    while True:
        ret, img = cap.read()
        if not ret:
            print("Error: Could not read frame from webcam.")
            break
        
        result, objectInfo, boxList = getObjects(img, 0.45, 0.2, objects=['cell phone'])
        # print(len(boxList))

        for i, inner_list in enumerate(boxList):
            # print(f"Length of inner list {i + 1}:", len(inner_list))


            if(len(inner_list) == 4):
                count = count + 1
                area = (boxList[0][0] - boxList[0][2]) * (boxList[0][1] - boxList[0][3])
                # print(area)

                if area < 1000 and count == 30:
                    print(area)
                    move = 1
                    count = 0
                if area > 1000 and count == 30:
                    print(area)
                    move = 2
                    count = 0
                    
        # Pass the processed frame to the queue
        frame_queue.put(img)

    cap.release()

def move_rover():
    global move
    while True:
        if(move == 1):
            print("[Rover] Moving towards detected cellphone...")
            time.sleep(2)
        elif(move == 2):
            print("[Rover] Adjusting position...")
            time.sleep(2)
        else:
            print("[Rover] Stopping...")
            time.sleep(2)

def getObjects(img, thres, nms, draw=True, objects=[]):
    classIds, confs, bbox = net.detect(img, confThreshold=thres, nmsThreshold=nms)
    if len(objects) == 0: objects = classNames
    objectInfo = []
    boxList = []
    if len(classIds) != 0:
        for classId, confidence, box in zip(classIds.flatten(), confs.flatten(), bbox):
            className = classNames[classId - 1]
            if className in objects:
                objectInfo.append([box, className])
                boxList.append([box[0], box[1], box[2], box[3]])
                if draw:
                    cv2.rectangle(img, box, color=(0, 255, 0), thickness=2)
                    cv2.putText(img, classNames[classId - 1].upper(), (box[0] + 10, box[1] + 30),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
                    cv2.putText(img, str(round(confidence * 100, 2)), (box[0] + 200, box[1] + 30),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

    return img, objectInfo, boxList

if __name__ == "__main__":
    camera_thread = threading.Thread(target=detectObject, args=(frame_queue,))
    rover_thread = threading.Thread(target=move_rover)
    camera_thread.start()
    rover_thread.start()



    while True:
        if not frame_queue.empty():
            img = frame_queue.get()
            cv2.imshow("Output", img)
        
        if cv2.waitKey(1) == 27:  # Esc key to stop
            break

    camera_thread.join()
    rover_thread.join()

    cv2.destroyAllWindows()

    
