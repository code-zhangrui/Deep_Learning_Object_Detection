# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response, HttpResponse
from detect.models import Player, Card, Paper

def delete_all(request):
	# test1 = Test.objects.get(id=1)
	# test1.delete() # 删除id=1的数据
	# Test.objects.filter(id=1).delete() # 删除id=1的数据

	Card.objects.all().delete() # 删除所有数据
	Paper.objects.all().delete() # 删除所有数据
	Player.objects.all().delete() # 删除所有数据
	return HttpResponse("<p>删除成功</p>")
