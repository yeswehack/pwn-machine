# import asyncio
# import pty
#
# class Shell:
#     def __init__(self):
#         pass
#
#
#     def run(cmd):
#         pid, fd = pty.fork()
#         if pid == 0:
#             subprocess.run(cmd)
#             exit(0)
#         else:
#             shell = cls(name, str(uuid4()), fd)
#             socketio.start_background_task(target=lambda: shell._runner())
#             shell.created()
#             return shell
#
#
# async def run(cmd):
#     proc = await asyncio.create_subprocess_shell(
#         cmd,
#         stdin=asyncio.subprocess.PIPE,
#         stdout=asyncio.subprocess.PIPE,
#         stderr=asyncio.subprocess.PIPE)
#     print("dir", dir(proc.stdin))
#     stdout, stderr = await proc.communicate(b"pouet\n")
#     print(f'[{cmd!r} exited with {proc.returncode}]')
#     if stdout:
#         print(f'[stdout]\n{stdout.decode()}')
#     if stderr:
#         print(f'[stderr]\n{stderr.decode()}')
#
# async def main():
#     await run("while true; do echo pouet; sleep 1; done")
#
# asyncio.run(main())
import pty
from subprocess import Popen, PIPE


def run(cmd):
    r = pty.spawn(["ls", "-l"])
    print(r)


run(4)
