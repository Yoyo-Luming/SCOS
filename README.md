# Selection of Compiler Optimization Sequence based on Evolutionary Algorithms

A Demo Project of using evolutionary algorithms to solve the compiler optimization sequence selection problem.

### DataSet
We use PolyBench and cBench from [ctuning-programs](https://github.com/ctuning/ctuning-programs).

### Installation

```shell
 $ pip install ck
 $ ck pull ck pull repo:ck-env
 $ ck pull repo:ck-autotuning
 $ ck pull repo:ctuning-programs
 $ ck pull repo:ctuning-datasets-min
```
Then you compile and run programs in datasets as follows:
```shell
$ ck compile program:cbench-automotive-susan --speed
$ ck run program:cbench-automotive-susan
```

### Basic Usage
> python GA.py