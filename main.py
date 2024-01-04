import flet
from flet import *
import pygame
import random
import time

pygame.mixer.init()

class GenerateGrid(UserControl):
    def __init__(self, difficulty):
        self.grid = Column(opacity=0, animate_opacity=300)
        self.correct: int = 0
        self.incorrect: int = 0
        self.blue_tiles: int = 0
        self.difficulty: int = difficulty
        self.music_playing = False
        self.music_loaded = False
        super().__init__()

    def load_music(self, file_path):
        pygame.mixer.music.load(file_path)
        self.music_loaded = True

    def show_color(self, e):
        if e.control.data == '#69FFF5':
            e.control.bgcolor = '69FFF5'
            e.control.opacity = 1
            e.control.update()
            self.correct += 1
            e.page.update()
        else:
            e.control.bgcolor = '#000000'
            e.control.opacity = 1
            e.control.update()
            self.incorrect += 1
            e.page.update()

    def hide_colors(self):
        for row in self.grid.controls[:]:
            for container in row.controls:
                container.bgcolor = '#34807A'
                container.update()

    def build(self):
        rows: list = [
            Row(
                alignment=MainAxisAlignment.CENTER,
                controls=[
                    Container(
                        width=54,
                        height=54,
                        animate=300,
                        border=None,   #border.all(1, 'blue'),
                        on_click=lambda e: self.show_color(e),
                    )
                    for _ in range(5)
                ]
            )
            for _ in range(5)
        ]

        colors: list = ['#34807A', '#69FFF5']

        for row in rows:
            for container in row.controls[:]:
                container.bgcolor = random.choices(colors, weights=[10, self.difficulty])[0]
                container.data = container.bgcolor
                if container.bgcolor == '#69FFF5':
                    self.blue_tiles += 1

        self.grid.controls = rows
        return self.grid

    def play_music(self):
        if not self.music_loaded:
            print("Erro: Carregue a música antes de reproduzi-la.")
            return

        pygame.mixer.music.play(-1)
        self.music_playing = True

    def stop_music(self):
        pygame.mixer.music.stop()
        self.music_playing = False

    def set_volume(self, volume):
        pygame.mixer.music.set_volume(volume)

    def toggle_music(self):
        if self.music_playing:
            self.stop_music()
        else:
            self.play_music()

def main(page: Page):
    page.horizontal_alignment = 'center'
    page.vertical_alignment = 'center'
    page.bgcolor = ('#1A403D')
    stage = Text(size=13, weight='bold')
    result = Text(size=16, weight='bold')

    start_button = Container(
        content=ElevatedButton(
            on_click=lambda e: start_game(e, GenerateGrid(2)),
            content=Text('Start!', size=13, weight='bold'),
            style=ButtonStyle(
                shape={'': RoundedRectangleBorder(radius=8)},
                color={'': 'red'}
            ),
            height=45,
            width=255,
        )
    )

    def start_game(e, level):
        result.value = ''

        grid = level
        grid.load_music('relaxmusic.mp3')  # Substitua 'caminho_para_sua_musica.mp3' pelo caminho correto
        page.controls.insert(3, grid)
        page.update()
        grid.grid.opacity = 1
        grid.grid.update()

        stage.value = f'Stage: {grid.difficulty - 1}'
        stage.update()

        start_button.disabled = True
        start_button.update()

        time.sleep(1.5)

        grid.hide_colors()

        # Inicia a música
        grid.play_music()


        while True:
            if grid.correct == grid.blue_tiles:
                grid.grid.disabled: bool = True
                grid.grid.update()

                result.value: str = 'Òtimo acerto!!! você parece estar evoluindo'
                result.color = 'green700'
                result.update()

                time.sleep(2)
                result.value = ''
                page.controls.remove(grid)
                page.update()

                difficulty = grid.difficulty + 1

                start_game(e, GenerateGrid(difficulty))
                break

            if grid.incorrect == 3:
                result.value = 'Você perdeu! tente novamente'
                result.color = 'red700'
                result.update()
                time.sleep(2)
                page.controls.remove(grid)
                page.update()
                start_button.disabled = False
                start_button.update()
                break

    page.add(
        Row(alignment=MainAxisAlignment.CENTER,
            controls=[
                Text(
                    'M E M O R Y  G A M E - W I L L',
                    size=26,
                    weight='bold',
                    color='#FFFFFF',  # Cor branca para combinar com a estética retro
                )
            ],
        ),
        Row(alignment=MainAxisAlignment.CENTER, controls=[result]),
        Divider(height=10, color='transparent'),
        Divider(height=10, color='transparent'),

        Row(alignment=MainAxisAlignment.CENTER, controls=[stage]),
        Divider(height=10, color='transparent'),

        Row(alignment=MainAxisAlignment.CENTER, controls=[start_button]),
    )
    page.update(),

if __name__ == '__main__':
    flet.app(target=main)
