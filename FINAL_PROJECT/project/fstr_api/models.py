from django.db import models

class User(models.Model):
    email = models.EmailField(unique=True)
    fam = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    otc = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, unique=True)


class Coords(models.Model):
    latitude = models.DecimalField(max_digits=6, decimal_places=4)
    longitude = models.DecimalField(max_digits=7, decimal_places=4)
    height = models.IntegerField()


class Level(models.Model):
    winter = models.CharField(max_length=10, blank=True, default='')
    summer = models.CharField(max_length=10, blank=True, default='')
    autumn = models.CharField(max_length=10, blank=True, default='')
    spring = models.CharField(max_length=10, blank=True, default='')


class Pass(models.Model):
    beauty_title = models.CharField(max_length=255, blank=True, null=True)
    title = models.CharField(max_length=255)
    other_titles = models.CharField(max_length=500, blank=True, null=True)
    connect = models.TextField(blank=True, null=True)
    add_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="passes")
    coords = models.OneToOneField(Coords, on_delete=models.CASCADE)
    level = models.OneToOneField(Level, on_delete=models.CASCADE)


class Image(models.Model):
    data = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    pass_obj = models.ForeignKey(Pass, on_delete=models.CASCADE, related_name="images")
    


