### Introduction

Minimal example of how to generate an *.exe* executable using [PyInstaller](https://pyinstaller.org/) that can run [Manga-Ocr](https://github.com/kha-white/manga-ocr). Due to Manga-Ocr's use of [PyTorch](https://pytorch.org/), it is not trivial to generate a correctly functioning and lightweight *.exe*.

The instructions provide a way to generate an executable that launches Manga-Ocr using the CPU for image processing, as well as instructions for generating an executable that launches Manga-Ocr to use the GPU ([Cuda](https://docs.nvidia.com/cuda/cuda-toolkit-release-notes/contents.html)).

We were able to successfully generate the executable by using [Poetry](https://python-poetry.org/) to create a Python Environment, as well as a custom modification of PyInstaller's *.spec* file to optimize the compilation .

### Instructions

0. Make sure to have **Python 3.9** installed (other versions may cause conflicts).
1. Install [Poetry](https://python-poetry.org/) if you don't have it.
2. Validate that it is correctly installed using: `poetry -v`
3. Create and activate the environment with: `poetry shell`
4. Install dependencies with: `poetry install`

**---Instructions to compile Manga-Ocr to use CPU for image processing---**
This compilation will result in a folder with an approximate weight of 650mb. If we compress the folder using WinRar, we can achieve a weight of 125mb.

5. Run the program with Python to validate its functionality: `python main.py`
6. Create the build using: `pyinstaller MangaOcrPyInstaller.spec`
7. The build can be found in directory */dist*. To run the program, click on "MangaOcrPyInstaller.exe"

**---Instructions to compile Manga-Ocr to use GPU (Cuda) for image processing---**
Since Manga-Ocr uses PyTorch, GPU acceleration will only work if the computer has an Nvidia [graphics card that supports Cuda](https://developer.nvidia.com/cuda-gpus). The graphics card drivers must be up to date. The build of Manga-Ocr with GPU usage is exponentially heavier. This compilation will result in a folder with an approximate weight of 4gb. If we compress the folder using WinRar, we can achieve a weight of 1.3gb.

5. Use `poe force-cuda11` to install extra dependencies for GPU usage. This will install *PyTorch 1.12*, *Torchvision 0.13*, and *Cuda 11.6* in our environment. This download is approximately 2.3gb
6. Run the program with Python to validate its functionality: `python main.py`. We should see a message indicating that the GPU (Cuda) is being used
7. Create the build using: `pyinstaller MangaOcrPyInstaller.spec`
8. The build can be found in directory */dist*. To run the program, click on "MangaOcrPyInstaller.exe"

### Considerations
* Manga-Ocr checks if we have the [models stored in our cache](https://github.com/kha-white/manga-ocr/issues/17). If they are not present, Manga-Ocr will download the models (approximately 400mb) before starting. Subsequent executions will be faster as the models will be cached
* If we use `poe force-cuda11` and want to uninstall those dependencies to switch back to using only the CPU, we should run `poe force-remove-cuda11` and then `poetry install`

### Others
- The *.spec* file was generated using [this solution](https://stackoverflow.com/questions/71863714/packagenotfound-error-while-executing-exe-file-made-by-pyinstaller) as a base. Then it was merged with [this](https://github.com/blueaxis/Cloe/blob/main/build/main.spec) implementation. Finally, it was manually validated which packages could be ignored.
- Achieving to install Cuda with Poetry was possible thanks to [this approach](https://stackoverflow.com/questions/59158044/poetry-and-pytorch).

### Todo
- See if it's possible to reduce the weight of the GPU mode compilation by ignoring certain *.dll* and/or *.lib* files related to Cuda

