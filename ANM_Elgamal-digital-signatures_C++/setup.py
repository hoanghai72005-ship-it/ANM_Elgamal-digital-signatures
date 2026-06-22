from setuptools import setup, Extension
import pybind11

ext_modules = [
    Extension(
        'elgamal_core',
        ['elgamal_core.cpp'],
        include_dirs=[pybind11.get_include()],
        language='c++'
    ),
]

setup(
    name='elgamal_core',
    version='1.0',
    description='ElGamal C++ Core cho Tkinter GUI',
    ext_modules=ext_modules,
)