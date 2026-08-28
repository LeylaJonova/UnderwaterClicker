from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.animation import Animation
from kivy.metrics import dp
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy import platform
from kivy.properties import NumericProperty, BooleanProperty
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, PushMatrix, PopMatrix, Rotate
import json
import os
import random

Builder.load_string(r"""
#:import dp kivy.metrics.dp

<Menu>:
    FloatLayout:
        Image:
            source: "assets/images/back_menu_title.png"
            size: root.size
            pos: root.pos
            allow_stretch: True
            keep_ratio: False

        Image:
            source: "assets/images/title.png"
            size_hint: None, None
            size: dp(220), dp(80)
            pos_hint: {"center_x": .5, "center_y": .63}
            allow_stretch: True
            keep_ratio: True

        Button:
            text: "PLAY"
            font_size: dp(22)
            size_hint: None, None
            size: dp(280), dp(60)
            pos_hint: {"center_x": .5, "center_y": .50}
            background_normal: ""
            background_color: .93, .52, .18, 1
            on_release: root.go_level_select()

        Button:
            text: "SETTINGS"
            font_size: dp(20)
            size_hint: None, None
            size: dp(280), dp(55)
            pos_hint: {"center_x": .5, "center_y": .37}
            background_normal: ""
            background_color: .93, .52, .18, 1
            on_release: root.go_settings()

        Button:
            text: "EXIT"
            font_size: dp(20)
            size_hint: None, None
            size: dp(280), dp(55)
            pos_hint: {"center_x": .5, "center_y": .24}
            background_normal: ""
            background_color: .78, .43, .14, 1
            on_release: root.exit_app()


<LevelSelect>:
    FloatLayout:
        Image:
            source: "assets/images/back_menu_title.png"
            size: root.size
            pos: root.pos
            allow_stretch: True
            keep_ratio: False

        # Напис SELECT LEVEL опустили нижче, щоб він не накладався на заголовок
        Label:
            text: "SELECT LEVEL"
            font_size: dp(28)
            bold: True
            color: 1, 1, 1, 1
            size_hint: 1, None
            height: dp(40)
            pos_hint: {"center_x": .5, "center_y": .68}

        # Список рівнів трохи нижче заголовка
        ScrollView:
            size_hint: None, None
            size: dp(280), dp(220)
            pos_hint: {"center_x": .5, "center_y": .46}
            
            GridLayout:
                id: levels_grid
                cols: 1
                size_hint_y: None
                height: self.minimum_height
                spacing: dp(10)
                padding: dp(5)

        Button:
            text: "BACK"
            font_size: dp(20)
            size_hint: None, None
            size: dp(280), dp(55)
            pos_hint: {"center_x": .5, "center_y": .24}
            background_normal: ""
            background_color: .93, .52, .18, 1
            on_release: root.go_menu()


<Settings>:
    FloatLayout:
        Image:
            source: "assets/images/back_menu_title.png"
            size: root.size
            pos: root.pos
            allow_stretch: True
            keep_ratio: False

        Label:
            text: "SETTINGS"
            font_size: dp(38)
            bold: True
            color: 1, 1, 1, 1
            size_hint: 1, None
            height: dp(55)
            pos_hint: {"center_x": .5, "top": .73}

        Label:
            text: "Sound volume: " + str(int(app.volume * 100)) + "%"
            font_size: dp(21)
            color: 1, 1, 1, 1
            size_hint: None, None
            size: dp(250), dp(45)
            pos_hint: {"center_x": .5, "center_y": .62}

        Slider:
            min: 0
            max: 1
            value: app.volume
            size_hint: None, None
            size: dp(280), dp(45)
            pos_hint: {"center_x": .5, "center_y": .52}
            on_value: app.set_volume(self.value)

        Button:
            text: "RESET PROGRESS"
            font_size: dp(18)
            size_hint: None, None
            size: dp(280), dp(50)
            pos_hint: {"center_x": .5, "center_y": .38}
            background_normal: ""
            background_color: .85, .25, .25, 1
            on_release: root.reset_progress_data()

        Button:
            text: "BACK"
            font_size: dp(20)
            size_hint: None, None
            size: dp(280), dp(55)
            pos_hint: {"center_x": .5, "center_y": .24}
            background_normal: ""
            background_color: .93, .52, .18, 1
            on_release: root.go_back()


<Game>:
    FloatLayout:
        Image:
            id: level_bg
            source: "assets/images/level1.png"
            size: root.size
            pos: root.pos
            allow_stretch: True
            keep_ratio: False

        Label:
            id: level_title
            text: "Level 1"
            font_size: dp(45)
            bold: True
            color: 1, 1, 1, 1
            size_hint: 1, None
            height: dp(60)
            pos_hint: {"center_x": .5, "top": .85}
            opacity: 0

        Label:
            text: str(root.score)
            font_size: dp(48)
            bold: True
            color: 1, 1, 1, 1
            size_hint: None, None
            size: dp(100), dp(60)
            pos_hint: {"x": .05, "top": .95}

        Label:
            text: str(root.elapsed_time) + "s"
            font_size: dp(44)
            bold: True
            color: 1, 1, 1, 1
            size_hint: None, None
            size: dp(120), dp(60)
            pos_hint: {"right": .95, "top": .95}

        Label:
            id: stars_hint_label
            text: ""
            font_name: "DejaVuSans.ttf"
            font_size: dp(16)
            bold: True
            color: 1, 0.9, 0.4, 0.9
            size_hint: 1, None
            height: dp(30)
            pos_hint: {"center_x": .5, "top": .93}

        FloatLayout:
            id: game_window
            size_hint: 1, .76
            pos_hint: {"x": 0, "y": .12}

            Fish:
                id: fish
                size_hint: None, None
                size: dp(200), dp(200)

        Label:
            id: level_complete
            text: ""
            font_size: dp(40)
            bold: True
            color: 0.07, 0.95, 0.68, 1
            halign: "center"
            valign: "middle"
            text_size: self.size
            size_hint: 1, None
            height: dp(120)
            pos_hint: {"center_x": .5, "center_y": .62}
            opacity: 0

        BoxLayout:
            id: stars_container
            orientation: "horizontal"
            size_hint: None, None
            size: dp(180), dp(50)
            pos_hint: {"center_x": .5, "center_y": .48}
            spacing: dp(10)
            opacity: 0

        Button:
            id: retry_button
            text: "AGAIN"
            font_size: dp(18)
            size_hint: None, None
            size: dp(130), dp(50)
            pos_hint: {"center_x": .35, "center_y": .34}
            opacity: 0
            disabled: True
            background_normal: ""
            background_color: .93, .52, .18, 1
            on_release: root.retry_level()

        Button:
            id: next_button
            text: "NEXT LEVEL"
            font_size: dp(18)
            size_hint: None, None
            size: dp(150), dp(50)
            pos_hint: {"center_x": .67, "center_y": .34}
            opacity: 0
            disabled: True
            background_normal: ""
            background_color: 0.07, 0.95, 0.68, 1
            on_release: root.next_level()

        Button:
            text: "LEVELS"
            font_size: dp(15)
            size_hint: None, None
            size: dp(100), dp(45)
            pos_hint: {"x": .05, "y": .03}
            background_normal: ""
            background_color: .93, .52, .18, 1
            on_release: root.go_level_select()

        Button:
            text: "SETTINGS"
            font_size: dp(15)
            size_hint: None, None
            size: dp(110), dp(45)
            pos_hint: {"right": .95, "y": .03}
            background_normal: ""
            background_color: .93, .52, .18, 1
            on_release: root.go_settings()


<VictoryScreen>:
    FloatLayout:
        Image:
            source: "assets/images/back_menu_title.png"
            size: root.size
            pos: root.pos
            allow_stretch: True
            keep_ratio: False

        Image:
            id: giant_star
            source: "assets/images/star.png"
            size_hint: None, None
            size: dp(100), dp(100)
            pos_hint: {"center_x": .5, "center_y": .60}
            opacity: 0

        Label:
            text: "GAME COMPLETE!"
            font_size: dp(28)
            bold: True
            color: 0.07, 0.95, 0.68, 1
            size_hint: 1, None
            height: dp(40)
            pos_hint: {"center_x": .5, "top": .73}

        BoxLayout:
            id: results_list
            orientation: "vertical"
            size_hint: None, None
            size: dp(320), dp(220)
            pos_hint: {"center_x": .5, "center_y": .48}
            spacing: dp(10)

        Button:
            text: "MAIN MENU"
            font_size: dp(20)
            size_hint: None, None
            size: dp(280), dp(55)
            pos_hint: {"center_x": .5, "center_y": .24}
            background_normal: ""
            background_color: .93, .52, .18, 1
            on_release: root.go_menu()


<Bubble>:
    canvas:
        Color:
            rgba: 0.65, 0.9, 1, root.opacity
        Ellipse:
            pos: root.pos
            size: root.size


<RotatedImage>:
    canvas.before:
        PushMatrix
        Rotate:
            angle: root.angle
            origin: self.center
    canvas.after:
        PopMatrix
""")


