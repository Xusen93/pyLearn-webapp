# -*- coding: utf-8 -*-
# @Author: Xusen
# @Date:   2017-05-17 17:05:09
# @Last Modified by:   Xusen
# @Last Modified time: 2017-05-17 17:07:36
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
async def index(request):
    users = await User.findAll()
    return{
        '__template__': 'test.html',
        'users': users
    }
