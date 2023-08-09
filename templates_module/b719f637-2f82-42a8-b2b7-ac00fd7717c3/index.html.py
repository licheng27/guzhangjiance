# -*- coding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1691487915.470155
_enable_loop = True
_template_filename = '/framework_py/templates/index.html'
_template_uri = 'index.html'
_source_encoding = 'utf-8'
_exports = []


def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        __M_writer = context.writer()
        __M_writer('<!doctype html>\r\n<html lang="en">\r\n<head>\r\n    <meta charset="UTF-8">\r\n    <meta name="viewport"\r\n          content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">\r\n    <meta http-equiv="X-UA-Compatible" content="ie=edge">\r\n    <title>Document</title>\r\n</head>\r\n\r\n<body>\r\n\r\n<h1 id="h1">故障检测</h1>\r\n<table border="1px">\r\n    <tr>\r\n        <td>系统名称</td>\r\n        <td>状态</td>\r\n        <td>详情</td>\r\n\r\n    </tr>\r\n    {% for i in data_list %}\r\n        <tr>\r\n\r\n            <td align="center">{{ i.system_name }} </td>\r\n            <td align="center">{{ i.status }} </td>\r\n             <td align="center">\r\n                <a href="../sims/article/?system_id={{ i.SYSTEM_ID }}">\r\n                    编辑\r\n                </a>\r\n\r\n            </td>\r\n\r\n        </tr>\r\n    {% endfor %}\r\n</table>\r\n\r\n\r\n</body>\r\n</html>\r\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"filename": "D:/\u77f3\u5316\u667a\u4e91/2023-08\u6570\u636e/framework_3.3.1.92/framework_py/mako_templates/index.html", "uri": "index.html", "source_encoding": "utf-8", "line_map": {"16": 0, "21": 1, "27": 21}}
__M_END_METADATA
"""