class Menu(Screen):
    def go_level_select(self, *args):
        self.manager.transition.direction = "left"
        self.manager.current = "level_select"

    def go_settings(self, *args):
        self.manager.get_screen("settings").return_screen = "menu"
        self.manager.transition.direction = "up"
        self.manager.current = "settings"

    def exit_app(self, *args):
        App.get_running_app().stop()


class LevelSelect(Screen):
    def on_enter(self, *args):
        app = App.get_running_app()
        grid = self.ids.levels_grid
        grid.clear_widgets()

        max_unlocked = app.progress.get("current_level", 0)
        saved_stars = app.progress.get("stars", [])

        for i in range(len(app.LEVELS)):
            is_unlocked = i <= max_unlocked

            row = BoxLayout(orientation="horizontal", size_hint=(1, None), height=dp(50), spacing=dp(10))

            btn = Button(
                text=f"Level {i + 1}" if is_unlocked else f"Level {i + 1} (Locked)",
                font_size=dp(18),
                bold=True,
                size_hint_x=0.6,
                background_normal="",
                background_color=(0.93, 0.52, 0.18, 1) if is_unlocked else (0.4, 0.4, 0.4, 1),
                disabled=not is_unlocked
            )
            btn.level_index = i
            btn.bind(on_release=self.start_selected_level)
            row.add_widget(btn)

            stars_box = BoxLayout(orientation="horizontal", size_hint_x=0.4, spacing=dp(4))
            if is_unlocked:
                got = saved_stars[i] if i < len(saved_stars) else 0
                for _ in range(got):
                    stars_box.add_widget(Image(source="assets/images/star.png", allow_stretch=True, keep_ratio=True))

            row.add_widget(stars_box)
            grid.add_widget(row)

    def start_selected_level(self, instance):
        app = App.get_running_app()
        app.LEVEL = instance.level_index
        self.manager.transition.direction = "left"
        self.manager.current = "game"

    def go_menu(self):
        self.manager.transition.direction = "right"
        self.manager.current = "menu"


