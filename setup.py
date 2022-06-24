import setuptools

install_requires = []
install_requires.append('imutils')
install_requires.append('opencv-python')
install_requires.append('python-multipart')

setuptools.setup(
    name="fastapi_frame_stream",
    version="0.1.0",
    author="Tiago Prata",
    author_email="prataaa@hotmail.com",
    description="Package to easily stream individual frames using FastAPI",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: MIT",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
    ],
    python_requires='>=3.7',
    install_requires=install_requires
)