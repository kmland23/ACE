from setuptools import setup

setup(
   name='XML-Random',
   version='1.0',
   description='Creates random XML files given a directory of files',
   author='Kristina Landino',
   author_email='kristina.landino@heronsystems.com',
   packages=['XML-Random'],  
   install_requires=['glob2', 'beautifulsoup4', 'numpy'. 'lxml'], 
   scripts=[
            'XML-Random/fix_format.py',
            'XML-Random/xmlCreator_12_8.py',
           ]
)
