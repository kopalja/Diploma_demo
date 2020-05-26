# Diploma demo

This repository is made to easly replicate the results presented in our thesis. It also contains C++ implementation 
of the IoUTraction algoritm as well as the compiled binaries for the x86, ARMv7 and AArch64 architectures.

## Getting Started

The followirng section describes the setup process of the enviroment to be able to run the following demo scripts.
* run_demo.sh: to generate graphs presented in the thesis.
* count_cars.py: to count the cars in the video by traction-by-detection algorithm and generate video with bounding boxes.

### Prerequisites

To run this demo it is necesary to have an Edge TPU device along with Edge TPU runtime succesfully installed.
To install Edge TPU related software see [Coral official documentation.](https://coral.ai/docs/accelerator/get-started)


### Installing

In addition to Edge TPU runtime we also need the following python packages:

```
numpy>=1.18.4
matplotlib>=3.2.1
Pillow>=7.1.2
opencv-python>=4.1.2.30
```

## Generating graphs

To generate an accuracy graphs all we need to do is to run the run_demo script with one parameter indicating which graph we want to generate e.g.,

```
./run_demo -n 1
```
to generate the first graph.
To see a detail description of the ./run_demo script run

```
./run_demo -h
```

## Counting cars

To count a number of cars in the given video run 

```
python count_cars.py --input <path to input video>
```

For more datail description of the count_cars.py script run

```
python count_cars.py --help
```

## Built With

* [Coral official documentation](https://coral.ai/docs/accelerator/get-started) - Edge TPU official documentation

## Credits
To evaluate mAP score for generated results we use the [Cartucho/mAP](https://github.com/Cartucho/mAP) implementation.

