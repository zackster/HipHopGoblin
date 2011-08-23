from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from hhg_app import scraper
from django.contrib.auth.models import User, UserManager
from hhg_app.models import Song
from django.contrib.auth import login as authlogin
from django.contrib.auth import logout as authlogout
from hhg_app.forms import RegisterForm, LoginForm
import simplejson as json
import time
from django.contrib.auth.decorators import login_required
import bitly.bitly
import settings
import urllib, urllib2

API_URL = "http://developer.echonest.com/api/v4/"
ECHO_NEST_API_KEY = "Z5BUWFNXJP6NGXADB"#"PTRU3M6QKIIFXZCIK"

CONSUMER_KEY = 'ecJxueo2aLIvZ2bPadb3w'
CONSUMER_SECRET = 'MmbP5j1yKHBmSjsJB7j3q9D0b3J34ZOqqayZF9p3dE'
ACCESS_KEY = '64673120-PacJfLzv1TcvSheqSBkyJygVn16BJpALCDi1EEX9r'
ACCESS_SECRET = 'xIkA3RBApx0J83sIhxt33xJEQck0t5v6r6aucKxBak'

def hhg(request):
	if request.user.is_authenticated():
		user = request.user
		uploads = Song.objects.filter(uploader_id=user.id)
		up_num = len(uploads)
		up_left = 10-up_num
		top = Song.objects.order_by('timestamp').reverse()[0:12]
		top10 = Song.objects.order_by('count').reverse()[0:10]
                template = 'index-new-login.html'
		return render_to_response(template, {'user':user,'top':top,'top10':top10,'up_num':up_num,'up_left':up_left,}, context_instance=RequestContext(request))
		#else:
			#return render_to_response(template, {'top':top, 'user':user}, context_instance=RequestContext(request))	
	else:
		login = LoginForm()
		register = RegisterForm()
		top = Song.objects.order_by('timestamp').reverse()[0:12]
		template = 'index-slides.html'
		return render_to_response(template, {'top':top, 'register':register, 'login':login}, context_instance=RequestContext(request))

def get_echonest_id(name):
        q = [('api_key',ECHO_NEST_API_KEY),('name',name)]
        function = 'artist/search?'
	js = json.loads(urllib2.urlopen(API_URL+function+urllib.urlencode(q)).read())
        try:
            return js['response']['artists'][0]['id']
        except:
            return None

def hhg_stage(request):
	if request.user.is_authenticated():
		user = request.user
		uploads = Song.objects.filter(uploader_id=user.id)
		up_num = len(uploads)
		up_left = 10-up_num
		top = Song.objects.order_by('timestamp').reverse()[0:12]
		top10 = Song.objects.order_by('count').reverse()[0:10]
                template = 'index-august-login.html'
		return render_to_response(template, {'user':user,'top':top,'top10':top10,'up_num':up_num,'up_left':up_left,'sims':similars,'id':get_echonest_id(to_search)}, context_instance=RequestContext(request))
	else:
                #This is the code that matters right now
		login = LoginForm()
		register = RegisterForm()
		top = Song.objects.order_by('timestamp').reverse()[0:15]
		top10 = Song.objects.order_by('count').reverse()[0:10]
                top_dicts = []
                top10_dicts = []
                for song in top:
                        artist_name = song.title.split(' - ')
                        top_dicts.append({'id':song.id, 'artist':artist_name[0], 'title':artist_name[1]})
                for song in top10:
                        artist_name = song.title.split(' - ')
                        top10_dicts.append({'id':song.id, 'artist':artist_name[0], 'title':artist_name[1]})
		template = 'index-august.html'
		return render_to_response(template, {'top':top_dicts, 'top10':top10_dicts, 'register':register, 'login':login,}, context_instance=RequestContext(request))


aliaser = {'throne':'/home/hiphopgoblin/webapps/django/hhg/static/playlists/play.json'}

def playlistnext(request, alias, id):
        js = json.loads(open(aliaser[alias],'rb').read())
        next_id = js['nexter'][id]
        s = Song.objects.get(id=next_id)
        return HttpResponse(json.dumps({"filename":s.url, "title":s.title, "count":s.count,"id":s.id,}))

