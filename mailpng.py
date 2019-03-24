import smtplib 
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders
from time import time
   
fromaddr = "george.lou@nemoinfo.com"

def mailpng(fname, toaddr = "mice2100@qq.com"):
    msg = MIMEMultipart() 
    msg['From'] = fromaddr 
    msg['To'] = toaddr 
    
    msg['Subject'] = "screen shot"
    
    body = "this is body"
    msg.attach(MIMEText(body, 'plain')) 
    
    attachment = open(fname, "rb") 
    
    p = MIMEBase('application', 'octet-stream') 
    p.set_payload((attachment).read()) 
    encoders.encode_base64(p) 
    
    p.add_header('Content-Disposition', "attachment; filename= %s" % fname) 
    
    msg.attach(p) 
    
    s = smtplib.SMTP('smtp.exmail.qq.com', 587) 
    
    # start TLS for security 
    s.starttls() 
    
    # Authentication 
    s.login(fromaddr, "Monitor01") 
    
    # Converts the Multipart msg into a string 
    text = msg.as_string() 
    
    # sending the mail 
    s.sendmail(fromaddr, toaddr, text) 
    
    # terminating the session 
    s.quit()

if __name__ == "__main__":
    mailpng("screenshot.png")