#!/usr/bin/env python
# coding: utf-8

from setuptools import setup, find_packages

setup(
    name='zheinit',
    version='0.0.73',
    author='deng1fan',
    author_email='dengyifan@iie.ac.cn',
    url='https://github.com/deng1fan',
    description=u'Init zhei environment.',
    long_description=open("README.md", "r", encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        'bs4',
        'requests',
        'rich',
    ],
    exclude=["*.tests", "*.tests.*", "tests"],
    include_package_data=True,
    python_requires='>=3.6',
    entry_points = {
        'console_scripts' : [
            # 这一行是安装到命令行运行的关键
            'init = zheinit.env:init'
        ]
    }
)
