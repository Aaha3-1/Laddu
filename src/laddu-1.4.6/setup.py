from setuptools import setup, find_packages

setup(
    name='laddu',  # Name of your package
    version='1.4.6',  # Version of your package
    description='Laddu is a small, simple AUR Helper Built in Python.',
    author='Aaha3',
    author_email='Aaha3.sh@gmail.com',
    url='https://github.com/Aaha3-1/Laddu.git',
    packages=find_packages(),
    install_requires=[
        'colorama',
        'requests',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GPL3',
        'Operating System :: Arch Linux',
    ],
    python_requires='>=3.6',
)

