# Diploma demo

This repository is made to easly replicate the results presented in our thesis. It also contains C++ implementation 
of the IoUTraction algoritm as well as the compiled binaries for the x86, ARMv7 and AArch64 architectures.

## Getting Started

The followirng section describes the setup process of the enviroment to be able to run the demo script.

### Prerequisites

To run this demo it is necesary to have an Edge TPU device along with Edge TPU runtime succesfully installed.
To install Edge TPU related software see [Coral official documentation.](https://coral.ai/docs/accelerator/get-started)


### Installing

In addition to Edge TPU runtime we also need the following python packages:

```
numpy>=1.18.4
matplotlib>=3.2.1
Pillow>=7.1.2
```

## Running a demo

To run a demo all we need to do is to run the run_demo script with one parameter indicating which graph we want to generate e.g.,

```
./run_demo -n 1
```
to generate a first graph.
To see a detail description of the ./run_demo script run

```
./run_demo -h
```


## Built With

* [Coral official documentation](https://coral.ai/docs/accelerator/get-started) - Edge TPU official documentation

## Credits
To evaluate mAP score for generated results we use the [Cartucho/mAP](https://github.com/Cartucho/mAP) implementation.

