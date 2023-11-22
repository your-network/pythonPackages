from setuptools import setup, find_packages

setup(
    name="pythonPackages",
    version='0.7.9.0',
    author='Thijmen',
    author_email='thijmen@your.io',
    description='All packages used for YOUR development',
    long_description=open('README.txt').read(),
    long_description_content_type="text/markdown",
    url='https://github.com/your-network/pythonPackages',
    project_urls={},
    license='LICENSE',
    packages=find_packages(),
    install_requires=['urllib3',
                      'Pillow',
                      'numpy',
                      'python-dateutil',
                      'requests',
                      'rootpath',
                      'beautifulsoup4'],
    zip_safe=False,
)