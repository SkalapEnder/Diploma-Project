#ifndef IMAGE_H
#define IMAGE_H

#include <vector>

struct Image {
    int width;
    int height;
    int channels; // 1 = grayscale, 3 = RGB
    std::vector<unsigned char> data;
};

#endif
