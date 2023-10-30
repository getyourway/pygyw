from setuptools import setup

setup(
    name='pygyw',
    version='1.2.2',
    description='A Python package to interact with aRdent smart glasses',
    url='https://github.com/getyourway/pygyw',
    author='Antoine Malherbe',
    author_email='a.malherbe@getyourway.be',
    license='BSD 3-clause',
    packages=[
        'pygyw',
        'pygyw.bluetooth',
        'pygyw.layout'
    ],
    package_data={
        'pygyw.layout': ['icons/*'],
    },
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
