from dataclasses import dataclass, asdict
from typing import List, Dict, Any
import uuid
import time
import sys
from pathlib import Path

from backend import backend_module


@dataclass
class ImageRequest:
    id: str
    image_paths: List[str]
    params: Dict[str, Any]


@dataclass
class ImageResponse:
    id: str
    success: bool
    result_paths: List[str]
    results: List[Dict[str, Any]]
    message: str
    time_ms: float



class RequestManager:
    def create_request(self, image_paths, params) -> ImageRequest:
        return ImageRequest(
            id=str(uuid.uuid4()),
            image_paths=image_paths,
            params=params
        )

    def send_request(self, request: ImageRequest) -> ImageResponse:

        start_time = time.time()

        try:
            request_dict = {
                "id": request.id,
                "image_paths": request.image_paths,
                "params": request.params,
            }

            result = backend_module.process_request(request_dict)

            result_items = result.get("results", [])

            result_paths = [item["output_path"] for item in result_items]

            response = ImageResponse(
                id=request.id,
                success=result.get("success", True),
                result_paths=result_paths,
                results=result_items,
                message=result.get("message", ""),
                time_ms=(time.time() - start_time) * 1000
            )

        except Exception as e:
            response = ImageResponse(
                id=request.id,
                success=False,
                result_paths=[],
                results=[],
                message=str(e),
                time_ms=(time.time() - start_time) * 1000
            )

        return response

    # -------------------------------------------------
    # Full Processing Shortcut
    # -------------------------------------------------

    def process(self, image_paths, params) -> ImageResponse:

        request = self.create_request(
            image_paths=image_paths,
            params=params
        )

        return self.send_request(request)