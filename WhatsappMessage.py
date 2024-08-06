import os 
from twilio.rest import Client

account_sid = 'AC347a62b8f5d7a5af05ba99f9a85b7ed8'
auth_token = '7e927047d97f2003d6177cf30c762b60'
client = Client(account_sid, auth_token)

message = client.messages.create(
  from_='whatsapp:+14155238886',
  body='MOVEMENT DETECTED',
  to='whatsapp:+918018738353'
)

print(message.sid)