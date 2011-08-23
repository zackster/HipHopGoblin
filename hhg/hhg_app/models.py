from django.db import models
from django.contrib.auth.models import User, UserManager

class Song(models.Model):
	title = models.CharField(max_length=70, unique=False, blank=False)
	url = models.CharField(max_length=255, unique=True, blank=False)
	count = models.PositiveIntegerField(null=True)
	timestamp = models.PositiveIntegerField(null=True)
	fn = models.CharField(max_length=70, unique=True, blank=False)
	artist_id = models.IntegerField(unique=True,null=True)
	uploader_id = models.IntegerField(unique=False)
	comment = models.CharField(max_length=200,null=True)
	def __unicode__(self):
		return self.title

def get_unique_songfn(title, id):
	fixed = title.lower().strip(' ')
	return fixed + str(id) + '.mp3'

	
class Artist(models.Model):
	name = models.CharField(max_length=32, blank=False)
	description = models.CharField(max_length=240,blank=True, null=True)
	location = models.CharField(max_length=50,blank=True,null=True)
	user_id = models.IntegerField()

class PlaylistSong(models.Model):
	ps_id = models.PositiveIntegerField()
	playlist = models.ForeignKey('Playlist')
	song = models.ForeignKey(Song)
	#def __init__(song, last=False, next, id, pl):
	#	pass

class Playlist(models.Model):
	name = models.CharField(max_length=70)
	playlist_id = models.IntegerField()
	last = models.IntegerField()
	user = models.ForeignKey(User)

	#def getList():
	#	pass

	def __unicode__(self):
		return self.name

class Like(models.Model):
	by = models.IntegerField(unique=False,null=False)
	song_id = models.IntegerField(unique=False,null=False)
	timestamp = models.IntegerField(blank=True)
