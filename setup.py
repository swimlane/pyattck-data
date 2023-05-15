from setuptools import setup, find_packages

def parse_requirements(requirement_file):
    with open(requirement_file) as f:
        return f.readlines()

setup(
    name='pyattck-data',
    version='2.6.3',
    packages=find_packages(exclude=['tests*']),
    license='MIT',
    description='Generates contextual data utilized by pyattck.',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    install_requires=parse_requirements('./requirements.txt'),
    keywords=['att&ck', 'mitre', 'swimlane'],
    url='https://github.com/swimlane/pyattck-data',
    author='Swimlane',
    author_email='info@swimlane.com',
    python_requires='>=3.6, <4',
)
