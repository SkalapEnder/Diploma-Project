import backend

from pathlib import Path

import sys


BACKEND_DIR = Path(__file__).resolve().parent.parent / "backend"

sys.path.append(str(BACKEND_DIR))


class BackendEntry:

    @staticmethod
    def process(image_paths, interpolation, params, model_name="EDSR" ):

        request = {
            "image_paths": image_paths,
            "interpolation": interpolation,
            "params": params,
            "model_name": model_name
        }

        response = my_backend.process_request(request)
        return response