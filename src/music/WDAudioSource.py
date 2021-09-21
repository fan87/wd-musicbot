import audioop
import logging
import shlex
import subprocess
import sys
from typing import Any

import discord.player
import typing
from discord import ClientException
from discord.opus import Encoder

import wdutils.TimeParser

log: logging.Logger = logging.getLogger(__name__)

if sys.platform != 'win32':
    CREATE_NO_WINDOW = 0
else:
    CREATE_NO_WINDOW = 0x08000000

class WDVolumeTransformer(discord.player.PCMVolumeTransformer):

    time: int = 0

    def __init__(self, original: 'WDFFmpegAudio', volume: float=float(1.0)) -> None:
        if not isinstance(original, discord.AudioSource):
            raise TypeError('expected AudioSource not {0.__class__.__name__}.'.format(original))

        if original.is_opus():
            raise ClientException('AudioSource must not be Opus encoded.')

        self.original = original
        self.volume = volume

    def jump(self, milli: int) -> None:
        self.time = milli
        return self.original.jump(milli)

    @property
    def volume(self) -> float:
        """Retrieves or sets the volume as a floating point percentage (e.g. ``1.0`` for 100%)."""
        return self._volume

    @volume.setter
    def volume(self, value: float) -> None:
        self._volume = max(value, 0.0)

    def cleanup(self) -> None:
        self.original.cleanup()

    def read(self) -> bytes:
        ret = self.original.read()
        self.time += 20
        return audioop.mul(ret, 2, min(self._volume, 4.0))


class WDFFmpegAudio(discord.AudioSource):

    args: list[str] = []
    kwargs: dict = {}


    def read(self) -> bytes:
        raise NotImplementedError()

    process: typing.Optional[subprocess.Popen] = None
    stdout: typing.Optional[typing.IO] = None

    def jump(self, milli: int) -> None:
        raise NotImplementedError()

    def __init__(self, source: Any, *, executable: str='ffmpeg', args: Any, **subprocess_kwargs: Any) -> None:
        self._process = self.stdout = None

        args = [executable, *args]
        kwargs = {'stdout': subprocess.PIPE}
        kwargs.update(subprocess_kwargs)
        self.args = args
        self.kwargs = kwargs

        self.process = self.spawn_process(args, **kwargs)

        self.stdout = self.process.stdout

    def spawn_process(self, args: Any, **subprocess_kwargs: Any) -> subprocess.Popen[str]:
        process = None
        try:
            process = subprocess.Popen(args, creationflags=CREATE_NO_WINDOW, **subprocess_kwargs)
            t: str = ""
            for arg in args:
                t += arg + " "
        except FileNotFoundError:
            executable = args.partition(' ')[0] if isinstance(args, str) else args[0]
            raise ClientException(executable + ' was not found.') from None
        except subprocess.SubprocessError as exc:
            raise ClientException('Popen failed: {0.__class__.__name__}: {0}'.format(exc)) from exc
        else:
            return process

    def cleanup(self) -> None:
        proc = self._process
        if proc is None:
            return

        log.info('Preparing to terminate ffmpeg process %s.', proc.pid)

        try:
            proc.kill()
        except Exception:
            log.exception("Ignoring error attempting to kill ffmpeg process %s", proc.pid)

        if proc.poll() is None:
            log.info('ffmpeg process %s has not terminated. Waiting to terminate...', proc.pid)
            proc.communicate()
            log.info('ffmpeg process %s should have terminated with a return code of %s.', proc.pid, proc.returncode)
        else:
            log.info('ffmpeg process %s successfully terminated with return code of %s.', proc.pid, proc.returncode)

        self.process = self.stdout = None

class WDFFmpegPCMAudio(WDFFmpegAudio):


    def __init__(self, source: str, *, executable: str = 'ffmpeg', pipe: bool = False, stderr: Any = None, before_options: Any = None, options: Any = None) -> None:
        args = []
        subprocess_kwargs = {'stdin': source if pipe else subprocess.DEVNULL, 'stderr': stderr}

        if isinstance(before_options, str):
            args.extend(shlex.split(before_options))

        args.append('-i')
        args.append('-' if pipe else source)
        args.extend(('-f', 's16le', '-ar', '48000', '-ac', '2', '-loglevel', 'warning'))

        if isinstance(options, str):
            args.extend(shlex.split(options))

        args.append('pipe:1')

        super().__init__(source, executable=executable, args=args, **subprocess_kwargs)

    def jump(self, milli: int) -> None:
        args: list[str] = list[str]()
        i: int = 0
        for arg in self.args:
            i += 1
            args.append(arg)
            if i == 1:
                args.append("-ss")
                args.append(wdutils.TimeParser.parse_milli(milli))
        self.process = self.spawn_process(args, **self.kwargs)
        self.stdout = self.process.stdout



    def read(self) -> bytes:
        ret = typing.cast(typing.IO, self.stdout).read(Encoder.FRAME_SIZE)
        if len(ret) != Encoder.FRAME_SIZE:
            return b''
        return ret

    def is_opus(self) -> bool:
        return False
