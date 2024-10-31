import random
import tkinter as tk
from tempfile import TemporaryDirectory

import attrs
from mingus.containers import Bar
from mingus.core import intervals
from mingus.extra import lilypond
from PIL import Image, ImageTk

BUTTON_WIDTH = 15
TEXT_WIDTH = 2 * BUTTON_WIDTH + 10
TEXT_HEIGHT = 1
NOTE_CROP = (80, 0, 220, 100)

NOTE_VALUES = [
    "Gb",
    "Db",
    "Ab",
    "Eb",
    "Bb",
    "F",
    "C",
    "G",
    "D",
    "A",
    "E",
    "B",
    "F#",
    "C#",
    "G#",
    "D#",
    "A#",
]


@attrs.define()
class Application:
    """Tk app for interval learning."""

    root = tk.Tk()
    info_text: "tk.Text" = attrs.field(init=False)
    img_panel_label: "tk.Label" = attrs.field(init=False)
    interval_notes: list[str] = attrs.field(init=False)
    bar: Bar = attrs.field(init=False)

    def __attrs_post_init__(self) -> None:

        generate_interval_btn = tk.Button(
            self.root,
            text="Generate\nInterval",
            command=self.generate_interval,
            width=BUTTON_WIDTH,
        )

        solution_btn = tk.Button(
            self.root,
            text="Solution",
            command=self.interval_info,
            width=BUTTON_WIDTH,
        )
        self.info_text = tk.Text(self.root, width=TEXT_WIDTH, height=TEXT_HEIGHT)

        zero_size_img = tk.PhotoImage()  # zero size image
        self.img_panel_label = tk.Label(
            self.root,
            image=zero_size_img,
            width=f"{(NOTE_CROP[2] - NOTE_CROP[0])}px",
            height=f"{(NOTE_CROP[3] - NOTE_CROP[1])}px",
        )

        generate_interval_btn.grid(row=0, column=0, sticky=tk.W)
        solution_btn.grid(row=0, column=1, sticky=tk.W)
        self.img_panel_label.grid(row=1, column=0, columnspan=2)
        self.info_text.grid(row=2, column=0, sticky=tk.W, columnspan=2)

    def run(self) -> None:
        """Run the app."""
        self.root.mainloop()

    def generate_interval(self) -> None:
        """Generate a random interval."""
        self.clear_info()  # Reset answer space.

        self.interval_notes = [random.choices(NOTE_VALUES, k=2)][0]
        self.bar = Bar()
        # I don't know why mingus does it like this.
        self.bar + self.interval_notes[0]
        self.bar + self.interval_notes[1]

        lp = lilypond.from_Bar(self.bar, showkey=False, showtime=False)
        with TemporaryDirectory() as tdir:
            out = tdir + "pond.png"
            lilypond.to_png(lp, out)
            img = Image.open(out).convert("RGBA")
            img2 = img.crop(NOTE_CROP)
            img2.save(out)

            image = ImageTk.PhotoImage(file=out)
            self.img_panel_label.config(image=image)
            self.img_panel_label.image = (
                image  # save a reference of the image to avoid garbage collection
            )

    def interval_info(self) -> None:
        """Print out interval info."""
        if self.interval_notes:
            info = (
                " ".join(self.interval_notes)
                + ": "
                + intervals.determine(self.interval_notes[0], self.interval_notes[1])
            )
            self.clear_info()
            self.info_text.insert(tk.END, info)

    def clear_info(self) -> None:
        """Clear info text."""
        self.info_text.delete(1.0, tk.END)


if __name__ == "__main__":
    app = Application()
    app.run()
