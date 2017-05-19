# -*- coding: utf-8 -*-
# @Author: Xusen
# @Date:   2017-05-17 17:05:09
# @Last Modified by:   Xusen
# @Last Modified time: 2017-05-19 18:18:43
'url handlers'
import re
import time
import json
import logging
import hashlib
import base64
import asyncio
from coroweb import get, post
from models import User, Comment, Blog, next_id


@get('/')
def index(request):
    summary = 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.'
    blogs = [
        Blog(id='1', name='Awesome\'s Blog', summary=summary,
             created_at=time.time()-120),
        Blog(id='2', name='Something New',
             summary=summary, created_at=time.time()-3600),
        Blog(id='3', name='Learn Swift', summary=summary,
             created_at=time.time()-7200)
    ]
    return {
        '__template__': 'blogs.html',
        'blogs': blogs
    }
