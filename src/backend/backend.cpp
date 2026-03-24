#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <iostream>
#include <vector>
#include <string>

namespace py = pybind11;

py::dict process_request(py::dict req) {
    // Extract fields
    std::string id = req["id"].cast<std::string>();
    std::vector<std::string> image_paths = req["image_paths"].cast<std::vector<std::string>>();
    std::string operation = req["operation"].cast<std::string>();
    py::dict params = req["params"];

    std::cout << "Request ID: " << id << std::endl;
    std::cout << "Operation: " << operation << std::endl;

    // Example param
    double scale = 1.0;
    if (params.contains("scale")) {
        scale = params["scale"].cast<double>();
    }

    std::vector<std::string> result_paths;

    // 🔹 Process images (mock for now)
    for (const auto& path : image_paths) {
        std::cout << "Processing: " << path << std::endl;

        // Fake result (you'll replace with OpenCV later)
        result_paths.push_back(path + "_processed");
    }

    // Return result as dict
    py::dict response;
    response["success"] = true;
    response["result_paths"] = result_paths;
    response["message"] = "Processed in C++";

    return response;
}