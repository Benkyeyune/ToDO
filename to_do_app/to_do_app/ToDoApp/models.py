from django.db import models
from django.contrib.auth.models import User

# user models.
class UserProfileInformation(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=10)
    # profile_picture = models.ImageField(upload_to='profile_pictures',blank=True)

    def __str__(self):
        return self.user.first_name,self.user.last_name,self.user.email,self.user.username,self.phone_number
    

# the to do task model.

class Task(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE,null=True,blank=False)
    title = models.CharField(max_length=250)
    activity = models.TextField(max_length=1000)
    starting_time = models.DateTimeField()
    reminder_time =models.DateTimeField()

    status_choice = (('Un attempted','Un attempted'),('Done','Done'))
    status = models.CharField(choices=status_choice, max_length=15,default='un attempted')

    def __str__(self):
        return self.title
    class meta:
        order_with_respect_to ='user'
