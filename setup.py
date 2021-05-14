import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

version = {}
with open("campaigninfo/version.py") as fp:
    exec(fp.read(), version)

setuptools.setup(
    name="campaigninfo",
    version=version['__version__'],
    author="Wayne Crawford",
    author_email="crawford@ipgp.fr",
    description="Marine campaign information files",
    long_description=long_description,
    long_description_content_type="text/x-rst; charset=UTF-8",
    # url="https://github.com/WayneCrawford/seaplan",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=[
          'pyyaml>=3.0',
          'jsonschema>=2.6',
           'jsonref>=0.2'
    ],
    entry_points={
         'console_scripts': [
             'experiment_to_campaigns=campaigninfo.experiment_to_campaigns:main',
             'validate_campaign=campaigninfo.info_files:_validate_script'
         ]
    },
    python_requires='>=3.7',
    classifiers=(
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Physics"
    ),
    keywords='software'
)
