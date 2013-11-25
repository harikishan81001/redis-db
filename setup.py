from distutils.core import setup

setup(
    name='Redis-DB',
    version='0.1.5',
    author='Hari Kishan',
    author_email='hari.kishan81001@gmail.com',
    packages=['redis_db'],
    url='http://pypi.python.org/pypi/redis-db/',
    license='LICENSE.txt',
    description='Redis cache for managing Django ORM',
    long_description='',
    install_requires=[
        "Django >= 1.4",
        "redis >= 2.7.4",
    ],
)
