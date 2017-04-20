import cv2
import sys
import time
import XML

OBJECT_TYPE='blue'

class preprocess_video:
    def __init__(self):
        self.xmin=0
        self.xmax=0
        self.ymin=0
        self.ymax=0
        self.draw=0
        self.can_store=0

        self.file_name=0

        self.time=0

        self.xml=XML.XML()
    def get_object(self,event,x,y,flags,param):
        if event==cv2.EVENT_LBUTTONDOWN:
            self.xmin=x
            self.ymin=y
            self.draw=1
            self.can_store=0
            print "down"
        t=time.time()-self.time
        if event==cv2.EVENT_MOUSEMOVE and self.draw==1 and t >0.05:
            self.time=time.time()
            self.image=self.frame.copy()
            '''t=time.time()
            print time.time()-t'''
            cv2.rectangle(self.image,(self.xmin,self.ymin),(x,y),(0,255,0),3,8,0)
            cv2.imshow("frame",self.image)
            cv2.waitKey(2)
            #cv2.imshow("frame2",self.frame)
            #cv2.waitKey(10)
        if event==cv2.EVENT_LBUTTONUP:
            self.xmax=x
            self.ymax=y
            self.draw=0
            self.roi=self.image[self.xmin:self.xmax,self.ymin:self.ymax]
            self.can_store=1
            print "up"

    def __init_rcctangle(self):
        self.xmin=0
        self.xmax=0
        self.ymin=0
        self.ymax=0
        self.draw=0
        self.can_store=0

    def store_roi_xml(self,count,object_type):

        self.xml.insert_object(object_type,[self.xmin,self.ymin,self.xmax,self.ymax])

    def roi(self,video_path):
        cap=cv2.VideoCapture(video_path)
        while(cap.isOpened()):
            ret,frame=cap.read()
            self.image=frame.copy()
            self.frame=frame
            cv2.namedWindow("frame")
            cv2.imshow("frame",self.image)
            cv2.setMouseCallback("frame",self.get_object)
            count=0
            print frame.shape
            self.file_name=self.file_name+1
            self.xml.creat_tree("data",str(self.file_name),frame.shape)
            while(1):
                c=cv2.waitKey(2)&0xFF
                if c==ord('s') and self.can_store==1: #store
                    count=count+1
                    self.store_roi_xml(count,OBJECT_TYPE)
                    self.image=self.frame
                    self.__init_rcctangle()
                    cv2.imshow("frame",self.image)
                if c==ord('r'):   #redo
                    self.__init_rcctangle()
                    self.image=self.frame
                    cv2.imshow("frame",self.image)

                if c==ord('n'): #next
                    self.__init_rcctangle()
                    break

                if c==ord(' '): #store and next
                    if self.can_store==1:
                        count=count+1
                        self.store_roi_xml(count,OBJECT_TYPE)
                    self.__init_rcctangle()
                    break
            self.xml.close("xml/")
            cv2.imwrite('images/'+str(self.file_name)+".jpg",self.frame)

if __name__=='__main__':
    sys.setrecursionlimit(1000000)
    VIDEO_PATH="./data/blueface-ev-0.MOV"
    print "begin"
    pv=preprocess_video()
    pv.roi(VIDEO_PATH)
