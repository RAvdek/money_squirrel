from distutils.core import setup

with open('requirements.txt') as f:
    requirements = [line.strip() for line in f if line.strip() != '']

setup(
    name='money_squirrel',
    version='1.0',
    description='Correlate scraped data to asset prices',
    author='The money squirrel obv.',
    author_email='funkpacolypse@yahoo.com',
    packages=['money_squirrel'],
    requires=requirements
)
