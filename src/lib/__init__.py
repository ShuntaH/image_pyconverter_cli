import dataclasses
import glob

from src.utils.stdout import Stdout, Bcolors


@dataclasses.dataclass
class Library:
    dir_path: str

    @property
    def image_paths(self) -> list[str]:
        image_paths = sorted(glob.glob(f'{self.dir_path}/*'))
        # => ['/User/macbook/a.jpg', '/User/macbook/b.jpg', '/User/macbook/c.jpg']
        if not image_paths:
            Stdout.styled_stdout(Bcolors.FAIL.value, 'No images.')
            raise ValueError
        return image_paths
