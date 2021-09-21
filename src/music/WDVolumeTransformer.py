import audioop

import discord.player
from discord import ClientException


class WDVolumeTransformer(discord.player.PCMVolumeTransformer):
    """Transforms a previous :class:`AudioSource` to have volume controls.

    This does not work on audio sources that have :meth:`AudioSource.is_opus`
    set to ``True``.

    Parameters
    ------------
    original: :class:`AudioSource`
        The original AudioSource to transform.
    volume: :class:`float`
        The initial volume to set it to.
        See :attr:`volume` for more info.

    Raises
    -------
    TypeError
        Not an audio source.
    ClientException
        The audio source is opus encoded.
    """

    time: int = 0

    def __init__(self, original: discord.FFmpegAudio, volume: float=float(1.0)) -> None:
        if not isinstance(original, discord.AudioSource):
            raise TypeError('expected AudioSource not {0.__class__.__name__}.'.format(original))

        if original.is_opus():
            raise ClientException('AudioSource must not be Opus encoded.')

        self.original = original
        self.volume = volume

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
        return audioop.mul(ret, 2, min(self._volume, 2.0))