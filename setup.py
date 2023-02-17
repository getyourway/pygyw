from setuptools import setup

setup(
    name='pygyw',
    version='1.1.1',
    description='A Python package to communicate with Get Your Way devices',
    url='https://github.com/getyourway/pygyw',
    author='Antoine Malherbe',
    author_email='a.malherbe@getyourway.be',
    license='BSD 3-clause',
    packages=['pygyw'],
    install_requires=[
        'bleak',
    ],
    classifiers=[
        'Development Status :: 2 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: System :: Hardware :: Hardware Drivers',
    ],
)
