import setuptools

setuptools.setup(
    name="python_packages",
    version='0.0.1',
    author='Thijmen Francken',
    author_email='thijmen.airbridge@gmail.com',
    description='All packages used for YOUR development',
    long_description=open('README.txt').read(),
    long_description_content_type="text/markdown",
    url='https://github.com/your-network/python_packages',
    project_urls = {
    },
    license='MIT',
    packages=['seleniumYour', 'helpers'],
    install_requires=['selenium'],
)