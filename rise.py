# import the opencv library 
import cv2 
import numpy as np
import matplotlib.pyplot as plt
import datetime

  
#now try to get the depth of each point.
 
# define a video capture object 
vid = cv2.VideoCapture(1) 
  
#import face cascade and eye cascade (classifier using visual cues)
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

#counter for the filenames when taking screenshot
numSnaps = 1


def canny_edge_detection(frame):
    #convert to grayscale for edge detect
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #apply gaussian blur to reduce noice n smoothe dges
    blurred = cv2.GaussianBlur(src=gray, ksize=(3,5), sigmaX=0.5)

    #perform canny edge detection
    oldEdge = cv2.Canny(blurred, 70, 135)
    #had to rotate
    rotatedEdge = cv2.rotate(oldEdge, cv2.ROTATE_90_COUNTERCLOCKWISE)
    #have to flip
    edges = cv2.flip(rotatedEdge, 0)

    return blurred, edges


while(vid.isOpened()): 
      
    # Capture the video frame 
    # by frame 
    ret, frame = vid.read() 
    #ret: boolean, return true if frame is available
    #frame: img array vector, stores values of respective pxls of vid    
    
    #dimensions of the frame
    frameH, frameW = frame.shape[:2]

    #create new window to display the plots without the video frames
    whiteImg = np.ones((frameH, frameW, 3), dtype = np.uint8)
    whiteImg = 255*whiteImg


    if not ret:
        print("Image not captured")
        break

    """FOR EDGE DETECTION"""    
    
    blurred, edges = canny_edge_detection(frame)

    #use numpy to grab coordinates having value > 0 (meaning an adge value)
    indices = np.where(edges != [0])
    #zip and list func to get a list of tuples containing said points
    edgeCoordinates = list(zip(indices[0], indices[1]))
    
    
    #now print the circles to map the points
    for edge in edgeCoordinates[::40]: 
        #print(edge)
        cv2.circle(frame, tuple(edge), 6, (0, 255, 1), 1)   
    
    #for plotted edges window
    for edge in edgeCoordinates[::50]: #100 is best
        cv2.circle(whiteImg, tuple(edge), 8, (0, 255, 1), -1)
   
    """FOR COUNTOUR DETECTION(Finding number of obj in frame)"""
    CGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    CBlur = cv2.GaussianBlur(CGray, (11,11), 0)
    CCanny = cv2.Canny(CBlur, 30, 150, 3)
    CDilated = cv2.dilate(CCanny, (1,1), iterations=0)

    (cnt, hierarchy) = cv2.findContours(CDilated.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    #print text to the frame
    cv2.putText(frame, "# of objects detected: " + str(len(cnt)), (10, frameH - 20), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0,0,255), 2, cv2.LINE_AA)
    
    #print out number of objects
    print(len(cnt))

    """FOR COLOR DETECTION"""
    
    into_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    #changing color format from BGR to HSV, used to create the mask
    L_limit = np.array([98,50,50]) #setting blue lower limit [98,50,50]
    U_limit = np.array([139,255,255]) #setting blue upper limit [139,255,255]

    b_mask = cv2.inRange(into_hsv, L_limit, U_limit)
    #creating the mask
    #pixels falling in the range will turn white and the rest black.
    blue = cv2.bitwise_and(frame, frame, mask=b_mask)
    #give color to the mask
    

 
    """FOR FACE DETECTION"""
    
    #convert to greyscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #detect faces of different sizes in the input img
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    #date and time text and output
    datet = str(datetime.datetime.now())
    cv2.putText(frame, datet, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2, cv2.LINE_AA)


    
    for (x,y,w,h) in faces:
        #draw rectangle around the face
        image = cv2.rectangle(frame, (x,y), (x+w, y+h), (255, 255, 0), 2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
        
        #blur the face
        image[y:y+h, x:x+w] = cv2.medianBlur(image[y:y+h, x:x+w], 35)
        

        
        #detect eyes of different sizes in the input img
        eyes = eye_cascade.detectMultiScale(roi_gray)

        #draw rectangle in the eyes
        for (ex, ey, ew, eh) in eyes:
            cv2.putText(frame, "Eyes", (ex, ey - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
            cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0,127,255), 2)
            print(eyes)
        #output text label into the face rectangle
        cv2.putText(frame, "Him", (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)    
    
                

    #print(frame)
    

    #display the ploted edges window
    cv2.imshow("plot", whiteImg)

    #display the masked image
    #cv2.imshow('BLUE DETECTOR', blue)

    # Display the resulting frame 
    cv2.imshow('frame', frame) 
    

    #holder for key press
    keyPress = cv2.waitKey(1) & 0xFF

    #take snapshot of frame
    #better yet display a separatewindow of the frame
    if keyPress  == ord('s'):
        cv2.imwrite(f"snapshot{numSnaps}.jpg", frame)
        numSnaps += 1

    #take snapshot of the plotted edges in white background
    if keyPress == ord('p'):
        cv2.imwrite(f"plottedSnap{numSnaps}.jpg", whiteImg)
        numSnaps += 1

  
    # the 'q' button is set as the 
    # quitting button you may use any 
    # desired button of your choice 
    if keyPress == ord('q'): 
        break


# After the loop release the cap object 
vid.release() 
# Destroy all the windows 
cv2.destroyAllWindows() 
