import tkinter as tk

import attrs
from mingus.midi import fluidsynth
from progressions import Progression

BUTTON_WIDTH = 15
TEXT_WIDTH = 2 * BUTTON_WIDTH + 10
TEXT_HEIGHT = 10


@attrs.define()
class Application:
    """Tk app for interval learning."""

    root = tk.Tk()
    info_text: "tk.Text" = attrs.field(init=False)
    progression: "Progression" = attrs.field(init=False)

    def __attrs_post_init__(self) -> None:

        generate_interval_btn = tk.Button(
            self.root,
            text="Generate\nInterval",
            command=self.generate_interval,
            width=BUTTON_WIDTH,
        )
        generate_progression_btn = tk.Button(
            self.root,
            text="Generate\nProgression",
            command=self.generate_progression,
            width=BUTTON_WIDTH,
        )
        play_btn = tk.Button(
            self.root, text="Play", command=self.play, width=BUTTON_WIDTH
        )
        solution_btn = tk.Button(
            self.root,
            text="Solution",
            command=self.progression_info,
            width=BUTTON_WIDTH,
        )
        self.info_text = tk.Text(self.root, width=TEXT_WIDTH, height=TEXT_HEIGHT)

        generate_interval_btn.grid(row=0, column=0, sticky=tk.W)
        generate_progression_btn.grid(row=0, column=1, sticky=tk.W)
        play_btn.grid(row=1, column=0, sticky=tk.W)
        solution_btn.grid(row=1, column=1, sticky=tk.W)
        self.info_text.grid(row=2, column=0, sticky=tk.W, columnspan=2)

    def run(self) -> None:
        """Run the app."""
        self.root.mainloop()

    def generate_progression(self) -> None:
        """Generate a random progression."""
        self.progression = Progression.get_random()

    def generate_interval(self) -> None:
        """Generate a random three-value progression starting and ending with I."""
        self.progression = Progression.get_random_single_chord_interval()

    def play(self) -> None:
        """Play progression via MIDI."""
        if self.progression:
            fluidsynth.init("/usr/share/sounds/sf2/TimGM6mb.sf2")
            self.progression.play_progression()

    def progression_info(self) -> None:
        """Print out progression info."""
        if self.progression:
            info = "\n".join(self.progression.info())
            self.info_text.delete(1.0, tk.END)
            self.info_text.insert(tk.END, info)


if __name__ == "__main__":
    app = Application()
    app.run()