def playlist(request, alias):
	login = LoginForm()
	register = RegisterForm()
        js = json.loads(open(aliaser[alias],'rb').read())
	top = [Song.objects.get(id=id) for id in js['songs']]
        first = js['songs'][0]
        top_dicts = []
        for song in top:
                artist_name = song.title.split(' - ')
                top_dicts.append({'id':song.id, 'artist':artist_name[0], 'title':artist_name[1]})
	template = 'index-playlist.html'
	return render_to_response(template, {'first_play':first, 'playlistname':js['name'], 'top':top_dicts, 'register':register, 'login':login,}, context_instance=RequestContext(request))


def api_imageurl(id):
        function = 'artist/images?'
        q = [('api_key',ECHO_NEST_API_KEY),('id', id),('format','json'),('results',5), ('license','unknown')]
        try:
                js = json.loads(urllib2.urlopen(API_URL+function+urllib.urlencode(q)).read())
                if id in image_list.keys():
                        return js['response']['images'][image_list[id]]['url']
                return js['response']['images'][0]['url']
        except:
                raise urllib2.URLError

def getsimilars(request):
        artist_name = request.GET['title'].split(' - ')
        if len(artist_name) == 2:
                artist = artist_name[0]
        else:
                return HttpResponse()
        id = get_echonest_id(artist)
        q = [('api_key',ECHO_NEST_API_KEY),('id',id),('format','json'),('results',5),('start',0)]
        function = 'artist/similar?'
        js = json.loads(urllib2.urlopen(API_URL+function+urllib.urlencode(q)).read())
        similars = [art['name'] for art in js['response']['artists']]
        to_return = ""
        for sim in similars:
                to_return += "<p class='similar'>" + sim + "</p>"
        return HttpResponse(to_return)

image_list = {'ARLGIX31187B9AE9A0':4, 'ARXIBDN1187B994F5E':4}
artist_imgdict = {'Jay-Z, Kanye West'       : '/static/images/throne.jpg',
                  'Kendrick Lamar'          : '/static/images/kendrick.jpg',
                  'J. Cole'                 : '/static/images/jcole.jpg',
                  'Meek Mill'               : '/static/images/meekmill.png',
                  'The Cool Kids'           : '/static/images/coolkids.jpg',
                  'Gorilla Warfare Tactics' : '/static/images/gorilla.jpg',}

def getdata(request):
        artist_name = request.GET['title'].split(' - ')
        if len(artist_name) == 0:
                return HttpResponse()
        else:
                artist = artist_name[0]
                if len(artist_name) > 1:
                        name = artist_name[1]
                        if artist in artist_imgdict.keys():
                                json_string = '{"api_image_url":"%s", "artist":"%s", "name":"%s"}' % (artist_imgdict[artist], artist, name)
                                return HttpResponse(json_string)
                else:
                        name = ""
        try:
                imgurl = api_imageurl(get_echonest_id(artist))
                resp = urllib2.urlopen(imgurl)
                json_string = '{"api_image_url":"%s", "artist":"%s", "name":"%s"}' % (imgurl, artist, name)
        except:
                json_string = '{"api_image_url":"%s", "artist":"%s", "name":"%s"}' % ("/static/images/biggie.jpg", artist, name)
        return HttpResponse(json_string)

def secret(request):
        top = Song.objects.order_by('timestamp').reverse()
	template = 'index-secret.html'
        return render_to_response(template,{'top':top},context_instance=RequestContext(request))

def get_twitter_widget(request):
        artist_name = request.GET['title'].split(' - ')
        artist = artist_name[0]
        name = artist_name[1]
        twitter_string = "<script>new TWTR.Widget({version: 2,type: 'search',search: '%s OR %s OR hiphopgoblin',interval: 6000,title: 'what u sayin bout...',subject: '%s',width: '25em',height: 140,theme: {shell: {background: '#A8A8A8',color: '#000',},tweets: {background: '#ffffff',color: '#444444',links: '#1985b5'}},features: {scrollbar: false,loop: true,live: true,hashtags: true,timestamp: true,avatars: true,toptweets: true,behavior: 'default'}}).render().start();</script>" % (artist, name, artist)
        return HttpResponse(twitter_string)

