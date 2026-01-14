#include "interpolation.h"
#include <cmath>

Image resizeNearest(const Image& input, int newW, int newH) {
    Image output;
    output.width = newW;
    output.height = newH;
    output.channels = input.channels;
    output.data.resize(newW * newH * input.channels);

    float x_ratio = static_cast<float>(input.width) / newW;
    float y_ratio = static_cast<float>(input.height) / newH;

    for (int y = 0; y < newH; ++y) {
        for (int x = 0; x < newW; ++x) {
            int srcX = static_cast<int>(x * x_ratio);
            int srcY = static_cast<int>(y * y_ratio);

            for (int c = 0; c < input.channels; ++c) {
                output.data[(y * newW + x) * input.channels + c] =
                    input.data[(srcY * input.width + srcX) * input.channels + c];
            }
        }
    }
    return output;
}

Image resizeBilinear(const Image& input, int newW, int newH) {
    Image output;
    output.width = newW;
    output.height = newH;
    output.channels = input.channels;
    output.data.resize(newW * newH * input.channels);

    float x_ratio = static_cast<float>(input.width - 1) / newW;
    float y_ratio = static_cast<float>(input.height - 1) / newH;

    for (int y = 0; y < newH; ++y) {
        for (int x = 0; x < newW; ++x) {
            float gx = x * x_ratio;
            float gy = y * y_ratio;

            int x0 = static_cast<int>(gx);
            int y0 = static_cast<int>(gy);
            int x1 = std::min(x0 + 1, input.width - 1);
            int y1 = std::min(y0 + 1, input.height - 1);

            float dx = gx - x0;
            float dy = gy - y0;

            for (int c = 0; c < input.channels; ++c) {
                float p00 = input.data[(y0 * input.width + x0) * input.channels + c];
                float p10 = input.data[(y0 * input.width + x1) * input.channels + c];
                float p01 = input.data[(y1 * input.width + x0) * input.channels + c];
                float p11 = input.data[(y1 * input.width + x1) * input.channels + c];

                float value =
                    p00 * (1 - dx) * (1 - dy) +
                    p10 * dx * (1 - dy) +
                    p01 * (1 - dx) * dy +
                    p11 * dx * dy;

                output.data[(y * newW + x) * input.channels + c] =
                    static_cast<unsigned char>(value);
            }
        }
    }
    return output;
}
