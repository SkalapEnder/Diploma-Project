def process_request(req: dict) -> dict:
    #print("Backend received:", req)

    result_paths = [path + "_processed" for path in req["image_paths"]]

    return {
        "success": True,
        "result_paths": result_paths,
        "message": "Processed successfully"
    }