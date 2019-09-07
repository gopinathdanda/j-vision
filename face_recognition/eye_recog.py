import face_recognition, math, operator, cv2, argparse
from PIL import Image, ImageDraw
import numpy as np

def get_frac_point(a, b, k):
    x = tuple(map(operator.sub, a, b))
    y = tuple(map(operator.mul, x, (k,k)))
    return tuple(map(operator.add, y, b))
    #return tuple(map(operator.div, tuple(map(operator.add, a, b)), (2,2)))

def get_eye_rec_coord(a):
    k_l_t_mid = get_frac_point(a[1], a[2], 0.5)
    k_l_b_mid = get_frac_point(a[4], a[5], 0.5)
    k_l_mid = get_frac_point(a[0], a[3], 0.5)
    k_l_mid_l = get_frac_point(a[0], k_l_mid, 0.33)
    k_l_mid_r = get_frac_point(k_l_mid, a[3], 0.66)
    return [k_l_t_mid, k_l_mid_r, k_l_b_mid, k_l_mid_l]

def get_eye_center(eye):
    return get_frac_point(get_frac_point(eye[1], eye[2], 0.5), get_frac_point(eye[5], eye[4], 0.5), 0.5)
    
def get_eye_radius(eye):
    p1 = get_frac_point(eye[1], eye[2], 0.5)
    p2 = get_frac_point(eye[4], eye[5], 0.5)
    return math.hypot(p2[0]-p1[0], p2[1]-p1[1])*0.8

def get_circle_points(center, radius, points=10):
    return [(math.cos(2*math.pi/points*x)*radius+center[0],math.sin(2*math.pi/points*x)*radius+center[1]) for x in range(0,points+1)]

def get_eye_circ_coord(a):
    return get_circle_points(get_eye_center(a), get_eye_radius(a))

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", help="If image based, path to image")
args = vars(ap.parse_args())

if not args.get("image", True):
    process_this_frame = True
    
    # Get a reference to webcam #0 (the default one)
    video_capture = cv2.VideoCapture(0)
    
    while True:
        ret, frame = video_capture.read()
        
        small_frame = cv2.resize(frame, (0,0), fx=0.25, fy=0.25)
        
        face_landmark_list = face_recognition.face_landmarks(small_frame)
        
        for landmark in face_landmark_list:
            cv2.fillPoly(small_frame, np.array([landmark['left_eye']]), (255,255,255))
            cv2.fillPoly(small_frame, np.array([landmark['right_eye']]), (255,255,255))
            cv2.fillPoly(small_frame, np.array([get_eye_circ_coord(landmark['left_eye'])], dtype=np.int32), (0,0,0))
            cv2.fillPoly(small_frame, np.array([get_eye_circ_coord(landmark['right_eye'])], dtype=np.int32), (0,0,0))
        
        cv2.imshow("Video", small_frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    video_capture.release()
    cv2.destroyAllWindows()

else:
    # Load a sample picture and learn how to recognize it.
    image = face_recognition.load_image_file(args.get("image"))
    face_landmark_list = face_recognition.face_landmarks(image)

    for landmark in face_landmark_list:
        pil_image = Image.fromarray(image)
        d = ImageDraw.Draw(pil_image, 'RGBA')
    
        d.polygon(landmark['left_eye'], fill = (255,255,255,255))
        d.polygon(landmark['right_eye'], fill = (255,255,255,255))
    
        eyeL = get_eye_circ_coord(landmark['left_eye'])
        eyeR = get_eye_circ_coord(landmark['right_eye'])
        #eyeL = get_eye_coord(landmark['left_eye'])
        #eyeR = get_eye_coord(landmark['right_eye'])
    
        #print eye
        d.polygon(eyeL, fill = (0,0,0,255))
        d.polygon(eyeR, fill = (0,0,0,255))
    
        pil_image.show()

