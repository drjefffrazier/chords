Run via `python app.py`

Requires python 3.6 or later.

You also need this for playback: https://github.com/wybiral/python-musical

* Modules:
    * `notes`:          lowest level, contains logic about notes and scales
    * `chords`:         depends on `notes`, has logic about chords
    * `ui`:             GUI layout
    * `progressions`:   database of known chord progressions
    * `playback`:       playback of sounds
    * `timeline`:       copied from `musical` package
    * `app`:            main application
