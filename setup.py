from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    # noinspection SpellCheckingInspection
    setup(
        name="mysqlmapper",
        version="2.2.4",
        description=(
            "MySQL query tool class used by python."
        ),
        keywords="mysql orm",
        long_description=open('README.md', 'r').read(),
        long_description_content_type="text/markdown",
        author='lyoshur',
        author_email='1421333878@qq.com',
        maintainer='lyoshur',
        maintainer_email='1421333878@qq.com',
        license='MIT License',
        packages=find_packages(),
        platforms=["ubuntu", 'windows'],
        url='https://github.com/lyoshur/mysqlmapper',
        classifiers=[
            'Development Status :: 4 - Beta',
            'Operating System :: OS Independent',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python',
            'Programming Language :: Python :: Implementation',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Topic :: Software Development :: Libraries'
        ],
        install_requires=[
            'tabledbmapper==0.2.1',
            'PyMySQL',
        ],
        zip_safe=False
    )
    long_description = fh.read()
