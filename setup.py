from setuptools import setup, find_packages

setup(
    name="pythonPackages",
    version='0.6.3.3',
    author='Thijmen Francken',
    author_email='thijmen@your.io',
    description='All packages used for YOUR development',
    long_description=open('README.txt').read(),
    long_description_content_type="text/markdown",
    url='https://github.com/your-network/pythonPackages',
    project_urls={},
    license='LICENSE',
    packages=find_packages(),
    install_requires=['selenium',
                      'urllib3',
                      'pandas',
                      'selenium_stealth',
                      'Pillow',
                      'SQLAlchemy',
                      'boto3',
                      'botocore',
                      'numpy',
                      'python-dateutil',
                      'requests',
                      'markdownify',
                      'google-cloud',
                      'google-api-core',
                      'google-auth',
                      'google-cloud-logging',
                      'google-cloud-core',
                      'google-cloud-pubsub',
                      'html-sanitizer',
                      'rootpath',
                      'beautifulsoup4',
                      'Flask'],
    zip_safe=False,
)