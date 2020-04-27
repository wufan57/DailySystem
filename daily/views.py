import os
from io import BytesIO

import xlwt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

from daily.form import DailyPostForm
from daily.models import DailyPost


def list(request):
    date = request.GET.get('date')
    list = DailyPost.objects.all().order_by('-created')

    if date:
        date = date.strip()
        list = list.filter(created__icontains=date).order_by('-created')


    paginator = Paginator(list, 5)
    # 获取 url 中的页码
    page = request.GET.get('page')
    # 将导航对象相应的页码内容返回给 articles
    dailylist = paginator.get_page(page)
    # 需要传递给模板（templates）的对象
    context = {'dailylist': dailylist, "date": date}

    return render(request, 'daily/list.html', context)

@login_required(login_url='/userprofile/login/')
def create(request):
    # 判断用户是否提交数据
    if request.method == "POST":
        # 将提交的数据赋值到表单实例中
        daily_post_form = DailyPostForm(request.POST)
        # 判断提交的数据是否满足模型的要求
        if daily_post_form.is_valid():
            # 保存数据，但暂时不提交到数据库中
            new_daily = daily_post_form.save(commit=False)
            new_daily.author = User.objects.get(id=request.user.id)
            # 将日报保存到数据库中
            new_daily.save()
            # 完成后返回到日报列表
            return redirect("daily:list")
        # 如果数据不合法，返回错误信息
        else:
            return HttpResponse("输日报表单内容有误，请重新填写。")
    # 如果用户请求获取数据
    else:
        return render(request, 'daily/create.html')

def excel_export(request):
    date = request.GET.get('date')
    """导出excel表格"""
    dailylist = DailyPost.objects.all().order_by('-created')

    if len(date)>0:
        dailylist = dailylist.filter(created__icontains=date).order_by('-created')


    if dailylist:
        # 创建工作薄
        ws = xlwt.Workbook(encoding="UTF-8")
        w = ws.add_sheet(u'日报')
        w.write(0, 0, 'id')
        w.write(0, 1, u'作者')
        w.write(0, 2, u'今日项目进度')
        w.write(0, 3, u'今日自动化进度')
        w.write(0, 4, u'明日计划（业务&自动化）')
        w.write(0, 5, u'创建时间')
        # 设置每一列的宽度
        w.col(0).width = 3000
        w.col(1).width = 3000
        w.col(2).width = 15000
        w.col(3).width = 15000
        w.col(4).width = 15000
        w.col(5).width = 3000

        # 初始化样式
        style = xlwt.XFStyle()
        # 自动换行
        style.alignment.wrap = 1
        # 写入数据
        excel_row = 1
        for daily in dailylist:
            daily_id = daily.id
            daily_author = daily.author.profile.nikename
            daily_todaytask = daily.todaytask
            daily_autotask = daily.autotask
            daily_tomorrowtask = daily.tomorrowtask
            daily_created = daily.created.strftime('%Y-%m-%d')
            w.write(excel_row, 0, daily_id)
            w.write(excel_row, 1, daily_author)
            w.write(excel_row, 2, daily_todaytask,style)
            w.write(excel_row, 3, daily_autotask,style)
            w.write(excel_row, 4, daily_tomorrowtask,style)
            w.write(excel_row, 5, daily_created)
            excel_row += 1

        exist_file = os.path.exists("daily.xls")
        if exist_file:
            os.remove(r"daily.xls")
        ws.save("daily.xls")
        ############################
        sio = BytesIO()
        ws.save(sio)
        sio.seek(0)
        response = HttpResponse(sio.getvalue(), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename=daily.xls'
        response.write(sio.getvalue())
        return response

@login_required(login_url='/userprofile/login/')
def edit(request, id):
    # 获取需要修改的日报对象
    daily = DailyPost.objects.get(id=id)

    # 过滤非作者的用户
    if request.user != daily.author:
        return HttpResponse("抱歉，你无权修改这篇文章。")

    # 判断用户是否为 POST 提交表单数据
    if request.method == "POST":
        # 将提交的数据赋值到表单实例中
        daily_post_form = DailyPostForm(data=request.POST)
        # 判断提交的数据是否满足模型的要求
        if daily_post_form.is_valid():
            # 保存新写入的 title、body 数据并保存
            daily.todaytask = request.POST['todaytask']
            daily.autotask = request.POST['autotask']
            daily.tomorrowtask = request.POST['tomorrowtask']
            daily.save()
            # 完成后返回到日报列表
            return redirect("daily:list")
        # 如果数据不合法，返回错误信息
        else:
            return HttpResponse("表单内容有误，请重新填写。")

    # 如果用户 GET 请求获取数据
    else:
        # 赋值上下文，将日报对象也传递进去，以便提取旧的内容
        context = {'daily': daily}
        # 将响应返回到模板中
        return render(request, 'daily/edit.html', context)


def test(request):
    return render(request, 'daily/test.html')