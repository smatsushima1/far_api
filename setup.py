import setuptools

with open('README.md', 'r', encoding = 'utf8') as rm:
  desc = rm.read()

with open('LICENSE.md', 'r', encoding = 'utf8') as lic:
  lic = lic.read()

setuptools.setups(
  name = 'far-api-smatsushima1',
  version = '0.0.1',
  author = 'smatsushima1',
  author_email = 'smatsushima1@gmail.com',
  description = 'Federal Acquisition Regulation text to be recalled as necessary.',
  long_description = desc,
  license = lic,
  url = 'https://github.com/smatsushima1/far_api',
  packages = setuptools.find_packages(),
  classifiers = [
                 'Programming Language :: Python :: 3',
                 'License :: OSI Approved :: MIT License',
                 'Operating System :: OS Independent'
                 ],
  python_requires = '>=3.8'
)


