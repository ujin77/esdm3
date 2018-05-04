from setuptools import setup

setup(
    name='esdmd',
    version='1.0',
    url='https://github.com/ujin77/esdmd',
    license='',
    author='Eugene M.',
    author_email='ujin@i.ua',
    description='Eastron electricity meter daemon',
    install_requires = ['python-daemon>=2.1.2', 'lockfile>=0.12.2', 'minimalmodbus>=0.7', 'paho-mqtt>=1.3.0',
                    'py-zabbix>=1.1.3']
)
