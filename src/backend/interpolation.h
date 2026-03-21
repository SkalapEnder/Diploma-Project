#ifndef INTERPOLATION_H
#define INTERPOLATION_H

#include "image.h"

enum class InterpolationMethod {
    Nearest = 0,
    Bilinear = 1,
    Bicubic = 2,
    Lanczos = 3
};

Image resizeImage(
    const Image& input,
    int newWidth,
    int newHeight,
    InterpolationMethod method
);

#endif
