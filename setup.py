from setuptools import setup, find_packages

setup(
        name='tvdosage',
        version='0.1.1',
        description='Keep your Tv Series dose going',
        long_description=(open('README.md').read()),
        url='http://github.com/jairot/dosage/',
        license='MIT',
        author='Jairo Trad',
        author_email='jtrad@insus.com.ar',
        packages = find_packages(exclude=['*_test.py']),
        py_modules = ['tvdosage'],
          entry_points={
                    'console_scripts':
                        ['dosagedaemon = scripts.dosagedaemon:main',
                         'tvdosage = scripts.tvdosage:main'
                         ]},
        install_requires=['ThePirateBay', 'argparse', 'beautifulsoup4', 'dateutils', 'lxml',
                          'mattdaemon','mccabe', 'peewee', 'purl', 'python-dateutil',
                          'pytz', 'six', 'timeout-decorator','transmissionrpc','wsgiref'],
        include_package_data=True,
        classifiers=[
                'Development Status :: 2 - Pre-Alpha',
                'Intended Audience :: End Users/Desktop',
                'Natural Language :: English',
                'License :: OSI Approved :: MIT License',
                'Operating System :: OS Independent',
                'Programming Language :: Python',
                'Programming Language :: Python :: 2.7',
            ],
    )

