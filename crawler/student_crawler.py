from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List, Union

import requests
from bs4 import BeautifulSoup
from business.domain.student import Student, StudentId

PathOrStr = Union[Path, str]

PRETTY_FORMAT = """
ID {id} -- Student {fullname}
++ Date of Birth: {dob}
++ Hometown: {hometown}
++ Email: {email}
++ Final mark: {final_mark}
"""


def pretty_print(student: Student):
    return PRETTY_FORMAT.format(
        id=student.id.value,
        fullname=student.fullname,
        dob=student.dob,
        email=student.email,
        hometown=student.hometown,
        final_mark=student.final_mark,
    )


@dataclass
class CrawlerService:
    host: str
    endpoint: str
    handler: BeautifulSoup = None

    def crawl(self) -> str:
        with requests.get(f"{self.host}{self.endpoint}") as response:
            self.handler = BeautifulSoup(response.content, "html.parser")
        
        crawled: List[Student] = []

        for row in self.handler.select("tr.student-info"):
            cells = row.select("td")
            id = int(cells[1].text)
            first_name = cells[2].text
            last_name = cells[3].text
            email = cells[4].text
            dob = datetime.strptime(cells[5].text, "%Y-%m-%d").date()
            hometown = cells[6].text
            final_mark = float(cells[7].text)
            student = Student(
                id=StudentId(id),
                first_name=first_name,
                last_name=last_name,
                email=email,
                dob=dob,
                hometown=hometown,
                final_mark=final_mark,
            )
            crawled.append(student)
        return "\n".join(map(pretty_print, crawled)).strip()

    def __hash__(self) -> int:
        return id(self)
