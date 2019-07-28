# -*- coding: utf-8 -*-

import time
from django.utils import timezone
from detect.models import Player, Card, Paper
from django.shortcuts import render, render_to_response, HttpResponse
from detect import yolo_start
import json

def detect(request):
	request.encoding='utf-8'
	if request.method == 'POST':
		nickname = request.POST['nickname']
		img = request.FILES['file']
		suffix = (request.FILES['file'].name).split('.')[-1]
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
		data = {
			'list':output_dict,
			'title':title,
			'suffix':suffix,
		}
		json_str = json.dumps(data)
		response = HttpResponse(json_str)
		return response
	else:
		return HttpResponse("<p>请上传图片</p>")
