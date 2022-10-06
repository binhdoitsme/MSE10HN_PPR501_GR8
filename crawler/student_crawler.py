from dataclasses import dataclass
from pathlib import Path
from typing import NamedTuple, Union

PathOrStr = Union[Path, str]

class StudentListCrawlingResult(NamedTuple):
    ...


@dataclass
class StudentListCrawler:
    host: str
    endpoint: str

    def crawl(self) -> StudentListCrawlingResult:
        ...
