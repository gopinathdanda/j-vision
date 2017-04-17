import face_recognition
from PIL import Image, ImageDraw
import operator
import math

def get_circle_points(center, radius, points=10):
    return [(math.cos(2*math.pi/points*x)*radius+center[0],math.sin(2*math.pi/points*x)*radius+center[1]) for x in xrange(0,points+1)]

def get_frac_point(a, b, k):
    x = tuple(map(operator.sub, a, b))
    y = tuple(map(operator.mul, x, (k,k)))
    return tuple(map(operator.add, y, b))
    #return tuple(map(operator.div, tuple(map(operator.add, a, b)), (2,2)))

def get_eye_coord(a):
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
    return math.hypot(p2[0]-p1[0], p2[1]-p1[1])

# Load a sample picture and learn how to recognize it.
image = face_recognition.load_image_file("images/shreya_eyes.jpeg")
face_landmark_list = face_recognition.face_landmarks(image)

for landmark in face_landmark_list:
    pil_image = Image.fromarray(image)
    d = ImageDraw.Draw(pil_image, 'RGBA')
    
    d.polygon(landmark['left_eye'], fill = (255,255,255,255))
    d.polygon(landmark['right_eye'], fill = (255,255,255,255))
    
    eyeL = get_circle_points(get_eye_center(landmark['left_eye']), get_eye_radius(landmark['left_eye']))
    eyeR = get_circle_points(get_eye_center(landmark['right_eye']), get_eye_radius(landmark['right_eye']))
    #eyeL = get_eye_coord(landmark['left_eye'])
    #eyeR = get_eye_coord(landmark['right_eye'])
    
    #print eye
    d.polygon(eyeL, fill = (0,0,0,255))
    d.polygon(eyeR, fill = (0,0,0,255))
    
    pil_image.show()