class Settings(Screen):
    return_screen = "menu"

    def go_back(self, *args):
        direction = "down" if self.return_screen == "menu" else "right"
        self.manager.transition.direction = direction
        self.manager.current = self.return_screen

    def reset_progress_data(self):
        app = App.get_running_app()
        app.progress = {"current_level": 0, "volume": app.volume, "stars": []}
        app.save_progress()


class VictoryScreen(Screen):
    def on_enter(self, *args):
        app = App.get_running_app()
        container = self.ids.results_list
        container.clear_widgets()

        all_three_stars = True
        saved_stars = app.progress.get("stars", [])

        for i, lvl in enumerate(app.LEVELS):
            row = BoxLayout(orientation="horizontal", size_hint=(1, None), height=dp(40), spacing=dp(10))

            lbl = Label(
                text=f"Level {i + 1}:",
                font_size=dp(18),
                bold=True,
                color=(1, 1, 1, 1),
                size_hint_x=0.5
            )
            row.add_widget(lbl)

            stars_box = BoxLayout(orientation="horizontal", size_hint_x=0.5, spacing=dp(5))
            got_stars = saved_stars[i] if i < len(saved_stars) else 0
            if got_stars < 3:
                all_three_stars = False

            for _ in range(got_stars):
                stars_box.add_widget(Image(source="assets/images/star.png", allow_stretch=True, keep_ratio=True))

            row.add_widget(stars_box)
            container.add_widget(row)

        giant_star = self.ids.giant_star
        giant_star.opacity = 0
        giant_star.size = (dp(20), dp(20))

        if all_three_stars:
            anim = (
                           Animation(opacity=1, duration=0.3)
                           & Animation(size=(dp(120), dp(120)), duration=0.5, t="out_back")
                   ) + (
                       Animation(size=(dp(100), dp(100)), duration=0.2)
                   )
            anim.start(giant_star)

    def go_menu(self):
        self.manager.transition.direction = "right"
        self.manager.current = "menu"


