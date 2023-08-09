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

from django.db import models

# Create your models here.
class TSystem(models.Model):
    system_code = models.CharField('系统编码', max_length=100)
    system_name = models.CharField('系统名称', max_length=100)

    class Meta:
        db_table = 't_system'
        verbose_name = '系统'

class RrdDay(models.Model):
    rrd_id = models.IntegerField(primary_key=True)
    ne_name = models.CharField('名称', max_length=400)
    attribute_code = models.CharField('编码', max_length=400)
    avg_value = models.FloatField('平均值')
    max_value = models.FloatField('最大值')
    min_value = models.FloatField('最小值')

    class Meta:
        db_table = 'd_rrd_day_new'


class AssetInfo(models.Model):
    ASSET_ID = models.IntegerField(primary_key=True)
    NE_ID = models.IntegerField()
    SYSTEM_ID = models.IntegerField()
    IP_ADDR = models.CharField('IP地址', max_length=128)

    class Meta:
        db_table = 't_asset_info'

