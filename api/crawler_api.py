from functools import lru_cache
from io import BytesIO

from crawler.student_crawler import CrawlerService
from fastapi import APIRouter
from fastapi.responses import Response, StreamingResponse
from utils.responses import default_exception_handling


@lru_cache
def crawler_api(crawler: CrawlerService):
    router = APIRouter()

    @router.get("/students")
    @default_exception_handling
    def get_crawler_result():
        try:
            crawler_result = crawler.crawl().strip().encode("UTF-8")
            headers = {
                "Content-Type": "application/octet-stream",
                "Content-Disposition": """attachment;filename=\"students.txt\"""",
            }
            return StreamingResponse(
                content=BytesIO(crawler_result), headers=headers
            )
        except ConnectionError:
            return Response("Cannot connect to specified URL!", 500)

    return router