class RotatedImage(Image):
    angle = NumericProperty(0)


class Bubble(Widget):
    opacity = NumericProperty(1)


class Fish(RotatedImage):
    anim_play = False
    interaction_block = True
    fish_current = None
    fish_index = 0
    hp_current = 0

    click_music = SoundLoader.load("assets/audios/bubble01.mp3")
    defeat_music = SoundLoader.load("assets/audios/fish_def.ogg")

    def on_kv_post(self, base_widget):
        self.GAME_SCREEN = self.parent.parent.parent
        return super().on_kv_post(base_widget)

    def new_fish(self, *args):
        app = App.get_running_app()
        if app.LEVEL >= len(app.LEVELS):
            return
        self.fish_current = app.LEVELS[app.LEVEL]["fishes"][self.fish_index]
        self.source = app.FISHES[self.fish_current]["source"]
        self.hp_current = app.FISHES[self.fish_current]["hp"]
        self.swim()

    def swim(self):
        game = self.GAME_SCREEN
        self.stop_all_animations()
        self.size = (dp(200), dp(200))
        self.angle = 0
        self.pos = (-self.width, game.height * .40)
        self.opacity = 1
        self.interaction_block = True

        swim = Animation(
            x=game.width / 2 - self.width / 2,
            duration=.8,
            t="out_quad"
        )
        swim.bind(on_complete=lambda *_: setattr(self, "interaction_block", False))
        swim.start(self)

    def stop_all_animations(self):
        Animation.cancel_all(self)

    def defeated(self):
        self.interaction_block = True
        old_size = self.size
        old_pos = self.pos
        new_size = (self.width * 1.8, self.height * 1.8)
        new_pos = (
            self.x - (new_size[0] - self.width) / 2,
            self.y - (new_size[1] - self.height) / 2
        )

        anim = (
                       Animation(angle=self.angle + 360, duration=.45, t="in_cubic")
                       & Animation(size=new_size, pos=new_pos, duration=.45, t="out_back")
               ) + Animation(opacity=0, duration=.25)

        def restore(*_):
            self.size = old_size
            self.pos = old_pos
            self.angle = 0

        anim.bind(on_complete=restore)
        anim.start(self)

        app = App.get_running_app()
        if app.sound_enabled and self.defeat_music:
            self.defeat_music.play()

    def spawn_bubbles(self, touch):
        for _ in range(5):
            diameter = random.randint(10, 30)
            local_x, local_y = self.to_local(*touch.pos)

            bubble = Bubble(
                size=(diameter, diameter),
                pos=(
                    local_x - diameter / 2 + random.randint(-10, 10),
                    local_y - diameter / 2 + random.randint(-10, 10)
                )
            )
            self.add_widget(bubble)

            animation = Animation(
                y=bubble.y + random.randint(30, 200),
                opacity=0,
                duration=random.uniform(0.3, 0.6)
            )
            animation.bind(
                on_complete=lambda *_, item=bubble: item.parent.remove_widget(item)
                if item.parent else None
            )
            animation.start(bubble)

    def on_touch_down(self, touch):
        if not self.collide_point(*touch.pos):
            return super().on_touch_down(touch)

        if self.anim_play or self.interaction_block or not self.GAME_SCREEN.game_active:
            return True

        app = App.get_running_app()
        self.hp_current -= 1
        self.GAME_SCREEN.score += 1

        if app.sound_enabled and self.click_music:
            self.click_music.play()

        self.spawn_bubbles(touch)

        if self.hp_current > 0:
            old_size = self.size
            old_pos = self.pos
            new_size = (self.width * 1.15, self.height * 1.15)
            new_pos = (
                self.x - (new_size[0] - self.width) / 2,
                self.y - (new_size[1] - self.height) / 2
            )
            zoom_anim = (
                    Animation(size=new_size, pos=new_pos, duration=.06)
                    + Animation(size=old_size, pos=old_pos, duration=.06)
            )
            self.anim_play = True
            zoom_anim.bind(on_complete=lambda *_: setattr(self, "anim_play", False))
            zoom_anim.start(self)
        else:
            self.defeated()
            level_fish = app.LEVELS[app.LEVEL]["fishes"]
            if self.fish_index + 1 < len(level_fish):
                self.fish_index += 1
                Clock.schedule_once(self.new_fish, .75)
            else:
                Clock.schedule_once(self.GAME_SCREEN.check_level_complete, .75)

        return True


