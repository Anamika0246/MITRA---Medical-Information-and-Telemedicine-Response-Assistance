# from setuptools import find_packages, setup

# setup(
#     name = 'MITRA',
#     version= '0.0.0',
#     author= 'Anamika Tiwari',
#     author_email= 'anamikatiwari0246@gmail.com',
#     packages= find_packages(),
#     install_requires = []
# )

from setuptools import find_packages, setup

# Read dependencies from requirements.txt
def get_requirements():
    with open("requirements.txt", "r") as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("-e")]

setup(
    name='MITRA',
    version='0.1.0',
    author='Anamika Tiwari',
    author_email='anamikatiwari0246@gmail.com',
    description='MITRA - Medical Information and Telemedicine Response Assistance',
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=get_requirements(),
    license='MIT',  
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
