from setuptools import setup
  
setup(
    name = 'urph',
    version = '0.1',
    description = '',
    url = '',
    author = 'fcelli',
    author_email = 'fedecel93@gmail.com',
    packages = [ 'urph',
                 'urph.plot_tools',
                 'urph.file_tools'
                ],
    install_requires=['uproot', 'numpy', 'matplotlib', 'pandas'],
    license='',
)