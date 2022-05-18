from setuptools import setup, find_packages

setup(
    name="pythonPackages",
    version='0.1.4',
    author='Thijmen Francken',
    author_email='thijmenfrancken@gmail.com',
    description='All packages used for YOUR development',
    long_description=open('README.txt').read(),
    long_description_content_type="text/markdown",
    url='https://github.com/your-network/pythonPackages',
    project_urls = {
    },
    license='LICENSE',
    packages= find_packages(),
    install_requires=['selenium','pandas','selenium_stealth','Pillow'],
    zip_safe=False,
)