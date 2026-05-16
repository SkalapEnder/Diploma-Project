#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include <opencv2/opencv.hpp>
#include <opencv2/dnn_superres.hpp>

#include <filesystem>
#include <string>
#include <vector>
#include <chrono>
#include <cmath>
#include <iomanip>
#include <sstream>
#include <algorithm>
#include <cctype>

namespace py = pybind11;
namespace fs = std::filesystem;
fs::path results_dir = "results";


double computeMSE(const cv::Mat& I1, const cv::Mat& I2) {

    cv::Mat diff;

    cv::absdiff(I1, I2, diff);

    diff.convertTo(diff, CV_32F);
    diff = diff.mul(diff);

    cv::Scalar s = cv::sum(diff);

    double sse = s[0] + s[1] + s[2];

    double mse = sse / (double)(I1.channels() * I1.total());

    return mse;
}


double computePSNR(const cv::Mat& I1, const cv::Mat& I2) {

    double mse = computeMSE(I1, I2);

    if (mse <= 1e-10)
        return 100.0;

    double psnr =
        10.0 * log10((255.0 * 255.0) / mse);

    return psnr;
}


double computeSSIM(const cv::Mat& img1, const cv::Mat& img2) {
    if (img1.empty() || img2.empty() || img1.size() != img2.size()) 
        return 0.0;

    const double C1 = 6.5025;
    const double C2 = 58.5225;

    cv::Mat I1, I2;
    img1.convertTo(I1, CV_32F);
    img2.convertTo(I2, CV_32F);

    cv::Mat I1_2 = I1.mul(I1);
    cv::Mat I2_2 = I2.mul(I2);
    cv::Mat I1_I2 = I1.mul(I2);

    cv::Mat mu1, mu2;
    cv::GaussianBlur(I1, mu1, cv::Size(11, 11), 1.5);
    cv::GaussianBlur(I2, mu2, cv::Size(11, 11), 1.5);

    cv::Mat mu1_2 = mu1.mul(mu1);
    cv::Mat mu2_2 = mu2.mul(mu2);
    cv::Mat mu1_mu2 = mu1.mul(mu2);

    cv::Mat sigma1_2, sigma2_2, sigma12;
    cv::GaussianBlur(I1_2, sigma1_2, cv::Size(11, 11), 1.5);
    sigma1_2 -= mu1_2;

    cv::GaussianBlur(I2_2, sigma2_2, cv::Size(11, 11), 1.5);
    sigma2_2 -= mu2_2;

    cv::GaussianBlur(I1_I2, sigma12, cv::Size(11, 11), 1.5);
    sigma12 -= mu1_mu2;

    // Formula: SSIM = ((2*mu1*mu2 + C1)*(2*sigma12 + C2)) / ((mu1^2 + mu2^2 + C1)*(sigma1^2 + sigma2^2 + C2))
    cv::Mat t1 = (2 * mu1_mu2 + C1).mul(2 * sigma12 + C2);
    cv::Mat t2 = (mu1_2 + mu2_2 + C1).mul(sigma1_2 + sigma2_2 + C2);

    cv::Mat ssim_map;
    cv::divide(t1, t2, ssim_map);

    cv::Scalar mssim = cv::mean(ssim_map);

    // 2. Fix: Only average the actual channels present in the input
    int channels = img1.channels();
    double sum_ssim = 0;
    for (int i = 0; i < channels; i++) {
        sum_ssim += mssim[i];
    }

    return sum_ssim / static_cast<double>(channels);
}


int getInterpolation(int method) {
    switch (method) {
        case 0: return cv::INTER_NEAREST;
        case 1: return cv::INTER_LINEAR;
        case 2: return cv::INTER_CUBIC;
        case 4: return cv::INTER_LANCZOS4;

        default: return cv::INTER_CUBIC;
    }
}

std::string getNowTime(){
    auto now = std::chrono::system_clock::now();
    std::time_t t = std::chrono::system_clock::to_time_t(now);

    std::tm tm = *std::localtime(&t);

    // format: YYYY-MM-DD_HH-MM-SS
    std::ostringstream oss;
    oss << std::put_time(&tm, "%Y-%m-%d_%H-%M-%S");
    return oss.str();
}

