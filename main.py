#Final
import imutils
from tkinter import *
from PIL import ImageTk, Image
from urllib.request import urlopen
import numpy as np
import cv2
import os
from tkinter.filedialog import askopenfilename

def ipdet():
    global ip_entry, port_entry, ipdet_root
    ipdet_root = Tk()
    IMAGE_PATH = 'Adobe XD Python\\Ipcamdet.png'

    ipdet_canvas = Canvas(ipdet_root, width=1300, height=800, bd=0, highlightthickness=0)
    ipdet_canvas.pack(fill="both", expand=True)

    ipdet_img = ImageTk.PhotoImage(Image.open(IMAGE_PATH).resize((1300, 800), Image.ANTIALIAS))
    ipdet_canvas.background = ipdet_img
    ipdet_canvas.create_image(0, 0, anchor=NW, image=ipdet_img)

    ip_entry = Entry(ipdet_root, font="Helvetica 11", width=24, bd=0, fg="#F7DC5F", background="#222233")

    port_entry = Entry(ipdet_root, font="Helvetica 11", width=24, bd=0, fg="#F7DC5F", background="#222233")

    camprocedbttn = Button(ipdet_root, text="Proceed", height=1, width=10, bd=0, fg="#F7DC5F", background="#222233",
                           command=cam)

    prerecbttn = Button(ipdet_root, text="Pick A File", height=1, width=10, bd=0, fg="#F7DC5F", background="#222233",
                           command=detectByPathVideo)


    # Adding to Frame

    ip_window = ipdet_canvas.create_window(520, 280, anchor="nw", window=ip_entry)

    port_window = ipdet_canvas.create_window(520, 370, anchor="nw", window=port_entry)

    camprocedbttn_window = ipdet_canvas.create_window(582, 483, anchor="nw", window=camprocedbttn)

    prerecbttn_window = ipdet_canvas.create_window(582, 550, anchor="nw", window=prerecbttn)

    ipdet_root.geometry("1300x800")

    mainloop()

def detect(frame):
    bounding_box_cordinates, weights =  HOGCV.detectMultiScale(frame, winStride = (4, 4), padding = (8, 8), scale = 1.03)
    
    person = 1
    for x,y,w,h in bounding_box_cordinates:
        cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 4)
        cv2.putText(frame, f'person {person}', (x,y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1)
        person += 1
    
    cv2.putText(frame, 'Status : Detecting ', (40,40), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255,0,0), 2)
    cv2.putText(frame, f'Total Persons : {person-1}', (40,70), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255,0,0), 2)
    cv2.imshow('output', frame)

    return frame

def cam():
    ip = ip_entry.get()
    port = port_entry.get()

    if (ip_entry.index("end") and port_entry.index("end") != 0):
        # slap = 'http://'+ip+':'+port
        # print(slap)

        # Pc Cam
        # cap = cv2.VideoCapture(0)
        try:
            cap = 'http://' + ip + ':' + port + '/shot.jpg'

            print(cap)
        except:
            pass
        else:
            pass

        cv2.startWindowThread()
        while 1:
            imgresp = urlopen(cap)
            imgNP = np.array(bytearray(imgresp.read()), dtype=np.uint8)
            img = cv2.imdecode(imgNP, -1)
            img = cv2.resize(img, (600, 400))

            result_image = detect(img)
            
            # cv2.imshow('img', img)



            if ord('q') == cv2.waitKey(10):
                # sys.exit()
                cv2.destroyWindow('img')
                cv2.waitKey(1)
                break
            k = cv2.waitKey(30) & 0xff
            if k == 27:
                break

    else:
        print("Nope")

def detectByPathVideo():
    path = askopenfilename()
    # print(filename)
    
    video = cv2.VideoCapture(path)
    check, frame = video.read()
    if check == False:
        print('Video Not Found. Please Enter a Valid Path (Full path of Video Should be Provided).')
        return

    print('Detecting people...')
    while video.isOpened():
        #check is True if reading was successful 
        check, frame =  video.read()

        if check:
            frame = imutils.resize(frame , width=min(800,frame.shape[1]))
            frame = detect(frame)
            
            # if writer is not None:
            #     writer.write(frame)
            
            key = cv2.waitKey(1)
            if key== ord('q'):
                break
        else:
            break
    video.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    HOGCV = cv2.HOGDescriptor()
    HOGCV.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())


ipdet()