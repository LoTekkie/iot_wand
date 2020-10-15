import platform
import os
import subprocess
import sys
import time
import signal

def mk_server_cmd(dir, module, new_terminal=True):
    import iot_wand.server.settings as _s

    system = platform.system()
    print(system)
    python = 'python'
    terminal_cmd = 'start cmd /K'
    if system == 'Linux':
        terminal_cmd = 'lxterminal -e'
        python = '%s' % os.path.join(dir, 'env/bin/python3')
    print(python)
    path_module = os.path.join(_s.DIR_BASE, module)
    if new_terminal:
        cmd = '%s %s %s %s' % (terminal_cmd, python, path_module, dir)
    else:
        cmd = '%s %s %s' % (python, path_module, dir)
    print(cmd)
    return cmd

def start_subprocess(cmd):
    return subprocess.Popen(cmd, shell=True)


def main(dir_top):
    cmd = mk_server_cmd(dir_top, 'server_manager.py')
    start_subprocess(cmd)

if __name__ == '__main__':
    print('Starting server manager...')
    dir_top = sys.argv[1]
    sys.path.append(dir_top)
    cmd = mk_server_cmd(dir_top, 'server.py', new_terminal=False)
    process = start_subprocess(cmd)
    try:
        while True:
            resp = process.poll()
            print(resp)
            if resp is not None:
                print('restarting process...')
                process = start_subprocess(cmd)
            time.sleep(2)

    except (Exception, KeyboardInterrupt, subprocess.CalledProcessError) as e:
        print(e)

