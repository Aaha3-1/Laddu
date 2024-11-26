# Laddu // An AUR Helper
[![laddu](https://github.com/Aaha3-1/Laddu/actions/workflows/python-app.yml/badge.svg)](https://github.com/Aaha3-1/Laddu/actions/workflows/python-app.yml) [![Python 2.6|2.7|3.x](https://img.shields.io/badge/python-2.6|2.7|3.x-yellow.svg)](https://www.python.org/) [![License](https://img.shields.io/badge/license-GPLv2-red.svg)](https://raw.githubusercontent.com/Aaha3-1/Laddu/master/LICENSE)

`Laddu` Is a Small and Simple AUR Helper Which Was Programmed with Python

## Installation

to install Laddu, you can use the following script below:
```
sudo pacman -S --needed git base-devel
git clone --depth 1 https://github.com/Aaha3-1/Laddu
makepkg -si
```

## Usage

`Laddu` can be used to install various packages from the AUR, or Any other PKGBUILD on github, or in your Hardrive.

- To install any `AUR` package, use:
  ```
  laddu -S --aur/<package>
  ```
- To install any `github` PKGBUILD file, use:
  ```
  laddu -S <user>/<reponame>
  ```
- To install from `hardisk`, use:
  ```
  laddu -B <path>
  ```

 > [!WARNING]  
 > Don't install random packages without making sure it is safe.
 > Always check the `PKGBUILD` file in case you download a virus. 
