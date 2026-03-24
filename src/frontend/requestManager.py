from dataclasses import dataclass, asdict
from typing import List, Dict, Any
import uuid
import time


@dataclass
class ImageRequest:
    id: str
    image_paths: List[str]
    operation: str
    params: Dict[str, Any]


@dataclass
class ImageResponse:
    id: str
    success: bool
    result_paths: List[str]
    message: str
    time_ms: float


class RequestManager:
    def __init__(self, backend):
        self.backend = backend

    # CREATE
    def create_request(self, image_paths, operation, params) -> ImageRequest:
        return ImageRequest(
            id=str(uuid.uuid4()),
            image_paths=image_paths,
            operation=operation,
            params=params
        )

    # SEND
    def send_request(self, request: ImageRequest) -> ImageResponse:
        start_time = time.time()

        try:
            # Convert to dict (important for pybind11)
            request_dict = asdict(request)

            result = self.backend.process_request(request_dict)

            response = ImageResponse(
                id=request.id,
                success=result.get("success", True),
                result_paths=result.get("result_paths", []),
                message=result.get("message", ""),
                time_ms=(time.time() - start_time) * 1000
            )

        except Exception as e:
            response = ImageResponse(
                id=request.id,
                success=False,
                result_paths=[],
                message=str(e),
                time_ms=(time.time() - start_time) * 1000
            )

        return response

    def process(self, image_paths, operation, params) -> ImageResponse:
        request = self.create_request(image_paths, operation, params)
        return self.send_request(request)