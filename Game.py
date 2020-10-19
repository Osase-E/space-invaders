# Space Shooter Game
# Created by Osase Emokpae
# December 2019, optimised

from tkinter import *
import random
import time


class ShooterGame:
        def __init__(self, master):
            self.master = master
            root.title('Ranger')
            self.background_image = PhotoImage(file='background.gif')
            self.main_background_image = PhotoImage(file='mainBG.png')
            self.player_sprite_image = PhotoImage(file='asset.png')
            self.boss_key_image = PhotoImage(file='boss_image.png')
            self.bullets_player = []  # Stores the bullets of the player
            self.bullets_enemies = []  # Stores the bullets of the enemies
            # Stores the enemies that are allowed to shoot
            self.allowed_to_shoot = []
            # Stores the index of previous enemies and current ones
            self.temp_enemies = []
            self.enemies = []  # Stores the enemies
            # Initialises the counter to update the jumper variable
            self.counter = 0
            self.direction = -1
            # Initialises counter for the max number of enemies on the screen
            self.max_enemies = 10
            self.enemies_speed = 10  # Initialises the speed of the enemies
            self.pause_boolean = False
            self.boss_key_boolean = False
            self.instruction_window = None
            self.quit_boolean = False
            self.time_start = 0
            self.time_check = 0
            self.leader_board_top = None
            self.quit_top = None
            self.enemy_player_collision = False
            background_label = Label(root, image=self.background_image)
            background_label.place(x=0, y=0, relwidth=1, relheight=1)
            root.geometry('854x640')
            root.resizable(False, False)
            load_game_btn = Button(root, text='Load Game', state=DISABLED,
                                   font=('Arial', 12, 'bold'), width=20,
                                   height=2, bg='#A31997', fg='#FFFFFF',
                                   command=self.load_game)
            if save_file_exists:
                load_game_btn.config(state=NORMAL, cursor='hand2')
            new_game_btn = Button(root, text='New Game',
                                  font=('Arial', 12, 'bold'), width=20,
                                  height=2, bg='#A31997', fg='#FFFFFF',
                                  cursor="hand2", command=self.get_details)
            cheat_code_btn = Button(root, text='Cheat Codes', font=('Arial', 12, 'bold'), width=20,
                                    height=2, bg='#A31997',fg='#FFFFFF', cursor="hand2")
            leader_board_btn = Button(root, text='Leaderboard', state=DISABLED, font=('Arial', 12, 'bold'), width=20, height=2,
                                      bg='#A31997', fg='#FFFFFF', command=self.leader_board)
            if leaderboard_file_exists:
                leader_board_btn.config(state=NORMAL, cursor='hand2')
            self.instruction_btn = Button(root, text='?', font=('Arial', 25, 'bold'), relief=FLAT, fg='#E55DD5', bg='black',
                                     command=self.instruction_page)
            exit_btn = Button(root, text='X', font=('Arial', 25, 'bold'), relief=FLAT, fg='#E55DD5', bg='black',
                              command=self.exit)
            # Creates the widgets on the screen
            load_game_btn.place(x=330, y=330)
            new_game_btn.place(x=330, y=390)
            cheat_code_btn.place(x=330, y=450)
            leader_board_btn.place(x=330, y=510)
            self.instruction_btn.place(x=780, y=20)
            exit_btn.place(x=30, y=20)

        @staticmethod
        def exit():
            sys.exit(0)

        def get_details(self):
            global get_user_details, get_details
            root.withdraw()
            get_details = Toplevel(self.master)
            get_details.geometry('480x160')
            get_details.config(bg='black')
            Label(get_details, text='Before you can continue, what would you like your name to be on the leaderboard?',
                  fg='#E55DD5', bg='black', font=('Arial', 12, 'bold'), wraplength=460).pack()
            Label(get_details, text='Your player name must be at least 3 characters long', fg='#E55DD5', bg='black',
                  font=('Arial', 12, 'bold'), wraplength=460).pack(pady=(0, 10))
            get_user_details = Entry(get_details, width=45, font=('Arial', 12, 'bold'))
            get_user_details.pack()
            self.done_btn = Button(get_details, text='Submit', command=self.create_player, font=('Arial', 12, 'bold'),
                                   bg='#E55DD5', state=DISABLED)
            get_details.bind('<Key>', self.update_button)
            self.done_btn.pack(pady=10)

        def update_button(self, _event=None):
            # Prevents the player from continuing if the length of their name is shorter than 3 characters
            user_input = get_user_details.get()
            if len(user_input.replace(" ", "")) >= 3:
                self.done_btn.config(state=NORMAL)
                get_details.bind('<Return>', self.create_player)

            if len(user_input.replace(" ", "")) < 3:
                self.done_btn.config(state=DISABLED)
                get_details.unbind('<Return>')

        def create_player(self, _event=None):
            global current_player
            current_player = Player(get_user_details.get())
            get_details.destroy()
            self.start_game()

        def start_game(self):
            global canvas, player_sprite, direction, start_game
            self.time_start = time.time()
            start_game = Toplevel(self.master)
            start_game.resizable(False, False)
            start_game.geometry('854x640')
            canvas = Canvas(start_game, bg='black', width=854, height=640)
            canvas.pack(expand=True, fill=BOTH)
            y = int(canvas.cget('height')) - 40
            x = int(canvas.cget('width')) - 20
            canvas.create_image(0, 0, image=self.main_background_image, anchor=NW)
            player_sprite = canvas.create_image(26, y, image=self.player_sprite_image)
            self.score_holder = canvas.create_text(20, 10, fill="white", font="Times 20 bold",
                                                   text="Score: " + str(current_player.playerScore), anchor=NW)
            self.live_holder = canvas.create_text(x, 10, fill="white", font="Times 20 bold",
                                                  text="Lives: " + str(current_player.playerLives), anchor=NE)
            canvas.focus_set()
            canvas.bind('<Left>', self.move_player_left)
            canvas.bind('<Right>', self.move_player_right)
            canvas.bind('<space>', self.shoot)
            canvas.bind('<p>', self.pause_game)
            canvas.bind('<z>', self.boss_key)
            canvas.bind('<Escape>', self.quit_menu)
            canvas.bind('gimme', self.cheat_one)
            canvas.bind('1000', self.cheat_two)
            canvas.bind('boss', self.cheat_three)
            canvas.bind('stall', self.cheat_four)
            self.set_enemies()
            self.enemy_shoot()
            self.move_bullet()
            self.move_enemies()
            self.next_check()

        def cheat_one(self, _event=None):
            current_player.playerLives += 10
            canvas.itemconfig(self.live_holder, text='Lives: ' + str(current_player.playerLives))

        def cheat_two(self, _event=None):
            current_player.playerLives += 1000
            canvas.itemconfig(self.live_holder, text='Lives: ' + str(current_player.playerLives))

        def cheat_three(self, _event=None):
            root.after_cancel(self.enemy_shoot_after)

        def cheat_four(self, _event=None):
            root.after_cancel(self.enemy_shoot_after)
            root.after_cancel(self.move_enemies_after)

        def quit_menu_back(self):
            root.after_cancel(self.next_check_after)
            canvas.destroy()
            self.bullets_player = []  # Stores the bullets of the player
            self.bullets_enemies = []  # Stores the bullets of the enemies
            self.allowed_to_shoot = []  # Stores the enemies that are allowed to shoot
            self.temp_enemies = []  # Stores the index of previous enemies and current ones
            self.enemies = []  # Stores the enemies
            self.counter = 0  # Initialises the counter to update the jumper variable
            self.direction = -1
            self.max_enemies = 10  # Initialises the counter for the max number of enemies on the screen
            self.enemies_speed = 10  # Initialises the speed of the enemies
            self.pause_boolean = False
            self.boss_key_boolean = False
            self.quit_boolean = False
            self.time_start = 0
            self.time_check = 0
            self.leader_board_top = None
            self.enemy_player_collision = False
            self.quit_top.destroy()
            self.quit_top = None
            start_game.destroy()
            root.destroy()

        def quit_menu(self, _event=None):
            canvas.unbind('<Left>')
            canvas.unbind('<Right>')
            canvas.unbind('<space>')
            canvas.unbind('<p>')
            canvas.unbind('<z>')
            canvas.unbind('<Escape>')
            root.after_cancel(self.enemy_shoot_after)
            root.after_cancel(self.detect_collision_after)
            root.after_cancel(self.move_bullet_after)
            root.after_cancel(self.next_check_after)
            root.after_cancel(self.after_move_down_after)
            root.after_cancel(self.move_enemies_after)
            self.quit_boolean = not self.quit_boolean
            try:
                if self.quit_top == None or not self.quit_top.winfo_exists():
                    check_if_exists = False
                else:
                    check_if_exists = True
            except NameError or TypeError:
                check_if_exists = True
            if not check_if_exists:
                self.quit_top = Toplevel(self.master)
                self.quit_top.title('Options')
                self.quit_top.config(bg='black')
                quit_btn = Button(self.quit_top, text='Quit', font=('Arial', 20, 'bold'), cursor='hand2', bg='#A31997',
                                  fg='black', command=self.quit_menu_back)
                quit_btn.grid(row=0, column=0, padx=10, pady=10, sticky=EW)
                leader_board_btn = Button(self.quit_top, text='Leaderboard', font=('Arial', 20, 'bold'), bg='#A31997',
                                          fg='black', command=self.leader_board, state=DISABLED)
                leader_board_btn.grid(row=1, column=0, padx=10, pady=10, sticky=EW)
                if leaderboard_file_exists:
                    leader_board_btn.config(state=NORMAL, cursor='hand2')
                self.quit_top.grid_columnconfigure(0, weight=1)
                self.quit_top.grid_rowconfigure(0, weight=1)
                self.quit_top.grid_rowconfigure(1, weight=1)
            if self.quit_boolean:
                self.quit_top.bind('<Escape>', self.quit_menu)
                self.quit_top.focus_set()
            else:
                self.quit_top.unbind('<Escape>')
                self.quit_top.destroy()
                y = int(canvas.cget('height')) // 2
                x = int(canvas.cget('width')) // 2
                timer_rect = canvas.create_rectangle(x - 30, y - 30, x + 30, y + 30, fill='#A31997')
                timer_count = canvas.create_text(x, y, fill='white', font="Times 20 bold", text='')
                canvas.itemconfig(timer_count, text='3')
                canvas.update()
                time.sleep(1)
                canvas.itemconfig(timer_count, text='2')
                canvas.update()
                time.sleep(1)
                canvas.itemconfig(timer_count, text='1')
                canvas.update()
                time.sleep(1)
                canvas.delete(timer_rect)
                canvas.delete(timer_count)
                canvas.update()
                self.enemy_shoot()
                self.move_bullet()
                self.next_check()
                self.move_enemies()
                # for enemy in self.enemies:
                #     enemy.animate_enemies_still()
                canvas.bind('<Left>', self.move_player_left)
                canvas.bind('<Right>', self.move_player_right)
                canvas.bind('<space>', self.shoot)
                canvas.bind('<Escape>', self.quit_menu)
                canvas.bind('<p>', self.pause_game)
                canvas.bind('<z>', self.boss_key)

        def pause_game(self, _event=None):
            self.pause_boolean = not self.pause_boolean
            if self.pause_boolean:
                canvas.unbind('<Left>')
                canvas.unbind('<Right>')
                canvas.unbind('<space>')
                root.after_cancel(self.enemy_shoot_after)
                root.after_cancel(self.detect_collision_after)
                root.after_cancel(self.move_bullet_after)
                root.after_cancel(self.next_check_after)
                root.after_cancel(self.after_move_down_after)
                root.after_cancel(self.move_enemies_after)
                # for enemy in self.enemies:
                #     root.after_cancel(enemy.animate_enemies_move_after)
                #     root.after_cancel(enemy.animate_enemies_still_after)
            else:
                canvas.unbind('<p>')
                y = int(canvas.cget('height')) // 2
                x = int(canvas.cget('width')) // 2
                timer_rect = canvas.create_rectangle(x-30, y-30, x+30, y+30, fill='#A31997')
                timer_count = canvas.create_text(x, y, fill='white', font="Times 20 bold", text='')
                canvas.itemconfig(timer_count, text='3')
                canvas.update()
                time.sleep(1)
                canvas.itemconfig(timer_count, text='2')
                canvas.update()
                time.sleep(1)
                canvas.itemconfig(timer_count, text='1')
                canvas.update()
                time.sleep(1)
                canvas.delete(timer_rect)
                canvas.delete(timer_count)
                canvas.update()
                self.enemy_shoot()
                self.move_bullet()
                self.next_check()
                self.move_enemies()
                # for enemy in self.enemies:
                #     enemy.animate_enemies_still()
                canvas.bind('<Left>', self.move_player_left)
                canvas.bind('<Right>', self.move_player_right)
                canvas.bind('<space>', self.shoot)
                canvas.bind('<Escape>', self.quit_menu)
                canvas.bind('<p>', self.pause_game)

        def boss_key(self, _event=None):
            self.time_check = time.time()
            if self.time_check - self.time_start > 0.7:
                self.boss_key_boolean = not self.boss_key_boolean
                if self.boss_key_boolean:
                    canvas.unbind('<Left>')
                    canvas.unbind('<Right>')
                    canvas.unbind('<space>')
                    canvas.unbind('<p>')
                    canvas.unbind('<Escape>')
                    root.after_cancel(self.enemy_shoot_after)
                    root.after_cancel(self.detect_collision_after)
                    root.after_cancel(self.move_bullet_after)
                    root.after_cancel(self.next_check_after)
                    root.after_cancel(self.after_move_down_after)
                    root.after_cancel(self.move_enemies_after)
                    # for enemy in self.enemies:
                    #     root.after_cancel(enemy.animate_enemies_move_after)
                    #     root.after_cancel(enemy.animate_enemies_still_after)
                    self.boss_window = Toplevel(self.master)
                    boss_window_canvas = Canvas(self.boss_window)
                    boss_window_canvas.pack(expand=True, fill=BOTH)
                    self.boss_window.focus_set()
                    boss_window_canvas.create_image(0, 0, image=self.boss_key_image, anchor=NW)
                    self.boss_window.attributes("-fullscreen", True)
                    self.boss_window.bind('<z>', self.boss_key)
                else:
                    self.boss_window.unbind('<z>')
                    canvas.unbind('<z>')
                    self.boss_window.destroy()
                    y = int(canvas.cget('height')) // 2
                    x = int(canvas.cget('width')) // 2
                    timer_rect = canvas.create_rectangle(x-30, y-30, x+30, y+30, fill='#A31997')
                    timer_count = canvas.create_text(x, y, fill='white', font="Times 20 bold", text='')
                    canvas.itemconfig(timer_count, text='3')
                    canvas.update()
                    time.sleep(1)
                    canvas.itemconfig(timer_count, text='2')
                    canvas.update()
                    time.sleep(1)
                    canvas.itemconfig(timer_count, text='1')
                    canvas.update()
                    time.sleep(1)
                    canvas.delete(timer_rect)
                    canvas.delete(timer_count)
                    canvas.update()
                    canvas.bind('<Left>', self.move_player_left)
                    canvas.bind('<Right>', self.move_player_right)
                    canvas.bind('<space>', self.shoot)
                    canvas.bind('<Escape>', self.quit_menu)
                    self.enemy_shoot()
                    self.move_bullet()
                    self.next_check()
                    self.move_enemies()
                    # for enemy in self.enemies:
                    #     enemy.animate_enemies_still()
                    canvas.bind('<z>', self.boss_key)

        def save_mid_game(self):
            save_file = open('savedData.txt', 'w+')
            save_file.write(current_player.playerName + "\n" + str(current_player.playerScore) + '\n' +
                            str(current_player.playerLives) + "\n" + str(self.max_enemies))

        @staticmethod
        def save_leaderboard():
            save_file = open('leaderboardData.txt', 'a+')
            save_file.write(current_player.playerName + "\n" + str(current_player.playerScore) + '\n')

        def shoot(self, _event=None):
            if len(self.bullets_player) < 6:
                current_player.playerPosition = canvas.coords(player_sprite)
                bullet_start_x = current_player.playerPosition[0] - 2
                bullet_start_y = current_player.playerPosition[1] - 29
                bullet_end_x = bullet_start_x + 4
                bullet_end_y = bullet_start_y + 15
                bullet_coordinates = bullet_start_x, bullet_start_y, bullet_end_x, bullet_end_y
                self.bullets_player.append(Bullet(canvas, bullet_coordinates))

        def enemy_shoot(self):
            self.allowed_to_shoot = []
            if len(self.enemies) > 0:
                if len(self.bullets_enemies) < 8:
                    for enemy in range(5):
                        if canvas.itemcget(self.temp_enemies[enemy][1].enemy, 'state') == 'normal':
                            self.allowed_to_shoot.append(self.temp_enemies[enemy][1].enemy)
                        else:
                            if canvas.itemcget(self.temp_enemies[enemy+5][1].enemy, 'state') == 'normal':
                                self.allowed_to_shoot.append(self.temp_enemies[enemy+5][1].enemy)
                            else:
                                try:
                                    if canvas.itemcget(self.temp_enemies[enemy+10][1].enemy, 'state') == 'normal':
                                        self.allowed_to_shoot.append(self.temp_enemies[enemy+10][1].enemy)
                                    else:
                                        if canvas.itemcget(self.temp_enemies[enemy+15][1].enemy, 'state') == 'normal':
                                            self.allowed_to_shoot.append(self.temp_enemies[enemy+15][1].enemy)
                                        else:
                                            if canvas.itemcget(self.temp_enemies[enemy+20][1].enemy, 'state') == 'normal':
                                                self.allowed_to_shoot.append(self.temp_enemies[enemy+20][1].enemy)
                                            else:
                                                if canvas.itemcget(self.temp_enemies[enemy+25][1].enemy, 'state') == 'normal':
                                                    self.allowed_to_shoot.append(self.temp_enemies[enemy+25][1].enemy)
                                                else:
                                                    if canvas.itemcget(self.temp_enemies[enemy+30][1].enemy, 'state') == 'normal':
                                                        self.allowed_to_shoot.append(self.temp_enemies[enemy+30][1].enemy)
                                                    else:
                                                        continue
                                except IndexError:
                                    continue
                    try:
                        enemy_coordinates = canvas.coords(random.choice(self.allowed_to_shoot))
                        x_left, x_right = enemy_coordinates[0]-2, enemy_coordinates[0]+2
                        y_top, y_bottom = enemy_coordinates[1]+20, enemy_coordinates[1]+40
                        self.bullets_enemies.append(Bullet(canvas, (x_left, y_top, x_right, y_bottom)))
                    except IndexError:
                        pass
            self.enemy_shoot_after = root.after(700, self.enemy_shoot)

        def move_bullet(self):
            for enum, bullet in enumerate(self.bullets_player):
                if canvas.coords(bullet.bullet)[1] < 0:
                    canvas.delete(bullet.bullet)
                    self.bullets_player.pop(enum)
                else:
                    bullet.move(canvas)
            for enum, bullet in enumerate(self.bullets_enemies):
                if canvas.coords(bullet.bullet)[1] > int(canvas.cget('height')):
                    canvas.delete(bullet.bullet)
                    self.bullets_enemies.pop(enum)
                else:
                    bullet.enemy_bullet(canvas)
            self.detect_collision_after = root.after(10, self.detect_collision)

        def set_enemies(self):
            number_of_rows_needed = self.max_enemies//5
            gap_x = (int(canvas.cget('width')) // 2)-146
            gap_y = (int(canvas.cget('height')) // 2)
            for row in range(number_of_rows_needed):
                for enemy in range(5):
                    gaps = gap_x, gap_y
                    self.enemies.append(Enemies(canvas, gaps))
                    gap_x += 55
                gap_x = (int(canvas.cget('width'))//2)-146
                gap_y -= 40
            for enum, enemy in enumerate(self.enemies):
                self.temp_enemies.append((enum, enemy))

        def detect_collision(self):
            counter_player_shoot = 0
            counter_enemy_shoot = 0
            player_bbox = canvas.bbox(player_sprite)
            if len(self.enemies) > 0:
                for enum_b, bullet in enumerate(self.bullets_player):
                    for enum_e, enemy in enumerate(self.enemies):
                        enemy.enemy_bbox = canvas.bbox(enemy.enemy)
                        enemy_box = enemy.enemy_bbox
                        bullet_box = bullet.bullet_bbox
                        if (bullet_box[0] in range(enemy_box[0], enemy_box[2])
                            or bullet_box[2] in range(enemy_box[0], enemy_box[2])) and (bullet_box[1] in
                                                                                        range(enemy_box[1], enemy_box[3])
                                                                                        or bullet_box[3] in
                                                                                        range(enemy_box[1], enemy_box[3])):
                            enemy.life_value -= 1
                            if enemy.life_value == 0:
                                canvas.itemconfig(enemy.enemy, state=DISABLED)
                                canvas.delete(enemy.enemy)
                                self.enemies.pop(enum_e)
                                current_player.playerScore += enemy.point_value
                                canvas.itemconfig(self.score_holder, text='Score: ' + str(current_player.playerScore))
                            canvas.delete(bullet.bullet)
                            if counter_player_shoot == 0:
                                self.bullets_player.pop(enum_b)
                                counter_player_shoot += 1
                            canvas.update()
                    counter_player_shoot = 0
                for enum_b, bullet in enumerate(self.bullets_enemies):
                    bullet_box = bullet.bullet_bbox
                    if (bullet_box[0] in range(player_bbox[0], player_bbox[2])
                        or bullet_box[2] in range(player_bbox[0], player_bbox[2])) and (bullet_box[1] in
                                                                                    range(player_bbox[1], player_bbox[3])
                                                                                    or bullet_box[3] in
                                                                                    range(player_bbox[1], player_bbox[3])):
                        current_player.lost_life()
                        canvas.itemconfig(self.live_holder, text='Lives: ' + str(current_player.playerLives))
                        canvas.delete(bullet.bullet)
                        if counter_enemy_shoot == 0:
                            self.bullets_enemies.pop(enum_b)
                            counter_enemy_shoot += 1
                        canvas.update()
                    counter_enemy_shoot = 0
                for enemy in self.enemies:
                    enemy.enemy_bbox = canvas.bbox(enemy.enemy)
                    enemy_box = enemy.enemy_bbox
                    if (enemy_box[0] in range(player_bbox[0], player_bbox[2])
                        or enemy_box[2] in range(player_bbox[0], player_bbox[2])) and (enemy_box[1] in
                                                                                       range(player_bbox[1],
                                                                                             player_bbox[3])
                                                                                       or enemy_box[3] in
                                                                                       range(player_bbox[1],
                                                                                             player_bbox[3])):
                        self.enemy_player_collision = True
                        break
            if current_player.playerLives == 0 or self.enemy_player_collision:
                self.game_over()
            else:
                self.move_bullet_after = root.after(30, self.move_bullet)

        def game_over(self):
            global canvas_game_over
            canvas.unbind('<Left>')
            canvas.unbind('<Right>')
            canvas.unbind('<space>')
            canvas.unbind('<p>')
            canvas.unbind('<z>')
            canvas.unbind('<Escape>')
            root.after_cancel(self.enemy_shoot_after)
            root.after_cancel(self.detect_collision_after)
            root.after_cancel(self.move_bullet_after)
            root.after_cancel(self.next_check_after)
            root.after_cancel(self.after_move_down_after)
            root.after_cancel(self.move_enemies_after)
            # for enemy in self.enemies:
            #     root.after_cancel(enemy.animate_enemies_move_after)
            #     root.after_cancel(enemy.animate_enemies_still_after)
            canvas.destroy()
            canvas_game_over = Canvas(start_game, bg='black', width=854, height=640)
            canvas_game_over.pack(expand=True, fill=BOTH)
            canvas_game_over.focus_set()
            x_mid = int(canvas_game_over.cget('width')) // 2
            x = int(canvas_game_over.cget('width'))
            y_mid = int(canvas_game_over.cget('height')) // 2
            canvas_game_over.create_image(0, 0, image=self.main_background_image, anchor=NW)
            canvas_game_over.create_rectangle(0, y_mid-60, x, y_mid+60, fill='#A31997')
            canvas_game_over.create_text(x_mid, y_mid, fill="white", font="Times 60 bold",
                                         text="Game Over")
            canvas_game_over.create_text(x_mid, 1.5*y_mid, fill="white", font="Times 20 bold",
                                         text="Press Q to go back to menu\nPress R to restart")
            canvas_game_over.bind('<q>', self.go_back)
            canvas_game_over.bind('<r>', self.restart)
            self.save_leaderboard()

        def restart(self, _event=None):
            root.after_cancel(self.enemy_shoot_after)
            root.after_cancel(self.detect_collision_after)
            root.after_cancel(self.move_bullet_after)
            root.after_cancel(self.next_check_after)
            root.after_cancel(self.after_move_down_after)
            root.after_cancel(self.move_enemies_after)
            self.bullets_player = []  # Stores the bullets of the player
            self.bullets_enemies = []  # Stores the bullets of the enemies
            self.allowed_to_shoot = []  # Stores the enemies that are allowed to shoot
            self.temp_enemies = []  # Stores the index of previous enemies and current ones
            self.enemies = []  # Stores the enemies
            self.counter = 0  # Initialises the counter to update the jumper variable
            self.direction = -1
            self.max_enemies = 10  # Initialises the counter for the max number of enemies on the screen
            self.pause_boolean = False
            self.boss_key_boolean = False
            self.quit_boolean = False
            self.time_start = 0
            self.time_check = 0
            self.leader_board_top = None
            self.quit_top = None
            self.enemy_player_collision = False
            current_player.playerLives = 3
            current_player.playerScore = 0
            canvas_game_over.destroy()
            start_game.destroy()
            self.start_game()

        def leader_board(self):
            leader_board_counter = 1
            leader_board_rowcounter = 2
            leader_board_names = []
            leader_board_score = []
            leader_board_display = []
            leader_board_data = open('leaderboardData.txt', 'r')
            leader_board_iterator = leader_board_data.readlines()
            leader_board_iterator = [item.rstrip("\n") for item in leader_board_iterator]
            for item_it in leader_board_iterator:
                try:
                    item_it = int(item_it)
                    leader_board_score.append(item_it)
                except ValueError:
                    leader_board_names.append(item_it)
            for i in range(5):
                try:
                    checker = leader_board_score.index(max(leader_board_score))
                    leader_board_display.append((leader_board_score[checker], leader_board_names[checker]))
                    leader_board_names.pop(checker)
                    leader_board_score.pop(checker)
                except ValueError:
                    continue
            try:
                if self.leader_board_top == None or not self.leader_board_top.winfo_exists():
                    check_if_exists = False
                else:
                    check_if_exists = True
            except NameError or TypeError:
                check_if_exists = True
            if not check_if_exists:
                self.leader_board_top = Toplevel(self.master)
                self.leader_board_top.title('Leaderboard')
                self.leader_board_top.config(bg='black')
                leader_board_window = Frame(self.leader_board_top, highlightbackground="#A31997",
                                            highlightcolor="#A31997",
                                            highlightthickness=5, width=100, height=100, bd=5, bg='black')
                leader_board_window.pack(pady=10, padx=10, expand=True, fill=BOTH)
                leader_board_label = Label(leader_board_window, text='LEADERBOARD', font=('Arial', 20, 'bold'),
                                           bg='black', fg='#A31997')
                leader_board_label.grid(row=0, column=0, pady=20, columnspan=3)
                Label(leader_board_window, text='Name', font=('Arial', 20, 'bold', 'underline'), bg='black',
                      fg='#A31997').grid(row=1, column=0, pady=5, padx=10)
                Label(leader_board_window, text='    ', font=('Arial', 20, 'bold'), bg='black',
                      fg='#A31997').grid(row=1, column=1, pady=5, padx=10)
                Label(leader_board_window, text='Score', font=('Arial', 20, 'bold', 'underline'), bg='black',
                      fg='#A31997').grid(row=1, column=2, pady=5, padx=10)
                for i in range(5):
                    try:
                        name_to_print = str(leader_board_counter)+'. '+str(leader_board_display[i][1])
                        score_to_print = str(leader_board_display[i][0])
                        Label(leader_board_window, text=name_to_print, font=('Arial', 20, 'bold'), bg='black',
                              fg='white').grid(row=leader_board_rowcounter, column=0, ipadx=(10))
                        Label(leader_board_window, text=score_to_print, font=('Arial', 20, 'bold'), bg='black',
                              fg='white').grid(row=leader_board_rowcounter, column=2, padx=5)
                        leader_board_counter += 1
                        leader_board_rowcounter += 1
                    except IndexError:
                        continue
                for i in range(7):
                    leader_board_window.grid_rowconfigure(i, weight=1)
                for i in range(3):
                    leader_board_window.grid_columnconfigure(i, weight=1)
                Label(leader_board_window, text='    ', font=('Arial', 20, 'bold'), bg='black',
                      fg='#A31997').grid(row=7, column=1, pady=5, padx=10)
                close_leader = Button(leader_board_window, text='X', font=('Arial', 20, 'bold'), bg='#A31997',
                                      fg='black', command=self.close_leader_board)
                close_leader.grid(row=8, column=0, pady=10, padx=15)

        def close_leader_board(self):
            self.leader_board_top.destroy()

        @staticmethod
        def go_back(_event=None):
            canvas_game_over.destroy()
            start_game.destroy()
            root.destroy()

        @staticmethod
        def move_player_left(self, _event=None):
            current_player.playerPosition = canvas.coords(player_sprite)
            if current_player.playerPosition[0] <= 26:
                canvas.coords(player_sprite, 26, int(canvas.cget('height')) - 30)
            else:
                canvas.move(player_sprite, -10, 0)

        @staticmethod
        def move_player_right(self, _event=None):
            current_player.playerPosition = canvas.coords(player_sprite)
            right_limit = int(canvas.cget('width')) - 26
            if current_player.playerPosition[0] >= right_limit:
                canvas.coords(player_sprite, right_limit, int(canvas.cget('height')) - 30)
            else:
                canvas.move(player_sprite, 10, 0)

        def next_check(self):
            if len(self.enemies) == 0:
                root.after_cancel(self.next_check_after)
                root.after_cancel(self.enemy_shoot_after)
                root.after_cancel(self.after_move_down_after)
                root.after_cancel(self.move_enemies_after)
                self.temp_enemies = []
                self.enemies = []
                if self.max_enemies < 35:
                    self.max_enemies += 5
                # if self.counter == 1:
                #     jumper = 100
                # else:
                #     jumper = ((self.counter**2)-self.counter)*100
                #     if current_player.playerScore >= jumper:
                #         self.max_enemies += 5
                #         self.counter += 1
                #         if self.enemies_speed == 120:
                #             self.enemies_speed += 10
                self.save_mid_game()
                self.set_enemies()
                self.move_enemies()
                self.enemy_shoot()
                if not self.quit_boolean:
                    self.next_check()
            self.next_check_after = root.after(50, self.next_check)

        def move_enemies(self):
            global moved_down
            if not self.enemy_player_collision:
                try:
                    c_width = int(canvas.cget('width'))
                    move_size = 0
                    almost_on_left_border = False
                    moved_down = False
                    almost_on_right_border = False
                    for enemy in self.enemies:
                        enemy.animate_enemies_still()
                        if canvas.coords(enemy.enemy)[0] < 46:
                            almost_on_left_border = True
                            move_size = -26+canvas.coords(enemy.enemy)[0]
                            break
                        elif canvas.coords(enemy.enemy)[0] > c_width-46:
                            almost_on_right_border = True
                            move_size = c_width-(canvas.coords(enemy.enemy)[0]+26)
                            break
                    if almost_on_left_border:
                        for enemy in self.enemies:
                            enemy.animate_enemies_move()
                        Enemies.move_enemy_across_fixed(-move_size, canvas)
                        canvas.update()
                        Enemies.move_enemy_down(canvas)
                        canvas.update()
                        moved_down = True
                    elif almost_on_right_border:
                        for enemy in self.enemies:
                            enemy.animate_enemies_move()
                        Enemies.move_enemy_across_fixed(move_size, canvas)
                        canvas.update()
                        Enemies.move_enemy_down(canvas)
                        canvas.update()
                        moved_down = True
                    self.after_move_down_after = root.after(350, self.after_move_down)
                except _tkinter.TclError:
                    pass

        def after_move_down(self):
            global moved_down
            if moved_down:
                self.direction = self.direction*(-1)
            for enemy in self.enemies:
                enemy.animate_enemies_move()
            Enemies.move_enemy_across(self.direction, canvas)
            canvas.update()
            self.move_enemies_after = root.after(350, self.move_enemies)

        def toggle_fullscreen(self):
            self.start_game.attributes("-fullscreen", True)

        def end_fullscreen(self):
            self.start_game.attributes("-fullscreen", False)

        def load_game(self):
            global current_player
            save_data = open('savedData.txt', 'r')
            save_data_iterator = save_data.readlines()
            save_data_iterator = [item.rstrip("\n") for item in save_data_iterator]
            current_player = Player(save_data_iterator[0])
            current_player.playerScore = int(save_data_iterator[1])
            current_player.playerLives = int(save_data_iterator[2])
            self.max_enemies = int(save_data_iterator[3])
            root.withdraw()
            self.start_game()

        def instruction_page(self):
            if self.instruction_window == None or not self.instruction_window.winfo_exists():
            # Creates a window to display the game instructions
                self.instruction_window = Toplevel(self.master)
                self.instruction_window.title('Instructions')
                self.instruction_window.geometry('480x360')
                self.instruction_window.resizable(False, False)
                self.instruction_window.config(bg='black')
                instruction_dict = [
                    '1. Press the right and left arrow keys to move right and left respectively',
                    '2. Press the space bar to shoot',
                    '3. Press the Z key to go into Boss Mode',
                    '4. Press the P key to pause the game',
                    '5. Press the S key to save the game'
                ]
                instructions = Frame(self.instruction_window, bg='black')
                instructions.config(highlightthickness=5, highlightbackground='#E55DD5')
                instructions.pack(padx=10, pady=10, ipady=10, ipadx=20, expand=TRUE, fill=X)
                Label(instructions, text='INSTRUCTIONS', font=('Arial', 25, 'bold', 'underline'), fg='#E55DD5', bg='black').pack(pady=10)
                for instruct in instruction_dict:
                    Label(instructions, text=instruct, font=('Arial', 12), fg='#E55DD5', bg='black',
                          wraplength=360).pack(fill=X, pady=10, anchor=W)


class Bullet:
    def __init__(self, canvas, coordinates):
        self.bullet = canvas.create_rectangle(coordinates, fill='#A31997', tags='bullet')
        self.bullet_bbox = canvas.bbox(self.bullet)

    def move(self, canvas):
        canvas.move(self.bullet, 0, -15)
        self.bullet_bbox = canvas.bbox(self.bullet)

    def enemy_bullet(self, canvas):
        canvas.move(self.bullet, 0, 15)
        self.bullet_bbox = canvas.bbox(self.bullet)


class Player:
    def __init__(self, name):
        self.playerName = name
        self.playerLives = 3
        self.playerScore = 0
        self.playerPosition = 0, 0

    def lost_life(self):
        self.playerLives -= 1


class Enemies:
    def __init__(self, canvas, coordinates):
        self.image_still, self.image_move, self.point_value, self.life_value = self.random_enemy_ranks()
        self.enemy = canvas.create_image(coordinates, image=self.image_still, tags='enemy_sprite', state=NORMAL)
        self.enemy_bbox = canvas.bbox(self.enemy)
        canvas.update()
        self.point_value = self.point_value
        self.life_value = self.life_value
        self.animate_enemies_still_after = 0
        self.animate_enemies_move_after = 0

    def animate_enemies_still(self):
        canvas.itemconfig(self.enemy, image=self.image_still)
        canvas.update()

    def animate_enemies_move(self):
        canvas.itemconfig(self.enemy, image=self.image_move)
        canvas.update()

    def move_enemy_across(direction, canvas):
        canvas.move('enemy_sprite', (20*direction), 0)
        canvas.update()

    def move_enemy_across_fixed(distance, canvas):
        canvas.move('enemy_sprite', distance, 0)
        canvas.update()

    def move_enemy_down(canvas):
        canvas.move('enemy_sprite', 0, 40)
        canvas.update()

    def random_enemy_ranks(self):
        if current_player.playerScore == 0:
            self.image_still = PhotoImage(file='10points_still.png')
            self.image_move = PhotoImage(file='10points_move.png')
            self.point_value = 10
            self.life_value = 1
        else:
            rand_choice = random.randint(1, 6)
            if rand_choice == 1:
                self.image_still = PhotoImage(file='10points_still.png')
                self.image_move = PhotoImage(file='10points_move.png')
                self.point_value = 10
                self.life_value = 1
            elif rand_choice == 2:
                self.image_still = PhotoImage(file='25points_still.png')
                self.image_move = PhotoImage(file='25points_move.png')
                self.point_value = 25
                self.life_value = 1
            elif rand_choice == 3:
                self.image_still = PhotoImage(file='50points_still.png')
                self.image_move = PhotoImage(file='50points_move.png')
                self.point_value = 50
                self.life_value = 1
            elif rand_choice == 4:
                self.image_still = PhotoImage(file='75points_still.png')
                self.image_move = PhotoImage(file='75points_move.png')
                self.point_value = 75
                self.life_value = 1
            elif rand_choice == 5:
                self.image_still = PhotoImage(file='100points_still.png')
                self.image_move = PhotoImage(file='100points_move.png')
                self.point_value = 100
                self.life_value = 2
            elif rand_choice == 6:
                self.image_still = PhotoImage(file='200points_still.png')
                self.image_move = PhotoImage(file='200points_move.png')
                self.point_value = 200
                self.life_value = 3
        return self.image_still, self.image_move, self.point_value, self.life_value


# Checks if the user has a saved file already
save_file_exists = True
leaderboard_file_exists = True
try:
    save_file = open('savedData.txt', 'r')
except FileNotFoundError:
    save_file_exists = False
try:
    leaderboardData = open('leaderboardData.txt', 'r')
except FileNotFoundError:
    leaderboard_file_exists = False

while True:
    root = Tk()
    app = ShooterGame(root)
    root.mainloop()
