# import os
import smtplib
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email import encoders

MAIL_SENDER = 'chayan.mazumder@ihsmarkit.com'
to_addr = "chayan.mazumder@ihsmarkit.com"
email_to_list = ["chayan.mazumder@ihsmarkit.com"]


class TestMail(object):
    def __init__(self):
        pass

    def send_mail(self, date, ttname, attachment=None, fname='attachment.txt'):
        # receiver should a list of receiver(s)
        # subject and msg_body can be string format
        global to_addr, email_to_list
        email_msg = MIMEMultipart()
        email_msg['Subject'] = "Status | Test Demo | {}".format(str(date))
        email_msg['To'] = to_addr
        email_msg['From'] = MAIL_SENDER
        text = self.compose_email(ticketn=ttname)
        part = MIMEText(text, 'html')
        email_msg.attach(part)

        """part = MIMEBase('application', "octet-stream")
        part.set_payload(open(attachment, "rb").read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename')"""

        """part = MIMEApplication(open(attachment).read())
        part.add_header('Content-Disposition',
                        'attachment; filename=fname')
        email_msg.attach(part) """

        # email_msg.attach(part)

        """if attachment:
            if filename.endswith('txt'):
                email_attachment = MIMEText(attachment)
            else:
                # fp = open(filename, "rb")
                #email_attachment = MIMEBase('application', 'octet-stream')
                # email_attachment.set_payload(fp.read())
                email_attachment = MIMEText(attachment)
            email_attachment.add_header('Content-Disposition',
                                        'attachment',
                                        filename=os.path.basename(filename))
            email_msg.attach(email_attachment)"""
        # email_msg.attach(MIMEText("test email", 'html'))
        smtp = smtplib.SMTP('uksmtp.markit.partners')
        smtp.sendmail(MAIL_SENDER, email_to_list, email_msg.as_string())
        smtp.quit()
        return "run_send"

    def compose_email(self, ticketn):
        email_body = """<html> <head></head>
        <body> <basefont face="calibri" size="3" color="Black"> <p>Hi,<br><br>Test run for
          <b>{0}</b>""".format(ticketn)
        signature = """
                       <p>Regards,\n<br>Chayan</p><p><font size="2">This is an auto generated email.
                       Please contact chayan.mazumder@ihsmarkit.com for further information</font></p>
                    </body>
                </html>"""

        email_body += signature
        return email_body


if __name__ == "__main__":
    path = r"C:\Users\chayan.mazumder\Desktop\CompareResult2\CompareFpML_Result.xlsx"

    from datetime import datetime

    currDateTime = datetime.now()
    sub_date = format(currDateTime.strftime('%d%b%Y'))
    filename = "CompareFpML_Result.xlsx"
    ticketname = "TradeSTP CitiPB bulk replay"
    Test = TestMail.send_mail(sub_date, path, ticketname, filename, ticketname)