std::string reGetInterpolation(int method) {
    switch (method) {
        case 0: return "Nearest Neighbor";
        case 1: return "Bilinear";
        case 2: return "Bicubic";
        case 4: return "Lanczos";
        case 10: return "Super-Resolution";
        default: return "Bicubic";
    }
}

std::string reGetInterpolation2(int method) {
    switch (method) {
        case 0: return "NN";
        case 1: return "Bilin";
        case 2: return "Bicun";
        case 4: return "Lanc";
        case 10: return "SR";
        default: return "Bicub";
    }
}

std::string make_output_name(
    const std::string& image_path,
    const std::string& mode,
    const std::string& interpolation,
    const std::string& format,
    double scale_first, double scale_second = -1.0)
{
    fs::path p(image_path);

    std::string stem = p.stem().string();

    std::string new_name;
        
    if(mode == "one_way"){
        new_name =
            stem + "_" +
            mode + "_" +
            interpolation + "_" +
            std::to_string(scale_first) +
            "_out." + format;
    }
    else if (mode == "reconstruction")
    {
        new_name =
            stem + "_" +
            mode + "_" +
            interpolation + "_" +
            std::to_string(scale_first) + "_" +
            std::to_string(scale_second) +
            "_out." + format;
    }
    else {
        new_name =
            stem + "_" +
            mode + "_" +
            interpolation +
            "_out." + format;
    }

    return new_name;
}

