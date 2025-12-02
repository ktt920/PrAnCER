# PrAnCER

Automated gait tracking of rodents, gait parameter extraction, and manual curation of rodent gait 
data.

## Getting Started
[Due to newer versions of the package have certain function deprecated, the setup need to specify some older, compatible package.]

### Prerequisites
The system has been tested on windows and mac environments.

### Installing
First, install Anaconda (Python 3.6 version).

If desired, create a new environment for running PrAnCER

```
(base) PS C:\Users\name> conda create -n prancer python=3.8
(base) PS C:\Users\name> conda activate prancer
(prancer) PS C:\Users\name> pip install numpy==1.19.5 opencv-python==3.4.18.65
(prancer) PS C:\Users\name> conda install -c conda-forge pims
(prancer) PS C:\Users\name> conda install -c conda-forge av
(prancer) PS C:\Users\name> conda install pandas
(prancer) PS C:\Users\name> conda install matplotlib
(prancer) PS C:\Users\name>pip install --no-cache-dir pillow
```

Clone the git repository (you'll need git installed)

```
git clone https://github.com/hayleybounds/PrAnCER.git
```
