import os
import setuptools

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

install_requires = []
install_requires.append('imutils')
install_requires.append('opencv-python')
install_requires.append('python-multipart')

setuptools.setup(
    name="fastapi_frame_stream",
    version="0.1.0",
    author="Tiago Prata",
    author_email="prataaa@hotmail.com",
    description="Package to easily stream individual frames (MJPEG) using FastAPI",
    long_description_content_type='text/markdown',
    long_description=read('README.md'),
    url = "https://github.com/TiagoPrata/fastapi-frame-stream",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
    ],
    python_requires='>=3.7',
    install_requires=install_requires
)