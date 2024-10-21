import random

import attrs
from constants import CHORD_NUMBERS, KEYS, PROGRESSIONS, VELOCITY
from mingus.containers import Bar, Note
from mingus.core import chords, progressions
from mingus.midi import fluidsynth


@attrs.define()
class Progression:
    """Progression object."""

    name: str
    progression: list[str]
    keysig: str
    chords: list[str] = attrs.field(init=False)
    instrument: int = attrs.field(default=1)  # Piano.
    bpm: int = attrs.field(default=40)

    def __attrs_post_init__(self) -> None:
        _chords = progressions.to_chords(key=self.keysig, progression=self.progression)
        self.chords = [
            [Note(note_name, velocity=VELOCITY) for note_name in chord]
            for chord in _chords
        ]

    def play_progression(self) -> None:
        """Play progression with MIDI."""
        # TODO: Do I always need to init this here?
        # fluidsynth.init("/usr/share/sounds/sf2/TimGM6mb.sf2")

        bar = Bar(key=self.keysig, meter=(4, 4))
        for chord in self.chords:
            bar + chord

        fluidsynth.play_Bar(bar, self.instrument, self.bpm)
        fluidsynth.stop_everything()

    def info(self) -> tuple[str, ...]:
        """Prints info about the progression."""
        chords_named: list[list[str]] = [
            "(" + ",".join([note.name for note in chord]) + ")" for chord in self.chords
        ]
        return (self.name, "-".join(self.progression), "", "\n".join(chords_named))

    @classmethod
    def get_random(cls) -> "Progression":
        """Generate random Progression object."""
        name, progression = random.choice(PROGRESSIONS)
        keysig = random.choice(KEYS)
        return cls(name=name, progression=progression, keysig=keysig)

    @classmethod
    def get_random_single_chord_interval(cls) -> "Progression":
        """Generate a length-two progression.

        Generate random Progression object starting and ending
        with I and having one additional number chord.
        """
        # Always start with the "I" chord, always end with "I" chord.
        progression = ["I", random.choice(CHORD_NUMBERS), "I"]
        keysig = random.choice(KEYS)
        return cls(name=" ".join(progression), progression=progression, keysig=keysig)
