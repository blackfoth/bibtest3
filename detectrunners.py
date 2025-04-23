import supervision as sv
import numpy as np
from ultralytics import YOLO
from is_runner import check_bibs_within_people
import cv2
import easyocr
import re
from detect_runners import detect_runners
import psycopg2
import databasepostg as database
import random











dbconnection = None
#close_connection = db_close(connection)

#Pre for addiing the finish line to the image.
finish_line = 750
fin_start = sv.Point(0,finish_line)  
fin_end = sv.Point(1000,finish_line)



Test_Video_1 = "TTTestVideo.mp4"
trained_model= "model/best.pt"
tracker = sv.ByteTrack() #To enable tracking of objects within a video
reader = easyocr.Reader(['en'])

box_annotator = sv.BoxAnnotator()
label_annotator = sv.LabelAnnotator()
line_annotator = sv.LineZoneAnnotator(thickness=2,text_thickness=1,text_scale=0.5)

model = YOLO(trained_model, None,False)
race_runners = detect_runners()

streaming = True

#Run the prediction model on an image to find the bibs within the picture.
def predict(image):

    mask = np.zeros_like(image)

    roi_polygon = np.array([[50,50],[1000,50],[1000,800],[50,800]])

    cv2.fillPoly(mask,[roi_polygon],(255,255,255))

    masked_image = cv2.bitwise_and(image,mask)

    
    results = model(masked_image,verbose=False)[0]
    detections = sv.Detections.from_ultralytics(results)
    return detections

#Add text to the frame
def frame_annotater(frame, detections):
    labels = [f"#{tracker_id}" for tracker_id in detections.tracker_id]
    annotated_frame = box_annotator.annotate(
        scene=frame.copy(),detections=detections)
    annotated_frame = label_annotator.annotate(
        scene=annotated_frame,detections=detections,labels=labels)
    line_zone = sv.LineZone(start=fin_start,end=fin_end)
    annotated_frame = line_annotator.annotate(annotated_frame,line_zone)
    return annotated_frame

def video_callback(frame: np.ndarray):
    #Find the bibs in the frame
    detections = predict(frame)

    #Track the found detections so we only have one id
    detections = tracker.update_with_detections(detections)
    #Used to get the class names.
    data_element = detections.data
    

    #The model only detects bibs and so there is only 1 class id which is 0. This extracts the bid detection into one variable
   # bib_detections = detections[detections.class_id==0]
    #Extra chack make sure we actually found something.
    class_name = data_element.get('class_name')
    runners = find_runners(detections.class_id,detections.xyxy,detections.tracker_id)
    
    #casll here
    #finish_and_update_runner(connection,runners,frame)
    
    for runner in runners: 
        print ("Finished ",race_runners.is_finished(runner['ID']))
        if race_runners.is_finished(runner['ID']) == False:
            OCRText = ocr(frame,runner['bib'],runner['ID'])
            race_runners.add_runner(runner['ID'],OCRText)
        #print(runner['ID'],detections.tracker_id,runner['person'][3])
        
            if runner['person'][3] >= finish_line:
                finish_and_update_runner(dbconnection,runner)
    #             runner_bib = race_runners.finish_runner(runner['ID'])
    #             print(runner['ID'],"with bib ",runner_bib,"finished" )
    # #           race_runners.print_runners()

    annotated_frame = frame_annotater(frame,detections)
    return annotated_frame

    #print("THIS IS THE tracking id:",detections.tracker_id, "and it ends here.....")

def run_race_processing(raceID):
    """ Replaces start race, produces frames while processing the video feed"""
    global streaming
    race_video_file_name=""
    if int(raceID) == (1):
        race_video_file_name = Test_Video_1
    for frame in sv.get_video_frames_generator(source_path=race_video_file_name,stride=1):
        if not streaming:
            break #Stop processing the video 
        
        processed_frame = video_callback(frame=frame)
        _, buffer = cv2.imencode('.jpg',processed_frame)
        frame_bytes = buffer.tobytes()

        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n'+frame_bytes+b'\r\n')