py::dict process_request(py::dict request) {
    py::dict response;
    py::dict aggregates;
    py::list results;

    try {
        std::vector<std::string> image_paths =
            request["image_paths"]
            .cast<std::vector<std::string>>();

        py::dict params =
            request["params"].cast<py::dict>();

        std::string mode =
            params["mode"].cast<std::string>();

        bool useAI =
            params.contains("ai") 
            && params["ai"].cast<bool>();

        std::string output_format =
            params.contains("output_format")
            ? params["output_format"].cast<std::string>()
            : "png";
        

        int interpolation1 =
            params.contains("interpolation")
            ? params["interpolation"].cast<int>()
            : 2;

        int interpolation = getInterpolation(interpolation1);

        // AI
        // ====================
        std::string model_name =
            params.contains("model_name")
            ? params["model_name"].cast<std::string>()
            : "EDSR";

        cv::dnn_superres::DnnSuperResImpl sr;

        if (useAI) {
            int ai_scale;
            if(mode == "one_way")
            {
                ai_scale = (int)params["scale"].cast<double>();
            }
            else
            {
                py::dict reconstruct = params["reconstruct"].cast<py::dict>();
                ai_scale = (int)reconstruct["second"].cast<double>();
            }

            std::string model_filename;

            if (model_name == "edsr") {
                model_filename =
                    "models/EDSR_x" +
                    std::to_string(ai_scale) +
                    ".pb";
            }
            else if (model_name == "espcn") {

                model_filename =
                    "models/ESPCN_x" +
                    std::to_string(ai_scale) +
                    ".pb";
            }
            else if (model_name == "fsrcnn") {

                model_filename =
                    "models/FSRCNN_x" +
                    std::to_string(ai_scale) +
                    ".pb";
            }
            else if (model_name == "lapsrn") {

                model_filename =
                    "models/LapSRN_x" +
                    std::to_string(ai_scale) +
                    ".pb";
            }
            else
                throw std::runtime_error("Unknown AI model: " + model_name);


            // Load model
            // ====================
            //throw std::runtime_error(model_filename);
            std::transform(model_name.begin(), model_name.end(), model_name.begin(), 
                   [](unsigned char c){ return std::tolower(c); });
            sr.readModel(model_filename);
            sr.setModel(model_name, (int)ai_scale);
        }
        
        // Processing loop
        // ====================
        double mse, psnr, ssim;
        double scale_first, scale_second = -1.0;

        if (!fs::exists(results_dir)) {
            fs::create_directory(results_dir);
        }

        fs::path run_folder = results_dir / (mode + "_" + getNowTime());
        fs::create_directories(run_folder);

        for (const auto& path : image_paths) {
            auto start = std::chrono::high_resolution_clock::now();
            
            // Load image
            // ====================
            cv::Mat img = cv::imread(path);

            if (img.empty()) {
                throw std::runtime_error("Failed to load image: " + path);
            }

            py::dict item;

            item["width_init"] = img.cols;
            item["height_init"] = img.rows;

            cv::Mat output;

            mse = 0.0;
            psnr = 0.0;
            ssim = 0.0;

           // Processing
            // ====================
            if (mode == "one_way") {
                scale_first = params["scale"].cast<double>();
                item["scale"] = scale_first;
                
                if (useAI) 
                    sr.upsample(img, output);
                else 
                    cv::resize(img, output, cv::Size(), scale_first, scale_first, interpolation);
                
            } 

            else if (mode == "reconstruct") {
                py::dict reconstruct = params["reconstruct"].cast<py::dict>();
                scale_first = reconstruct["first"].cast<double>();
                scale_second = reconstruct["second"].cast<double>();

                item["scale_first"] = scale_first;
                item["scale_second"] = scale_second;

                cv::Mat intermediate;

                cv::resize(img, intermediate, cv::Size(), scale_first, scale_first, interpolation);

                item["width_inter"] = intermediate.cols;
                item["height_inter"] = intermediate.rows;


                if (useAI && (scale_second == 2.0 || scale_second == 3.0 || scale_second == 4.0)) {
                    sr.upsample(intermediate, output);
                } else {
                    cv::resize(intermediate, output, cv::Size(), scale_second, scale_second, interpolation);
                }
            }

            else if (mode == "custom") {
                py::dict custom = params["custom"].cast<py::dict>();

                int width = custom["width"].cast<int>();
                int height = custom["height"].cast<int>();

                cv::resize(img, output, cv::Size(width, height), 0, 0, interpolation);
            }

            // Save image
            // ====================
            std::string output_name = make_output_name(
                path, mode, reGetInterpolation2(interpolation), output_format, scale_first, scale_second);
                
            fs::path output_path = run_folder / output_name;
            
            cv::imwrite(output_path.string(), output);

            // Timing
            // ====================
            auto end = 
                std::chrono::high_resolution_clock::now();

            double time_ms =
                std::chrono::duration<double, std::milli>(end - start).count();
            
            item["width_res"] = output.cols;
            item["height_res"] = output.rows;
            item["throughput"] = (output.cols * output.rows) / (time_ms / 1000.0);
            
            // Fixer code for metrics
            if (output.size() != img.size()) {
                cv::resize(output, output, img.size(), 0, 0, cv::INTER_CUBIC);
            }

            if (output.channels() != img.channels()) {
                if (output.channels() == 1 && img.channels() == 3)
                    cv::cvtColor(output, output, cv::COLOR_GRAY2BGR);
                
                else if (output.channels() == 3 && img.channels() == 1)
                    cv::cvtColor(output, output, cv::COLOR_BGR2GRAY);
                
            }

            mse = computeMSE(img, output);
            psnr = computePSNR(img, output);
            ssim = computeSSIM(img, output);

            // Result item
            // ====================
            item["mode"] = mode;
            item["interpolation"] = reGetInterpolation(interpolation1);
            item["time_ms"] = time_ms;

            item["mse"] = mse;
            item["psnr"] = psnr;
            item["ssim"] = ssim;

            item["total_images"] = image_paths.size();
            item["used_ai"] = useAI;
            item["model_name"] =  useAI ? model_name : "-";

            item["input_path"] = path;
            item["output_path"] = output_path.string();
            
            results.append(item);
        }

        response["success"] = true;
        response["results"] = results;
    }

    catch (const std::exception& e) {
        response["success"] = false;
        response["message"] = std::string(e.what());
    }

    return response;
}

// PYBIND11
// ====================
PYBIND11_MODULE(backend_module, m) {
    m.doc() = "Image Processing Backend";

    m.def(
        "process_request",
        &process_request,
        "Process images"
    );
}