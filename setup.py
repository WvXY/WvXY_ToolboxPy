from setuptools import find_packages, setup

setup(
    name="w_tbx",
    packages=find_packages("w_tbx"),
    package_dir={"": "w_tbx"},
    install_requires=["moderngl", "moderngl_window", "numpy", "torch", "pyrr"],
    version="0.5",
    description="A personal Python toolbox for my research prototypes",
    author="WvXY",
)

if __name__ == "__main__":
    setup()
