#include "interpolation.h"
#include "interpolation.cpp"
#include "image.h"

Image resizeImage(
    const Image& input,
    int newWidth,
    int newHeight,
    InterpolationMethod method
) {
    switch (method) {
        case InterpolationMethod::Nearest:
            return resizeNearest(input, newWidth, newHeight);
        case InterpolationMethod::Bilinear:
            return resizeBilinear(input, newWidth, newHeight);
        default:
            return resizeNearest(input, newWidth, newHeight);
    }
}