def getregisterform(request):
	form = RegisterForm()
	template = 'register.html'
	return render_to_response(template, {'form':form}, context_instance=RequestContext(request))

def getloginform():
        form = LoginForm()
        template = 'login.html'
        return render_to_response(template, {'form':form}, context_instance=RequestContext(request))

def register(request):
	if request.method == 'POST':
		form = RegisterForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			passw = form.cleaned_data['password']
			confirm = form.cleaned_data['confirm']
			email = form.cleaned_data['email']
			#display = form.cleaned_data['display']
			if passw == confirm and len(passw)>=6:
				try:
					h = User.objects.create_user(username, email, passw)
					# email validation link
                                        h.save()
					return HttpResponse('You just created an account with username ' + h.username)
				except Exception:
					return HttpResponse('Exception')
			else:
				return HttpResponse('Passwords must match, and be >6 characters')
		else:
			return HttpResponse('Invalid form data. Try again')
	elif request.method == 'GET':
		form = RegisterForm()
		template = 'register.html'
		return render_to_response(template, {'form':form}, context_instance=RequestContext(request))
		
@login_required
def logout(request):
	authlogout(request)
	return HttpResponseRedirect('/')

def login(request):
	if request.method == 'POST':
		from django.contrib.auth import authenticate
		form = LoginForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			passw = form.cleaned_data['password']
			u = authenticate(username=username, password=passw)
			if u is not None:
				authlogin(request, u)
				return HttpResponseRedirect('/upload')
			else:
				return HttpResponseRedirect('/')
		else:
			return HttpResponseRedirect('/');
        elif request.method == 'GET':
                form = LoginForm()
                template = 'login.html'
                return render_to_response(template, {'form':form}, context_instance=RequestContext(request))


def random(request):
	return HttpResponse(scraper.scrape())

def hot(request,songid):
	return HttpResponse(scraper.scrape(songid))

def track(request,songid):
	login = LoginForm()
        register = RegisterForm()
        top = Song.objects.order_by('timestamp').reverse()[0:15]
        top10 = Song.objects.order_by('count').reverse()[0:10]
        top_dicts = []
        top10_dicts = []
        for song in top:
                artist_name = song.title.split(' - ')
                top_dicts.append({'id':song.id, 'artist':artist_name[0], 'title':artist_name[1]})
        for song in top10:
                artist_name = song.title.split(' - ')
                top10_dicts.append({'id':song.id, 'artist':artist_name[0], 'title':artist_name[1]})
        template = 'index-august.html'
        return render_to_response(template, {'first_play':songid,'top':top_dicts, 'top10':top10_dicts, 'register':register, 'login':login,}, context_instance=RequestContext(request))


def clean(request):
	from hhg_app.models import Song
	import re
	for x in Song.objects.all():
		try:
			tag = re.compile(r'&#8211;')
			x.title = tag.sub('-', x.title)
			tag = re.compile(r'&.*?;')
			x.title = tag.sub(' ', x.title)
			x.save()
		except:
			pass

def getsongs(request):
	return scraper.getsongs(request)

def list(request):
	from hhg_app.models import Song

def handle_uploaded_file(title, file,up_id):
	from hhg_app.models import Song, Artist, get_unique_songfn
	#artst = Artist.objects.get(userid=request.user.id)
	song = Song(title=title,timestamp=time.time())
	song.save()
	filename=get_unique_songfn(title,song.id)
	song.fn = filename
	f = open('/home/hiphopgoblin/webapps/django/hhg/static/songs/'+filename,'wb+')
	for b in file.chunks():
		f.write(b)
	f.close()
	song.url = 'http://hiphopgoblin.com/static/songs/'+filename
	song.uploader_id = up_id
	song.save()
	return 'http://hiphopgoblin.com/track/'+str(song.id)

