from tempfile import NamedTemporaryFile
from typing import Any, Dict
from enum import Enum

from pydub import AudioSegment
import requests

__all__ = ['process']

ScriptType = Dict[str, Any]


def download_file(uri: str) -> str:
    r = requests.get(uri)
    assert r.status_code in (200, 201)

    with NamedTemporaryFile(mode='wb', delete=False) as tmpf:
        tmpf.write(r.content)
        return tmpf.name


class CmdType(Enum):
    FILE = 'file'
    CONCAT = 'cat'
    SILENCE = 'silence'
    OVERLAY = 'overlay'
    BYPASS = '_bypass'

    @staticmethod
    def from_val(val):
        return next((label for label in CmdType if label.value == val), None)


def require_field(cmd, cmd_type, field_name):
    assert field_name in cmd, f'Every "{cmd_type}" command must contain a field "{field_name}"'


def _process(cmd) -> AudioSegment:
    cmd_type = CmdType.from_val(cmd.get('type', CmdType.BYPASS.value)) if not isinstance(
        cmd, list) else CmdType.CONCAT

    if cmd_type == CmdType.BYPASS:
        if 'audio' not in cmd:
            require_field(cmd, cmd_type, 'audio')
        audio = _process(cmd['audio'])

    elif cmd_type == CmdType.FILE:
        require_field(cmd, cmd_type, 'src')
        file_src = cmd['src']
        if file_src.startswith('http://') or file_src.startswith('https://'):
            file_src = download_file(file_src)
        audio = AudioSegment.from_file(file_src) + cmd.get('gain', 0)

    elif cmd_type == CmdType.CONCAT:
        audio = AudioSegment.empty()
        for sub_cmd in cmd:
            audio += _process(sub_cmd)

    elif cmd_type == CmdType.SILENCE:
        require_field(cmd, cmd_type, 'duration')
        duration = cmd['duration']
        audio = AudioSegment.silent(duration=duration)

    elif cmd_type == CmdType.OVERLAY:
        require_field(cmd, cmd_type, 'audio')
        overlay_tracks = cmd['audio']

        audio_segments = [_process(track['audio']) for track in overlay_tracks]

        # left padding
        audio = AudioSegment.silent(
            duration=cmd['audio'][0].get('start', 0)) + audio_segments[0]

        for audio_seg, track in zip(audio_segments[1:], overlay_tracks[1:]):
            start_position = track.get('start', 0)
            gain = track.get('gain', 0)
            audio = audio.overlay(
                audio_seg, position=start_position, gain_during_overlay=gain)

    else:
        raise Exception(f'{cmd_type} not implemented')

    # add effects
    if 'fade_out' in cmd:
        duration = cmd['fade_out']
        audio = audio.fade_out(duration)
    elif 'fade_in' in cmd:
        duration = cmd['fade_in']
        audio = audio.fade_in(duration)

    return audio


def process(script: ScriptType) -> AudioSegment:
    '''
    example input:
    {
      "version": "3",
      "audio": [{
        "type": "overlay",
        "audio": [
            {
                "name": "intro",
                "audio": [
                    {"src": "https://source.com/1.wav", "gain": -5},
                    {"type": "silence", "duration": 3000},
                ]
            },
            {
                "name": "body",
                "start": 400,
                "audio": [
                    {"src": "local/dir/2.mp3"}
                ]
            }
        ]
      }]
    }
    '''
    version = script.get('version', '1')
    assert version == '3', 'Version must be exactly 3.'
    assert 'audio' in script, 'Script must contain an audio section.'

    return _process(script['audio'])
