from setuptools import setup, find_packages

setup(
    name='personal_helper',
    version='0.0.1',
    description='Personal helper bot that works in 3 modes: contacts book, notes and files sorting in a selected folder.',
    packages=find_packages(),
    package_data={'personal_helper': ['help.txt']},
    py_modules=['clean'],
    entry_points={'console_scripts': [
        'personal-helper = personal_helper.personal_helper:main']}
)