class Game(Screen):
    score = NumericProperty(0)
    elapsed_time = NumericProperty(0)
    game_active = False
    timer_event = None

    back_sound = SoundLoader.load("assets/audios/Black_Swan_part.mp3")
    level_complete_sound = SoundLoader.load("assets/audios/level_complete.ogg")

    def on_pre_enter(self, *args):
        app = App.get_running_app()
        if app.LEVEL >= len(app.LEVELS):
            app.LEVEL = 0

        bg_path = f"assets/images/level{app.LEVEL + 1}.png"
        if os.path.exists(bg_path):
            self.ids.level_bg.source = bg_path
        else:
            self.ids.level_bg.source = "assets/images/back_game.png"

        lvl_data = app.LEVELS[app.LEVEL]
        self.ids.stars_hint_label.text = f"3★ ≤ {lvl_data['t3']}s  |  2★ ≤ {lvl_data['t2']}s"

        self.score = 0
        self.elapsed_time = 0
        self.game_active = False

        self.ids.level_complete.opacity = 0
        self.ids.stars_container.opacity = 0
        self.ids.stars_container.clear_widgets()

        self.ids.retry_button.opacity = 0
        self.ids.retry_button.disabled = True
        self.ids.next_button.opacity = 0
        self.ids.next_button.disabled = True

        self.ids.level_title.text = f"Level {app.LEVEL + 1}"

        fish = self.ids.fish
        fish.fish_index = 0
        fish.opacity = 0
        fish.interaction_block = True

        return super().on_pre_enter(*args)

    def on_enter(self, *args):
        title = (
                Animation(opacity=1, duration=.45)
                + Animation(opacity=0, duration=.55)
        )
        title.bind(on_complete=self.start_game)
        title.start(self.ids.level_title)

        app = App.get_running_app()
        if app.music_enabled and self.back_sound:
            self.back_sound.volume = app.volume
            self.back_sound.play()

        return super().on_enter(*args)

    def start_game(self, *args):
        if self.manager.current != "game":
            return
        self.game_active = True
        self.elapsed_time = 0

        if self.timer_event:
            self.timer_event.cancel()
        self.timer_event = Clock.schedule_interval(self.update_timer, 1.0)

        self.ids.fish.new_fish()

    def update_timer(self, dt):
        if self.game_active:
            self.elapsed_time += 1

    def check_level_complete(self, *args):
        if not self.game_active:
            return

        self.game_active = False
        if self.timer_event:
            self.timer_event.cancel()

        app = App.get_running_app()

        lvl_data = app.LEVELS[app.LEVEL]
        if self.elapsed_time <= lvl_data["t3"]:
            stars_count = 3
        elif self.elapsed_time <= lvl_data["t2"]:
            stars_count = 2
        else:
            stars_count = 1

        while len(app.progress["stars"]) <= app.LEVEL:
            app.progress["stars"].append(0)
        if stars_count > app.progress["stars"][app.LEVEL]:
            app.progress["stars"][app.LEVEL] = stars_count

        is_last = app.LEVEL == len(app.LEVELS) - 1

        if is_last:
            self.ids.level_complete.text = "LEVEL COMPLETE!"
            self.ids.next_button.text = "VICTORY"
        else:
            self.ids.level_complete.text = "LEVEL COMPLETE!"
            self.ids.next_button.text = "NEXT LEVEL"
            if app.LEVEL + 1 > app.progress["current_level"]:
                app.progress["current_level"] = app.LEVEL + 1

        container = self.ids.stars_container
        container.clear_widgets()
        for _ in range(stars_count):
            star_img = Image(source="assets/images/star.png", allow_stretch=True, keep_ratio=True)
            container.add_widget(star_img)

        self.ids.stars_container.opacity = 1
        app.save_progress()

        Animation(opacity=1, duration=.3).start(self.ids.level_complete)

        self.ids.retry_button.disabled = False
        Animation(opacity=1, duration=.3).start(self.ids.retry_button)

        self.ids.next_button.disabled = False
        Animation(opacity=1, duration=.3).start(self.ids.next_button)

        if self.back_sound:
            self.back_sound.volume = app.volume * .4

        if app.sound_enabled and self.level_complete_sound:
            self.level_complete_sound.play()

    def retry_level(self):
        self.prepare_current_level()
        Clock.schedule_once(self.start_game, .25)

    def next_level(self):
        app = App.get_running_app()
        if app.LEVEL == len(app.LEVELS) - 1:
            if self.back_sound:
                self.back_sound.stop()
            self.manager.transition.direction = "left"
            self.manager.current = "victory"
        else:
            app.LEVEL += 1
            app.save_progress()
            self.prepare_current_level()
            Clock.schedule_once(self.start_game, .25)

    def prepare_current_level(self):
        app = App.get_running_app()
        self.game_active = False
        self.elapsed_time = 0
        if self.timer_event:
            self.timer_event.cancel()

        bg_path = f"assets/images/level{app.LEVEL + 1}.png"
        if os.path.exists(bg_path):
            self.ids.level_bg.source = bg_path
        else:
            self.ids.level_bg.source = "assets/images/back_game.png"

        lvl_data = app.LEVELS[app.LEVEL]
        self.ids.stars_hint_label.text = f"3★ ≤ {lvl_data['t3']}s  |  2★ ≤ {lvl_data['t2']}s"

        self.score = 0

        fish = self.ids.fish
        fish.stop_all_animations()
        fish.fish_index = 0
        fish.opacity = 0
        fish.interaction_block = True
        fish.angle = 0
        fish.size = (dp(200), dp(200))

        self.ids.level_complete.opacity = 0
        self.ids.stars_container.opacity = 0
        self.ids.stars_container.clear_widgets()

        self.ids.retry_button.opacity = 0
        self.ids.retry_button.disabled = True
        self.ids.next_button.opacity = 0
        self.ids.next_button.disabled = True

        self.ids.level_title.text = f"Level {app.LEVEL + 1}"

        if self.back_sound:
            self.back_sound.volume = app.volume

    def go_level_select(self):
        self.game_active = False
        if self.timer_event:
            self.timer_event.cancel()
        if self.back_sound:
            self.back_sound.stop()

        self.manager.transition.direction = "right"
        self.manager.current = "level_select"

    def go_settings(self):
        self.game_active = False
        if self.timer_event:
            self.timer_event.cancel()
        if self.back_sound:
            self.back_sound.stop()

        settings = self.manager.get_screen("settings")
        settings.return_screen = "game"
        self.manager.transition.direction = "left"
        self.manager.current = "settings"