@login_required
def upload(request):
        from hhg_app.forms import UploadForm
        if request.method == 'POST' and request.user.is_staff:
            form = UploadForm(request.POST, request.FILES)
            if form.is_valid():
                title = form.cleaned_data['title']
		#twitter = oauthtwitter.OAuthApi(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET)
		bitly_api = bitly.bitly.Api(login="jasons616",apikey="R_3ef914e7da37024dd2b41f5381883d1c")
		if len(Song.objects.filter(uploader_id=request.user.id))<10 or request.user.is_staff:
                	short = bitly_api.shorten(handle_uploaded_file(title,request.FILES['file'],request.user.id))
			#twitter.UpdateStatus('just uploaded '+title+' '+short)
                return HttpResponseRedirect('/upload/')
        else:
            form = UploadForm()
        return render_to_response('file_upload.html', {'uploader': form},context_instance=RequestContext(request))

def search(request):
        query = request.GET['query']
	qset = []
	out = ''
	if query=="SHOW_ALL":
		list_q = Song.objects.all()
	else:
		query_list = query.split('+')
		for q in query_list:
			list_q = Song.objects.filter(title__icontains=q)
	for l in list_q:
		if [l.title,l.id] not in qset:
			qset.append([l.title,l.id])
	for q in qset:
                artist_name = q[0].split(' - ')
                if len(artist_name) == 2:
                        out += '<a onClick="next('+str(q[1])+');" style="cursor:pointer;"><div class="songbutton"><strong>'+artist_name[0]+'</strong>&nbsp;&bull;&nbsp;'+artist_name[1]+'</div></a>'
                else:
		        out += '<a onClick="next('+str(q[1])+');" style="cursor:pointer;"><div class="songbutton">'+q[0]+'</div></a>'
	return HttpResponse(out)

@login_required
def song_info(request,id):
	from hhg_app.models import Like
	try:
		ls = Like.objects.get(by=request.user.id,song_id=id);
	except:
		ls = None
	s = Song.objects.get(id=id);
	try:
		uploader = User.objects.get(id=s.uploader_id).username
	except:
		uploader = "unknown"
	song_info = "<p>uploaded by <strong>"+uploader+"</strong></p><p style='font-size:12px;'></p>"
	like_info = ""
	if ls is not None:
		like_info = "You like this song.  <a style='cursor:pointer;' onClick='unlike_song("+str(s.id)+");'>Unlike</a>"
	else:
		like_info = "<a style='cursor:pointer;' onClick='like_song("+str(s.id)+");'>Like this song</a>"
	return HttpResponse('<p>'+like_info+'</p><p>'+song_info+'</p>')
	
@login_required
def unlike(request,id):
	from hhg_app.models import Like
        song = Song.objects.get(id=id)
	l = Like.objects.get(by=request.user.id,song_id=song.id)
	if song.count and song.count>0:
		song.count-=1
		song.save()
	l.delete()
	return HttpResponse()

@login_required
def like(request,id):
	from hhg_app.models import Like
	song = Song.objects.get(id=id)
	l = Like(by=request.user.id,song_id=song.id,timestamp=time.time())
	if song.count:
		song.count +=1	
	else:
		song.count = 1
	song.save()
	l.save()
	return HttpResponse("you now like song #"+str(id))

@login_required
def edit(request):
	sng = Song.objects.filter(uploader_id=request.user.id)
	return render_to_response('edit.html',{'songs':sng, 'user':request.user},context_instance=RequestContext(request))

@login_required
def comment(request, id):
	try:
		if request.method == "POST":
			s = Song.objects.get(id=id,uploader_id=request.user.id)
			s.comment = request.POST['comment']
			s.save()
	except:
		pass
	return HttpResponseRedirect('/edit/')

@login_required
def get_likes(request):
	from hhg_app.models import Like
	ls = Like.objects.filter(by=request.user.id).order_by('timestamp').reverse()[:7]
	ss = []
	if len(ls)>0:
		for l in ls:
			try:
				s = Song.objects.get(id=l.song_id)
				ss.append(s)
			except:
				pass
	
	out = "<h2>Recently Liked</h2><table id='topsongs' width='15em'>"
	for s in ss:
		out += "<tr class='row'><td><a onClick='next("+str(s.id)+");'>"+s.title+"</a></td></tr>"
	out += "</table>"
	return HttpResponse(out)