def race_start(connection, raceID):
    global dbconnection  
    dbconnection = connection
    print(raceID)

    global streaming
    streaming = True
   # race_video_file_name = ()
   # if int(raceID) == (1):
   #     race_video_file_name = Test_Video_1
   # print(race_video_file_name)
   # sv.process_video(race_video_file_name,'annotated_video.mp4',video_callback)

def race_end(race_id):
    global streaming
    streaming = False

def find_runners(class_array,xyxy_array,tracker):
    
    #print("Pos array ",xyxy_array)
    bib_array = []
    person_array = []
    tracking_array = []
    for i in range(len(class_array)):
    # Access elements using the index
        if class_array[i] == (0):
            bib_array.append(xyxy_array[i])
        elif class_array[i] == (1):
            person_array.append(xyxy_array[i])
            tracking_array.append(tracker[i])

    #print("person coords",person_array[0][1])
    #passes check bibs with theses resurn valuse
    results = check_bibs_within_people(bib_array, person_array,tracking_array)
    return results
    

def ocr(frame,box,id):
    #crop the frame to the box where the bib is.
    x1, y1, x2, y2 = box
    cropped_frame = frame[int(y1):int(y2), int(x1):int(x2)]
    #Do some image tidying up, so it is easer to OCR
    cropped_frame = process_image(cropped_frame)
    #debug, write the image to be processed.
    #cv2.imwrite(f'image_{id}.png', cropped_frame)
    #OCR the image
    result = []
    try:
        result = reader.readtext(cropped_frame,detail=0)
    except:
        print("OCR failed on image")
    #If we get text only process numbers
    text = "".join(result)
    text = re.sub(r'[^0-9]', '', text)
    #Now add it to the id tracker so the freq can be calculated, more hits for the same value the more certain we are about the value.
    if len(text)>0:
    #     bib_ids_tracker.add_candidate(id,text)
        print(text,id)
    return text

   




def process_image(image):

    # Define the scaling factor
    scale_factor = 6.0  # Enlarge by 6x

    # Get the original dimensions
    original_height, original_width = image.shape[:2]

    # Compute new dimensions
    new_width = int(original_width * scale_factor)
    new_height = int(original_height * scale_factor)

    # Resize the image
    enlarged_image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_CUBIC)
    #Make the inage gray scale
    gray_image = cv2.cvtColor(enlarged_image, cv2.COLOR_BGR2GRAY)
    #Turn the image into BW, the threshold values determing what is black and what is white. anything below or above is either black or white. 
    _, bw_image = cv2.threshold(gray_image, 97, 230, cv2.THRESH_BINARY)
    # Sharpen the image so the edges are cleaner
    # Define a sharpening kernel
    sharpen_kernel = np.array([
        [0, -1, 0],
        [-1, 5, -1],
        [0, -1, 0]
    ], dtype=np.float32)
    sharpened_image = cv2.filter2D(bw_image, -1, sharpen_kernel)
    return sharpened_image


def finish_and_update_runner(connection,runner):
    runner_bib = race_runners.finish_runner(runner['ID'])
    print(runner['ID'],"with bib ",runner_bib,"finished" )
    race_runners.print_runners()
    results = database.get_race_participent(connection,1,runner_bib)
    print(results)
    #Check we have found the record in the database
    if (len(results) > 0):
        fName = results[0]['firstname']
        lName = results[0]['lastname']
    else:
        fName ="A"
        lName ="Unknown"
    database.add_result(connection,runner_bib,fName,lName,'2333',1)






# conn = database.db_connection()
# #results = {'BibNum':'77','firstname':'Fred','lastname':'Blogs'}
# #database.add_result(conn,results['BibNum'],results['firstname'],results['lastname'],'2333',1)

# race_start(conn,1)
# database.db_close(conn)