class ClickerApp(App):
    LEVEL = 0
    volume = NumericProperty(.7)
    music_enabled = BooleanProperty(True)
    sound_enabled = BooleanProperty(True)

    FISHES = {
        "fish1": {"source": "assets/images/fish_01.png", "hp": 10},
        "fish2": {"source": "assets/images/fish_02.png", "hp": 15}
    }

    LEVELS = [
        {"fishes": ["fish1", "fish1"], "t3": 6, "t2": 8},
        {"fishes": ["fish2", "fish1", "fish2"], "t3": 12, "t2": 15},
        {"fishes": ["fish2", "fish1", "fish2", "fish1"], "t3": 15, "t2": 20}
    ]

    def on_start(self):
        self.progress = self.load_progress()
        self.volume = self.progress["volume"]

    def load_progress(self):
        defaults = {"current_level": 0, "volume": .7, "stars": []}
        path = os.path.join(self.user_data_dir, "progress.json")
        try:
            with open(path, "r", encoding="utf-8") as file:
                saved = json.load(file)
                if isinstance(saved, dict):
                    defaults.update(saved)
        except Exception:
            pass
        return defaults

    def save_progress(self):
        os.makedirs(self.user_data_dir, exist_ok=True)
        path = os.path.join(self.user_data_dir, "progress.json")
        with open(path, "w", encoding="utf-8") as file:
            json.dump(self.progress, file, ensure_ascii=False, indent=4)

    def set_volume(self, value):
        self.volume = max(0, min(float(value), 1))
        if hasattr(self, "progress"):
            self.progress["volume"] = self.volume
            self.save_progress()

    def build(self):
        sm = ScreenManager()
        sm.add_widget(Menu(name="menu"))
        sm.add_widget(LevelSelect(name="level_select"))
        sm.add_widget(Game(name="game"))
        sm.add_widget(Settings(name="settings"))
        sm.add_widget(VictoryScreen(name="victory"))
        return sm


if platform != "android":
    Window.size = (400, 600)

app = ClickerApp()
app.run()