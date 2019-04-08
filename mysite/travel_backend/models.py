from django.db import models

# Create your models here.
class Appointment(models.Model):
	name = models.CharField(max_length = 10)
	number = models.IntegerField()
	id_card = models.IntegerField()
	date = models.DateTimeField()
	app_id = models.AutoField(primary_key=True)
	

class Article(models.Model):
	title = models.CharField(max_length = 100)
	brief = models.CharField(max_length = 1000)
	_type = models.IntegerField()
	audio = models.CharField(max_length = 1000)
	page = models.CharField(max_length = 1000)
	image = models.CharField(max_length = 1000)
	article_id = models.AutoField(primary_key=True)
	top_view = models.IntegerField(default = 0)


class Comment(models.Model):
	article_id = models.IntegerField(max_length=130)
	comment = models.CharField(max_length=1000)
	date = models.DateTimeField('date published')
	wx_id = models.CharField(max_length=1000)
	name = models.CharField(max_length=1000)
	comment_id = models.AutoField(primary_key=True)
	