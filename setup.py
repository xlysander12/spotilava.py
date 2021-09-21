from setuptools import setup

setup(
    name='spotilava.py',
    version='1.0.0',
    packages=['spotilavapy'],
    url='https://github.com/xlysander12/spotilava.py',
    license='MIT',
    author='xlysander12',
    author_email='xlysander12pt@gmail.com',
    description='Python wrapper to convert Spotify songs to be playeed through LavaLink',
    install_requires=[
        "lavalink",
        "spotipy"
    ]
)
