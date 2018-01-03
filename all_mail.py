import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage
import os 
import cv2
import random


# capture image 
def take_image():
    cap = cv2.VideoCapture(0)

    while(True):
        ret, frame = cap.read()
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)

        cv2.imshow('frame', rgb)

        # generating random name for the file
        random_num = random.randrange(10**8)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            file_name = "img_"+str(random_num)

            # proving path to the images
            out = cv2.imwrite('images/'+file_name+'.jpg', frame)
            break

    cap.release()
    cv2.destroyAllWindows()
    send_mail()

def send_mail():
    # image directory path or directory name
	path='images'
	os.chdir(path)

    # It return list of all store file in assending order
	files=sorted(os.listdir(os.getcwd()),key=os.path.getmtime)

    # if [0] return oldest file if [-1] return latest file
	newest=files[-1]
# sender's email address
	fromaddr = "indiamagicmirror@gmail.com"
    #receiver's email address 
	toaddr = raw_input("enter sender's mail:")
# subject here
	msgRoot=MIMEMultipart()
	msgRoot['Subject']=raw_input("enter your Subject::")
	msgRoot['From'] = fromaddr
	msgRoot['To'] = toaddr

# body here 	 
	body = raw_input("enter your text::")
	msgRoot.attach(MIMEText(body, 'plain'))

	fp = open(newest, 'rb')
	msgImage = MIMEImage(fp.read())
	fp.close()


	msgImage.add_header('Content-ID', '<image1>')
	msgRoot.attach(msgImage)
	 
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login(fromaddr, "Prd*7891")
	text = msgRoot.as_string()
	server.sendmail(fromaddr, toaddr, text)
	server.quit()


if __name__ == '__main__':
	take_image()