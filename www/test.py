# -*- coding: utf-8 -*-
# @Author: Xusen
# @Date:   2017-05-15 14:45:04
# @Last Modified by:   Xusen
# @Last Modified time: 2017-05-15 20:51:38

import orm
import asyncio
from models import User, Blog, Comment


async def test(loop):
    await orm.create_pool(loop=loop, user='www-data', password='www-data', db='awesome')

    u = User(name='Test', email='test@example.com',
             passwd='1234567890', image='about:blank')

    await u.save()


async def test1(loop):
    await orm.create_pool(loop=loop, user='www-data', password='www-data', db='awesome')

    u = User(name='Test1', email='test1@example.com',
             passwd='1234567890', image='about:blank')

    await u.save()


loop = asyncio.get_event_loop()
loop.run_until_complete(test1(loop))
loop.close()