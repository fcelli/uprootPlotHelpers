from setuptools import setup
  
setup(
    name = 'urph',
    version = '0.1',
    description = 'urph is a package built around uproot that makes plotting tasks easy.',
    url = '',
    author = 'fcelli',
    author_email = 'fedecel93@gmail.com',
    packages = [ 'urph',
                 'urph.plot_tools',
                 'urph.file_tools'
                ],
    install_requires=['uproot==3.13.1', 'numpy==1.19.5', 'matplotlib==3.3.3', 'pandas==1.2.0'],
    license='MIT',
)