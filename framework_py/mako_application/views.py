# -*- coding: utf-8 -*-
"""
Tencent is pleased to support the open source community by making 蓝鲸智云PaaS平台社区版 (BlueKing PaaS Community
Edition) available.
Copyright (C) 2017-2020 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
You may obtain a copy of the License at
http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""

from django.shortcuts import render


# 开发框架中通过中间件默认是需要登录态的，如有不需要登录的，可添加装饰器login_exempt
# 装饰器引入 from blueapps.account.decorators import login_exempt
def home(request):
    """
    首页
    """

    return render(request, "mako_application/index_home.mako")


def dev_guide(request):
    """
    开发指引
    """
    return render(request, "mako_application/dev_guide.mako")


def contact(request):
    """
    联系页
    """
    return render(request, "mako_application/contact.mako")

from django.shortcuts import render
from .models import TSystem,RrdDay,AssetInfo
import pymysql

from django.http import HttpResponse

conn = pymysql.connect(
    host="localhost",
    user="root", password="",
    database="service_center",
    charset="utf8")

def query_all_dict(sql):
    cursor = conn.cursor()
    cursor.execute(sql)
    col_names = [desc[0] for desc in cursor.description]
    row = cursor.fetchall()
    row_list = []
    for lst in row:
        t_map = dict(zip(col_names, lst))
        row_list.append(t_map)
    return row_list

def ecs_mem_rate(system_id):
    sql = "select system_name,SYSTEM_ID,IP_ADDR from d_rrd_day_new as d1 "\
"left join t_asset_info as t1 on d1.parent_ne_id=t1.NE_ID "\
            "left join t_system as t2 on t1.SYSTEM_ID = t2.id where d1.attribute_code='YECS_MEM_RATE' "\
"and d1.avg_value>90 and SYSTEM_ID = {system} GROUP BY NE_ID;".format(system=system_id)
    ecs_mem = query_all_dict(sql)
    all_data = ecs_mem

    return all_data

def ecs_cpu_rate(system_id):
    sql = "select system_name,SYSTEM_ID,IP_ADDR from d_rrd_day_new as d1 "\
"left join t_asset_info as t1 on d1.parent_ne_id=t1.NE_ID "\
          "left join t_system as t2 on t1.SYSTEM_ID = t2.id where d1.attribute_code='YECS_CPU_RATE' "\
"and d1.avg_value>90 and SYSTEM_ID = {system} GROUP BY NE_ID;".format(system=system_id)
    ecs_cpu = query_all_dict(sql)
    all_data = ecs_cpu

    return all_data

def ecs_disk_rate(system_id):
    sql = "select system_name,SYSTEM_ID,IP_ADDR from d_rrd_day_new as d1 " \
          "left join t_asset_info as t1 on d1.parent_ne_id=t1.NE_ID "\
          "left join t_system as t2 on t1.SYSTEM_ID = t2.id where d1.attribute_code='YECS_DISK_RATE' " \
          "and d1.avg_value>90 and SYSTEM_ID = {system} GROUP BY NE_ID;".format(system=system_id)
    ecs_rate = query_all_dict(sql)
    all_data = ecs_rate

    return all_data

def ecs_disk_read(system_id):
    sql = "select system_name,SYSTEM_ID,IP_ADDR from d_rrd_day_new as d1 " \
          "left join t_asset_info as t1 on d1.parent_ne_id=t1.NE_ID "\
          "left join t_system as t2 on t1.SYSTEM_ID = t2.id where d1.attribute_code='YECS_DISK_READ' " \
          "and d1.avg_value>700000 and SYSTEM_ID = {system} GROUP BY NE_ID;".format(system=system_id)
    ecs_read = query_all_dict(sql)
    all_data = ecs_read

    return all_data

def ecs_disk_write(system_id):
    sql = "select system_name,SYSTEM_ID,IP_ADDR from d_rrd_day_new as d1 " \
          "left join t_asset_info as t1 on d1.parent_ne_id=t1.NE_ID "\
          "left join t_system as t2 on t1.SYSTEM_ID = t2.id where d1.attribute_code='YECS_DISK_WRITE' " \
          "and d1.avg_value>900000 and SYSTEM_ID = {system} GROUP BY NE_ID;".format(system=system_id)
    ecs_write = query_all_dict(sql)

    return ecs_write

# Create your views here.
def index(request):
    sql = "select DISTINCT SYSTEM_ID,system_name from t_asset_info as t1 left join  "\
          "t_system as ts on t1.SYSTEM_ID=ts.id; "
    data_list = query_all_dict(sql)
    for i in data_list:
        system_id = i.get("SYSTEM_ID", 0)
        ecs_mem = ecs_mem_rate(system_id)
        ecs_cpu = ecs_cpu_rate(system_id)
        ecs_rate = ecs_disk_rate(system_id)
        ecs_read = ecs_disk_read(system_id)
        ecs_write = ecs_disk_write(system_id)
        if ecs_mem or ecs_cpu or ecs_rate or ecs_read or ecs_write:
            i['status'] = "告警"
        else:
            i['status'] = "正常"
    return render(request, "index.html", {"data_list":data_list})

def article(request):
    system_id = request.GET.get('system_id')
    ecs_mem = ecs_mem_rate(system_id)
    ecs_cpu = ecs_cpu_rate(system_id)
    ecs_rate = ecs_disk_rate(system_id)
    ecs_read = ecs_disk_read(system_id)
    ecs_write = ecs_disk_write(system_id)
    data_list = {}
    mem_str = ""
    cpu_str = ""
    rate_str = ""
    read_str = ""
    write_str = ""
    if ecs_mem:
        mem_str += "ECS内存使用过大的ip：\n"
        i1 =0
        for i in ecs_mem:
            i1 += 1
            mem_str += str(i.get("IP_ADDR", "")+";")
            if i1 % 5 == 0 or i1 == len(ecs_mem):
                mem_str += "\n"
    if ecs_cpu:
        cpu_str += "\nECS的CPU使用过大的ip：\n"
        for j in ecs_cpu:
            cpu_str += str(j.get("IP_ADDR", "") + ";")
    if ecs_rate:
        rate_str += "\n磁盘使用率过大的ip：\n"
        k1 = 0
        for k in ecs_rate:
            k1 += 1
            rate_str += str(k.get("IP_ADDR", "") + ";")
            if k1 % 10 == 0 or k1 == len(ecs_rate):
                rate_str += "\n"
    if ecs_read:
        read_str += "\n磁盘读取字节数过大的ip：\n"
        m1 = 0
        for m in ecs_mem:
            m1 += 1
            read_str += str(m.get("IP_ADDR", "") + ";")
            if m1 % 10 == 0 or m1 == len(ecs_read):
                read_str += "\n"
    if ecs_write:
        write_str += "\n磁盘写入字节数过大的ip：\n"
        n1 = 0
        for n in ecs_mem:
            n1 += 1
            write_str += str(n.get("IP_ADDR", "") + ";")
            if n1 % 10 == 0 or n1 == len(ecs_write):
                write_str += "\n"
    system = TSystem.objects.filter(id=system_id).first()
    data_list['system_name'] = system.system_name
    data_list['mem_str'] = mem_str
    data_list['cpu_str'] = cpu_str
    data_list['rate_str'] = rate_str
    data_list['read_str'] = read_str
    data_list['write_str'] = write_str
    data_list['SYSTEM_ID'] = system_id
    return render(request, "detail.html", {"data_list": data_list})

def download_file(request):
    system_id = request.GET.get('system_id')
    ecs_mem = ecs_mem_rate(system_id)
    ecs_cpu = ecs_cpu_rate(system_id)
    ecs_rate = ecs_disk_rate(system_id)
    ecs_read = ecs_disk_read(system_id)
    ecs_write = ecs_disk_write(system_id)
    mem_str = ""
    cpu_str = ""
    rate_str = ""
    read_str = ""
    write_str = ""
    if ecs_mem:
        mem_str += "ECS内存使用过大的ip：\n"
        i1 = 0
        for i in ecs_mem:
            i1 += 1
            mem_str += str(i.get("IP_ADDR", "") + ";")
            if i1 % 5 == 0 or i1 == len(ecs_mem):
                mem_str += "\n"
    if ecs_cpu:
        cpu_str += "\nECS的CPU使用过大的ip：\n"
        for j in ecs_cpu:
            cpu_str += str(j.get("IP_ADDR", "") + ";")
    if ecs_rate:
        rate_str += "\n磁盘使用率过大的ip：\n"
        k1 = 0
        for k in ecs_rate:
            k1 += 1
            rate_str += str(k.get("IP_ADDR", "") + ";")
            if k1 % 10 == 0 or k1 == len(ecs_rate):
                rate_str += "\n"
    if ecs_read:
        read_str += "\n磁盘读取字节数过大的ip：\n"
        m1 = 0
        for m in ecs_mem:
            m1 += 1
            read_str += str(m.get("IP_ADDR", "") + ";")
            if m1 % 10 == 0 or m1 == len(ecs_read):
                read_str += "\n"
    if ecs_write:
        write_str += "\n磁盘写入字节数过大的ip：\n"
        n1 = 0
        for n in ecs_mem:
            n1 += 1
            write_str += str(n.get("IP_ADDR", "") + ";")
            if n1 % 10 == 0 or n1 == len(ecs_write):
                write_str += "\n"
    response = HttpResponse(content_type='text/plain')   #定义输出格式为txt
    response['Content-Disposition'] = 'attachment; filename=my.txt'   #规定文件名字
    system = TSystem.objects.filter(id=system_id).first()
    content = mem_str + "\n" + cpu_str + "\n" + rate_str + "\n" + read_str + "\n" + write_str
    response.write("系统名称："+ str(system.system_name))
    response.write("\n")
    response.write("故障原因：" + content)
    return response
