from django.core.mail import send_mail

class Email:
    def __init__(self):
        pass
    def register_email(self,to):
        send_mail('Registeration completed', 'We are pleased to inform you that you have completed the registeration process. You can now login and use our services', 'laundarydjango@gmail.com',[to])

    def checkin(self, to, data):  #sends mail about laundary submission
        send_mail('Order confiramation', 'Your request of submitting laundary('+ str(data[0])+') is successfully registered. You can collect laundary on '+str(data[1])[:10],
                 'laundarydjango@gmail.com',[to])

    def checkout(self, to): #sends mail about laundary collection
        send_mail('Order collected', 'Thanks for using our service',
                 'laundarydjango@gmail.com',[to])

    def  cycles_exhausted(self, to,name): #sends mail to tell user that there cycles are exhausted
        send_mail('Cycles exhausted', 'Dear '+name+", this is to inform you that all of yours cycles are exhausted, you may contact admin if you wish for more cycles",
                 'laundarydjango@gmail.com',[to])
    