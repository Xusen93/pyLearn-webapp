# -*- coding: utf-8 -*-
# @Author: Xusen
# @Date:   2017-05-23 20:52:28
# @Last Modified by:   Xusen
# @Last Modified time: 2017-05-24 20:34:41
import os
import sys
import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


def log(s):
    print('[Monitor] %s' % s)


class MyFileSystemEventHander(FileSystemEventHandler):

    def __init__(self, fn, filetype):
        super(MyFileSystemEventHander, self).__init__()
        self.restart = fn
        self.filetype = filetype

    def on_any_event(self, event):
        if event.src_path.endswith(self.filetype):
            log('%s file changed: %s' % (self.filetype, event.src_path))
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
    process = subprocess.Popen(
        command, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr)
    log('Start process [%s] at %s >>> %s' % (process.pid, time.strftime(
        '%Y-%m-%d %H:%M:%S', time.localtime(time.time())), ' '.join(command)))


def restart_process():
    kill_process()
    start_process()


def start_watch(path, filetype, callback):
    observer = [Observer() for p in path]
    for p, ob, ft in zip(path, observer, filetype):
        ob.schedule(MyFileSystemEventHander(
            restart_process, ft), p, recursive=True)
        ob.start()
        log('Watching %s files in %s...' % (ft, p))
    start_process()
    try:
        while True:
            time.sleep(0.5)
    except KeyboardInterrupt:
        for ob in observer:
            ob.stop()
    for ob in observer:
        ob.join()

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
    path = [path_www, path_templates]
    filetype = ['.py', '.html']
    # monitor \www\*.py,\www\templates\*.html
    start_watch(path, filetype, None)
