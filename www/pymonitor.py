# -*- coding: utf-8 -*-
# @Author: Xusen
# @Date:   2017-05-23 20:52:28
# @Last Modified by:   Xusen
# @Last Modified time: 2017-05-24 15:49:36
import os
import sys
import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


def log(s):
    print('[Monitor] %s' % s)


class MyFileSystemEventHander(FileSystemEventHandler):

    def __init__(self, fn):
        super(MyFileSystemEventHander, self).__init__()
        self.restart = fn

    def on_any_event(self, event):
        if event.src_path.endswith('.py'):
            log('Python source file changed: %s' % event.src_path)
            self.restart()

        if event.src_path.endswith('.html'):
            log('Html templates file changed: %s' % event.src_path)
            self.restart()

command = ['echo', 'ok']
process = None


def kill_process():
    global process
    if process:
        log('Kill process [%s]...' % process.pid)
        process.kill()
        process.wait()
        log('Process ended with code %s.' % process.returncode)
        process = None


def start_process():
    global process, command
    log('Start process %s...' % ' '.join(command))
    process = subprocess.Popen(
        command, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr)


def restart_process():
    kill_process()
    start_process()


def start_watch(path, callback):
    observer = [Observer() for p in path]
    for p, ob in zip(path, observer):
        ob.schedule(MyFileSystemEventHander(
            restart_process), p, recursive=True)
        ob.start()
        log('Watching directory %s...' % p)
    start_process()
    try:
        while True:
            time.sleep(0.5)
    except KeyboardInterrupt:
        for o in observer:
            o.stop()
    for o in observer:
        o.join()

if __name__ == '__main__':
    argv = sys.argv[1:]
    if not argv:
        print('Usage: ./pymonitor your-script.py')
        exit(0)
    if argv[0] != 'python':
        argv.insert(0, 'python')
    command = argv
    path_www = os.path.abspath('.')
    path_templates = '\\'.join([path_www, 'templates'])
    start_watch([path_www, path_templates], None)
