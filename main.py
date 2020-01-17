import smtplib
from email.mime.text import MIMEText
import imaplib
import poplib

def utf8(string):
    return str(string,'utf-8')

def smtp_protocol():
    server = smtplib.SMTP_SSL('smtp.mail.yahoo.com',465)
    print("Enter the Sender's email address")
    from_email = input()
    print("Enter the Sender's password")
    from_pass = input()
    server.login(from_email,from_pass)
    print("Enter the receiver's email address:")
    to_email = input()
    print("Email subject")
    subject = input()
    print("Email body")
    body = input()
    msg = MIMEText(body)
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    text = msg.as_string()
    server.sendmail(from_email,to_email,text)
    print("Email Sent")
    server.quit()

def imap_protocol():
    imap_host = 'imap.mail.yahoo.com'
    print("Email address to retrieve email")
    imap_user = input()
    print("Enter Password for the above email address:")
    imap_pass = input()
    print("Enter the email id of the user whose latest email you want to read.")
    from_email =  input()
    imap = imaplib.IMAP4_SSL(imap_host)

    imap.login(imap_user,imap_pass)

    status, data = imap.select('INBOX',readonly=True)
    status, msg_ids = imap.search(None, "FROM", '"{}"'.format(from_email))
    msg_ids_string = str(msg_ids[0])
    msg_ids_list = msg_ids_string.split(' ')
    status, msg_full = imap.fetch(msg_ids_list[len(msg_ids_list)-2],'(RFC822)')
    for response_part in msg_full:
        if type(response_part) is tuple:
            content = str(response_part[1],'utf-8')
            data = str(content)
            try:
                indexstart = data.find("Content-Transfer-Encoding")
                data2 = data[indexstart+31: len(data)]
                print(data2)
            except UnicodeEncodeError as e:
                pass

def pop_protocol():
    popserver = 'pop.mail.yahoo.com'
    print("Email address to retrieve email")
    username = input()
    print("Enter Password for the above email address:")
    password = input()

    pop = poplib.POP3_SSL(popserver)

    pop.user(username)
    pop.pass_(password)

    numMessages = len(pop.list()[1])

    for i in range(numMessages):
        latest = i

    print("Latest Email in the inbox\n")
    message = pop.retr(latest+1)[1]
    truncated = message[len(message)-8:len(message)]
    print(utf8(truncated[0]))
    print(utf8(truncated[1]))
    print(utf8(truncated[2]))
    print("Body: ", utf8(truncated[len(truncated)-1]))

def main_protocol():
    print("Please enter the protocol to be executed: ")
    print("smtp")
    print("imap")
    print("pop\n")
    protocol = input()
    if protocol == "smtp":
        smtp_protocol()
    elif protocol == "imap":
        imap_protocol()
    elif protocol == "pop":
        pop_protocol()
    else:
        print("Incorrect input")


if __name__ == '__main__':
    main_protocol()

