from django.http import HttpResponse
from hhg_app.models import Song, PlaylistSong, Playlist


def like_song(request,  songid):
    #create Like object in database
    if request.user.is_authenticated():
        s = Song.objects.get(id=songid)
        s.count = s.count + 1
        s.save()
	like, created = Playlist.objects.get_or_create(user=request.user, playlist_id=0,name="liked")
	like.save()
        ps = PlaylistSong(playlist=like, ps_id=like.last+1, song=s)
	ps.save()
        if created:
            #like.first = ps
            like.save()
    else:
        pass
    return HttpResponse()

def unlike_song(request,  songid):
    #delete Like object in database
    s = Song.objects.get(id=songid)
    s.count = s.count - 1
    s.save()
    return HttpResponse()

