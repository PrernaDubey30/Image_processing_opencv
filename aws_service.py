import cv2
import boto3

image_path= "./img2.png"

def get_image(imgpath):
    with open(imgpath,"rb") as img:
        return img.read()
    
# image=get_image(image_path)
# print(image)

def celeb_detection(imgpath):
    image_contain= get_image(imgpath)
    image=cv2.imread(imgpath)
    width,height=image.shape[1],image.shape[0]
    print("processing start....")

    client=boto3.client("rekognition")
    response= client.recognize_celebrities(Image={"Bytes":image_contain})
    print("building the box...")


    for labels in response["CelebrityFaces"]:                                          #box on image
        name=labels["Name"]
        face=labels["Face"]["BoundingBox"]
        x=int(face["Left"]*width)
        y=int(face["Top"]*height)
        w=int(face["Width"]*width)
        h=int(face["Height"]*height)

        cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,255),2)
        cv2.putText(image,name,(x,y-5),cv2.FONT_HERSHEY_COMPLEX,0.5,[255,0,0],2)
    return image
    

result=celeb_detection(image_path)
while True:
    cv2.imshow("Result",result)
    if cv2.waitKey(1) == ord("q"):
        break

