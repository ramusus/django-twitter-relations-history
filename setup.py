from setuptools import setup, find_packages

setup(
    name='django-twitter-relations-history',
    version=__import__('twitter_relations_history').__version__,
    description='Django implementation for storing twitter user relations history',
    long_description=open('README.md').read(),
    author='ramusus',
    author_email='ramusus@gmail.com',
    url='https://github.com/ramusus/django-twitter-relations-history',
    download_url='http://pypi.python.org/pypi/django-twitter-relations-history',
    license='BSD',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False, # because we're including media that Django needs
    install_requires=[
        'django-twitter-api>=0.1.1',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
