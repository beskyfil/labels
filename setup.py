from setuptools import setup


with open('README') as f:
    long_description = ''.join(f.readlines())


setup(
    name='labelsync',
    version='0.1',
    description='synchronize labels of your repos',
    long_description=long_description,
    author='Filip Beskyd',
    author_email='beskyfil@fit.cvut.cz',
    keywords='github, gitlab, label synchronization, webapp',
    license='MIT',
    url='https://github.com/beskyfil/labels',
    py_modules=['labelsync'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: MIT',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries',
        ],
    zip_safe=False,
)