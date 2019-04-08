from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.contrib.auth.models import User, AnonymousUser
from .models import Appointment, Article, Comment
from .forms import UploadFileForm
from datetime import datetime

# Create your views here.
def check_auth(request, url, content = {}):
	template = loader.get_template('login/login.html')
	
	if request.user != AnonymousUser and request.user.is_authenticated:
		return render(request, url, content)
	else:
		return redirect('/login/')

def index(request):
	template = loader.get_template('login/login.html')
	return check_auth(request, 'index.html')

def account_info(request):

	users = User.objects.all()
	user_names = [u.get_username() for u in users]

	return_info ={'user_names': user_names}
	
	return check_auth(request, 'login/account_info.html', return_info)

def appointment_info(request, filter = None):
	aps = Appointment.objects.all()
	filtered = 0
	if filter:
		filtered = 1
		[name, phone, id_card, date_stamp] = filter.split(":")
		if date_stamp == "":
			date_stamp = 0
		return_info = {"info": [],
					   "filter": 1,
					   "name": name,
					   "phone": phone,
					   "id_card": id_card,
					   "date_stamp": date_stamp
					   }
		aps = list(aps.filter(name__icontains=name, number__icontains=phone, id_card__icontains=id_card, date__gte=datetime.utcfromtimestamp(float(date_stamp))))
		return_info['info'] = [(appoint.name, appoint.number, appoint.id_card, appoint.date.timestamp(), appoint.app_id) for appoint in aps]
	else:
		return_info = {"info": [(appoint.name, appoint.number, appoint.id_card, appoint.date.timestamp(), appoint.app_id) for appoint in aps],
		"filter":filtered}

	return check_auth(request, 'appointment.html', return_info)

def appointment_change(request):
	idx = request.POST['idx']
	type_ = request.POST['type']
	aps = Appointment.objects.all()
	obj = aps.get(app_id=idx)
	
	if type_ == 'change':
		name = request.POST['name']
		phone = request.POST['phone']
		id_card = request.POST['id_card']
		date = request.POST['date']

		obj.name = name
		obj.number = phone
		obj.id_card = id_card
		obj.date = datetime.utcfromtimestamp(float(date))
		obj.save()
		return HttpResponse("Success")
	elif type_ == 'delete' and request.user != AnonymousUser and request.user.is_authenticated:
		obj.delete()
		return HttpResponse("Success")
	else:
		return HttpResponse("Failed")

def info_page(request, article = None):
	article_id = article
	edit = -1
	if request.method == 'POST':
		form = UploadFileForm(request.POST, request.FILES)
		if form.is_valid():
			url = request.build_absolute_uri('/')[:-1].strip("/")
			edit_id = request.POST['edit_id']
			title = request.POST['title']
			audio_title = request.POST['audio_title']
			html = request.POST['content']
			brief = request.POST['brief']
			# print(request.POST.keys())
			if 'top_view' in request.POST.keys():
				# print(123)
				top_view = 1
			else:
				top_view = 0
			type = request.POST['type']
			# print('edit_id', edit_id)
			if edit_id == "-1":
				article = Article()
			else:
				article = Article.objects.get(article_id = edit_id)
			article.title = title
			article.brief = brief
			article._type = type
			article.audio_title = audio_title
			article.top_view = top_view
			article.file = 'guides/audio/{}.mp3'.format(article.article_id)
			article.page = 'guides/article/{}.html'.format(article.article_id)
			# print(type)
			article.save()
			article.file = 'guides/audio/{}.mp3'.format(article.article_id)
			article.page = 'guides/article/{}_{}.html'.format(article.article_id, article.title)
			article.image = 'guides/image/{}.jpg'.format(article.article_id)
			article.save()
			# print(article.page)
			if 'file' in request.FILES:
				handle_audio_file(request.FILES['file'], article.article_id)
			if 'image' in request.FILES:
				handle_image_file(request.FILES['image'], article.article_id)
			with open(article.page, 'w') as f:
				f.write(html)
			

		return redirect('/info/' + str(article.article_id))
	else:
	    form = UploadFileForm(initial = {
	    	'edit_id':-1,
	    	})

	articles = Article.objects.all()
	if article_id:
		edit = article_id

		obj = articles.get(article_id = article_id)
		# print(obj.image)
		if obj.top_view == 1:
			top_view = "on"
		else:
			top_view = ""
		with open(obj.page, 'r') as f:
			form = UploadFileForm(initial = {
				"title":obj.title,
				"brief":obj.brief,
				"type":obj._type,
				"image":obj.image,
				"content": f.read(),
				"edit_id": article_id,
				"top_view": top_view,

				})
	
	list_ = [(obj.title, obj.brief, obj.article_id, obj.image) for obj in articles]
	
	return check_auth(request, 'information.html', {'form': form,
												    'list': list_,
												    'edit_id': edit,
												    })

def handle_audio_file(f, name):
    with open('guides/audio/{}.mp3'.format(name), 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def handle_image_file(f, name):
	with open('guides/image/{}.jpg'.format(name), 'wb+') as destination:
		for chunk in f.chunks():
			destination.write(chunk)

def change_password(request):
	users = User.objects.all()
	type_ = request.POST['type']
	username = request.POST['username']
	try:
		if type_ == 'change':
			user_obj = users.filter(username=username)[0]
			passwd = request.POST['passwd']
			user_obj.set_password(passwd)
			user_obj.save()
			return HttpResponse("Success")
		elif type_ == 'delete':
			if (len(users) == 1):
				return HttpResponse("Only one!")
			user_obj = users.filter(username=username)[0]
			user_obj.delete()
			return HttpResponse("Success")
		elif type_ == "new":
			passwd = request.POST['passwd']
			user_obj = User.objects.create_user(username=username, password=passwd)
			user_obj.save();
			return HttpResponse("Success")
		else:
			return HttpResponse("Failed")
	except Exception as e:
		return HttpResponse("Failed")

def delete_article(request):
	obj = Article.objects.all();
	# print(request.POST['type'])
	if request.POST['type'] == 'delete':
		idx = request.POST['idx']
		article = obj.get(article_id = idx)
		# print(article.title)
		article.delete()
		return HttpResponse("Success")


def wx_article_list(request):
	articles = Article.objects.all()
	list_ = [(obj.title, obj.brief, obj.article_id, obj.image, obj.page, obj._type, obj.top_view) for obj in articles]
	return JsonResponse(list_, safe=False)

def wx_get_article(request, idx):
	obj = Article.objects.get(article_id=idx)
	article_info = {
				"title":obj.title,
				"brief":obj.brief,
				"type":obj._type,
				"image":obj.image,
				"content": obj.page,
				}
	return JsonResponse(article_info)



def wx_comment(request):
	try:
		type = request.POST['type']
		if type == 'add':
			article_id = request.POST['id']
			comment = request.POST['comment']
			date = request.POST['timestamp']
			wx_id = request.POST['wx_id']
			name = request.POST['name']

			c = Comment()
			c.article_id = article_id
			c.comment = comment
			c.date = datetime.utcfromtimestamp(float(date))
			c.wx_id = wx_id
			c.name = name
			c.save()

			return HttpResponse(c.comment_id)
		if type == 'get':
			article_id = request.POST['article_id']
			commnets = Comment.objects.filter(article_id=article_id)
			return_info = [(obj.article_id, obj.commnets, obj.date, obj.wx_id, obj.name, obj.comment_id, obj.top_view) for obj in comments]
			return JsonResponse(return_info, safe=False)


	except Exception:
		return HttpResponse("Failed")