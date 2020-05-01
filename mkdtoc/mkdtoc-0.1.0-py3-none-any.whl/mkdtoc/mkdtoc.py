"""
Make table of contents automatically.
"""
import re
import uuid
from typing import List, Optional
from dataclasses import dataclass

# <a href="#user-content-some-heading" id="some-heading">#</a>


TOC_BEGIN = '<!-- TOC BEGIN -->'
TOC_END = '<!-- TOC END -->'


@dataclass(frozen=True)
class Header:
    n: int
    title: str
    _id: str

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return (
            self.n == other.n and
            self.title == other.title
        )

    def to_line(self) -> str:
        return '{} {} {}'.format(
            '#' * self.n,
            self.title,
            f'<a href="#{self._id}" id="{self._id}">#</a>',
        )

    @classmethod
    def of_line(cls, line: str) -> Optional['Header']:
        if not line.startswith('#'):
            return None
        m = re.search(r'^(?P<sharps>#+)( *)(?P<title>[^<]*)', line)
        if m is None:
            return None
        return Header(
            n=len(m.group('sharps')),
            title=m.group('title'),
            _id=str(uuid.uuid1()),
        )


@dataclass()
class TocBuilder:

    headers: List[Header]

    def build(self) -> List[str]:
        lines = []
        for header in self.headers:
            lines.append('{}- {}'.format(
                ' '*((header.n-1)*2),
                f'<a href="#{header._id}">{header.title}</a>',
            ))
        return lines


def insert_toc_lines(lines: List[str], toc_lines: List[str]) -> List[str]:
    res_lines = list(lines)
    if TOC_BEGIN in lines and TOC_END in lines:
        # If already exists
        toc_begin_index = lines.index(TOC_BEGIN)
        toc_end_index = lines.index(TOC_END)
        res_lines[toc_begin_index+1:toc_end_index] = toc_lines
        return res_lines
    else:
        # Non existing TOC
        res_lines[0:0] = [
            '# Table of Contens',
            '',
            TOC_BEGIN,
        ] + toc_lines + [
            '',
            TOC_END,
            '',
        ]
        return res_lines


def make_toc(lines: List[str]) -> str:
    """
    Make TOCed content for a given markdown file path.
    """
    res_lines: List[str] = []
    builder = TocBuilder([])
    for line in lines:
        line = line.strip()
        header = Header.of_line(line)
        res_lines.append(
            line if header is None else header.to_line()
        )
        if header is not None:
            builder.headers.append(header)
    return ('\n'.join(
        insert_toc_lines(res_lines, builder.build())
    ))


def main() -> None:
    lines: List[str] = []
    while(True):
        try:
            line = input()
        except Exception:
            break
        lines.append(line)
    print(make_toc(lines))
