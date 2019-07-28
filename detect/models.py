from django.db import models
import os


def save_cards(instance, filename):
	suffix = filename.split('.')[-1]
	filename = "%s.%s" % (instance.title, suffix)
	return os.path.join('cards', filename)

def save_papers(instance, filename):
	suffix = filename.split('.')[-1]
	filename = "%s.%s" % (instance.title, suffix)
	return os.path.join('papers', filename)

class Player(models.Model):
	nickname = models.CharField(max_length=200)
	join_time = models.DateTimeField('join time')
	profile_photo = models.ImageField(upload_to='players')

	def __str__(self):
		return self.nickname

class Card(models.Model):
	player = models.ForeignKey(Player, on_delete=models.CASCADE)
	img = models.ImageField(upload_to=save_cards)
	title = models.CharField(max_length=200)
	author = models.CharField(max_length=200)
	pub_date = models.DateTimeField('date published')

	def __str__(self):
		return self.title

class Paper(models.Model):
	player = models.ForeignKey(Player, on_delete=models.CASCADE)
	img = models.ImageField(upload_to=save_papers)
	title = models.CharField(max_length=200)
	author = models.CharField(max_length=200)
	pub_date = models.DateTimeField('date published')

	def __str__(self):
		return self.title
