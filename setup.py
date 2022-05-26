from setuptools import setup, find_packages

setup(
    name="pythonPackages",
    version='0.2.8',
    author='Thijmen Francken',
    author_email='thijmen@your.io',
    description='All packages used for YOUR development',
    long_description=open('README.txt').read(),
    long_description_content_type="text/markdown",
    url='https://github.com/your-network/pythonPackages',
    project_urls = {
    },
    license='LICENSE',
    packages=find_packages(),
    install_requires=['selenium',
                      'pandas',
                      'selenium_stealth',
                      'Pillow',
                      'SQLAlchemy',
                      'boto3',
                      'botocore',
                      'numpy',
                      'python-dateutil',
                      'mariadb',
                      'requests'],
    zip_safe=False,
)