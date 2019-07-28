# -*- coding: utf-8 -*-
import time
from django.utils import timezone
from django.shortcuts import render, render_to_response, HttpResponse
from detect.models import Player, Card, Paper
from django.http import HttpResponse
from detect import yolo_start


def detect(request):
	request.encoding='utf-8'
	if request.method == 'POST':
		nickname = 'rui'
		img = request.FILES.get('img')
		suffix = request.FILES.get('img').name.split('.')[-1]
		title = time.strftime('%Y%m%d%H%M%S') + '_' + nickname
		join_time = timezone.now()
		pub_date = timezone.now()
		if len(list(Player.objects.filter(nickname=nickname))) == 0:
			new_player = Player(
				nickname = nickname,
				join_time = join_time,
			)
			new_player.save()

		player = Player.objects.get(nickname=nickname)
		player.card_set.create(
			img = img,
			title = title,
			author = nickname,
			pub_date = pub_date,
		)
		output_dict = yolo_start.start(title, suffix)
		player.paper_set.create(
			img = '/papers/' + title + '.' + suffix,
			title = title,
			author = nickname,
			pub_date = pub_date,
		)
		img = Paper.objects.get(title = title)

		items = output_dict.items()
		output_list=[]
		for key,value in items:
			output_list.append(key+'(概率:'+str(round(value,2)*100)+'%);')
		output_list_str = ''
		for i in range(len(output_list)):
			output_list_str += output_list[i]
		output_str = '识别出:' + output_list_str
		content = {
			'img':img,
			'output_str':output_str
		}

		return render(request, 'detect/uploadimg.html', content)

	return render(request, 'detect/uploadimg.html')

def show_all(request, slug='default'):
	imgs = Paper.objects.all()
	content = {
		'imgs':imgs
	}
	return render(request, 'detect/showall.html', content)
