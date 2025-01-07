from setuptools import setup, find_packages


with open( "README.md", encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.2.1'
DESCRIPTION = 'Decorator for Fast Generation of Function Input Output Components with Tkinter or Streamlit'
LONG_DESCRIPTION = 'A function decorator that generates corresponding input and output components with Tkinter or Streamlit based on the number of arguments and return values of the function.'

setup(
    name="defgui",
    version=VERSION,
    author="davidho",
    author_email="",
    url="https://github.com/davidho123/defgui",
    license="MIT",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'gui', 'streamlit','defgui','function','tkinter'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
    ]
)
