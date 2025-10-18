#spele_metodes.py
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import math
import pygame

pygame.mixer.init()

class SpeleMetodes:
    def __init__(self):
        self.pawn_images = []
        
    def play_sound(self, sound_file):
        try:
            sound = pygame.mixer.Sound(sound_file)
            sound.set_volume(self.volume / 100 if hasattr(self, "volume") else 0.5)
            sound.play()
        except Exception as e:
            print(f"Sound error: {e}")

    def custom_error(self, title, message):
        error_win = tk.Toplevel(self.root)
        error_win.title(title)
        error_win.geometry("350x150")
        error_win.configure(bg="#ffe6e6")
        error_label = tk.Label(error_win, text=message, font=("Helvetica", 12, "bold"),
                               bg="#ffe6e6", fg="#a80000", wraplength=300)
        error_label.pack(pady=20, padx=20)
        ok_button = tk.Button(error_win, text="OK", font=("Helvetica", 12, "bold"), bg="#a80000", fg="white",
                              command=lambda: [self.play_sound("button.mp3"), error_win.destroy()])
        ok_button.pack(pady=10)

    def load_stats(self):
        self.player_stats = {}
        try:
            with open("player_stats.txt", "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        parts = line.split(",")
                        if len(parts) >= 5:
                            name = parts[0]
                            self.player_stats[name] = {
                                "regular_games": int(parts[1]),
                                "regular_wins": int(parts[2]),
                                "tournament_games": int(parts[3]),
                                "tournament_wins": int(parts[4])
                            }
        except FileNotFoundError:
            self.player_stats = {}

    def save_stats(self):
        with open("player_stats.txt", "w", encoding="utf-8") as f:
            for name, stats in self.player_stats.items():
                f.write(f"{name},{stats['regular_games']},{stats['regular_wins']},{stats['tournament_games']},{stats['tournament_wins']}\n")

    def saktSpele(self):
        self.play_sound("start.mp3")
        if self.game_mode.get() == "regular":
            self.saktSpeleRegular()
        else:
            self.saktSpeleTournament()

    def saktSpeleRegular(self):
        self.in_game = True 
        n = self.speletajuVar.get()
        self.speletaji = []
        used_names = set() 
        for i in range(n):
            vards = self.speletajuIevades[i].get().strip()
            if not vards:
                if self.computer_players_enabled.get():
                 vards = f"Dators {i+1}"
                 is_human = False
                else:
                    messagebox.showerror("Kļūda", f"Lūdzu ievadiet spēlētāja {i+1} vārdu!")
                    return
            else:
                if len(vards) < 3 or len(vards) > 15:
                    messagebox.showerror("Kļūda", "Spēlētāju vārdam jābūt no 3 līdz 15 burtu garumam!")
                    return
                is_human = True
                if vards in used_names:
                    messagebox.showerror("Kļūda", f"Spēlētāja vārds '{vards}' ir jau izmantots! Lūdzu izvēlies citu.")
                    return
                used_names.add(vards)
            if is_human and vards not in self.player_stats:
                self.player_stats[vards] = {"regular_games": 0, "regular_wins": 0, "tournament_games": 0, "tournament_wins": 0}
            self.speletaji.append({
                "vards": vards,
                "krasa": self.figuruKrasas[i],
                "laukums": 1,
                "beidzis": False,
                "figura_id": None,
                "pawn_image": None,
                "human": is_human
            })
        random.shuffle(self.speletaji)
        self.aktiviSpeletaji = list(range(len(self.speletaji)))
        self.aktualaisIndekss = 0
        self.beiguKartiba = []
        self.setup_frame.pack_forget()
        self.izveidotRami()


    def saktSpeleTournament(self):
        self.in_game = True  
        self.tournament_players = []
        used_names = set()  
        for i in range(8):
            vards = self.speletajuIevades[i].get().strip()
            if not vards:
                if self.computer_players_enabled.get():
                    vards = f"Dators {i+1}"
                    is_human = False
                else:
                    messagebox.showerror("Kļūda", f"Lūdzu ievadiet spēlētāja {i+1} vārdu!")
                    return
            else:
                if len(vards) < 3 or len(vards) > 15:
                    messagebox.showerror("Kļūda", "Spēlētāju vārdam jābūt no 3 līdz 15 burtu garumam!")
                    return
                is_human = True
                if vards in used_names:
                    messagebox.showerror("Kļūda", f"Spēlētāja vārds '{vards}' ir jau izmantots! Lūdzu izvēlies citu.")
                    return
                used_names.add(vards)
            if is_human and vards not in self.player_stats:
                self.player_stats[vards] = {"regular_games": 0, "regular_wins": 0, "tournament_games": 0, "tournament_wins": 0}
            self.tournament_players.append({
                "vards": vards,
                "laukums": 1,
                "beidzis": False,
                "figura_id": None,
                "pawn_image": None,
                "human": is_human
            })
        random.shuffle(self.tournament_players)
        group1 = self.tournament_players[:4]
        group2 = self.tournament_players[4:]
        colors_group1 = ["indianred", "blue", "green", "gold"]
        colors_group2 = ["purple", "cyan", "orange", "pink"]
        for i, player in enumerate(group1):
            player["krasa"] = colors_group1[i]
        for i, player in enumerate(group2):
            player["krasa"] = colors_group2[i]
        for group in (group1, group2):
            for player in group:
                player["laukums"] = 1
                player["beidzis"] = False

        self.setup_frame.pack_forget()

        self.tournament_frame = tk.Frame(self.root)
        self.tournament_frame.pack(padx=10, pady=10, fill="both", expand=True)

        # kreisās puses grupa
        left_frame = tk.Frame(self.tournament_frame, bd=2, relief="ridge")
        left_frame.pack(side=tk.LEFT, padx=5, fill="both", expand=True)

        # labās puses grupas
        right_frame = tk.Frame(self.tournament_frame, bd=2, relief="ridge")
        right_frame.pack(side=tk.LEFT, padx=5, fill="both", expand=True)

        settings_panel = tk.Frame(self.tournament_frame, bd=2, relief="ridge", bg="#F0F8FF")
        settings_panel.pack(side=tk.RIGHT, fill="y", padx=5, pady=5)
        self.iesatijumi_tourn_btn = tk.Button(
            settings_panel,
            text="⚙️ Iestatījumi",
            command=lambda: [self.play_sound("button.mp3"), self.show_iesatijumi(mode="game")],
            font=("Helvetica", 12, "bold"),
            bg="#337ab7",
            fg="white"
        )
        self.iesatijumi_tourn_btn.pack(expand=True, fill="both", padx=10, pady=10)

        self.left_board = self.createTournamentBoard(group1, left_frame, board_side="left")
        self.right_board = self.createTournamentBoard(group2, right_frame, board_side="right")
        left_frame.bind_all("<space>", lambda e: self.tournamentDiceThrow(self.left_board, e))
        right_frame.bind_all("<Return>", lambda e: self.tournamentDiceThrow(self.right_board, e))

    def izveidotRami(self):
        import random
        from PIL import Image, ImageTk
        self.game_frame = tk.Frame(self.root)
        self.game_frame.pack(padx=10, pady=10)
        self.canvas = tk.Canvas(self.game_frame, width=self.board_width, height=self.board_height)
        self.canvas.grid(row=0, column=0, rowspan=6, padx=5, pady=5)
        self.board_image = ImageTk.PhotoImage(Image.open("circus_board.png").resize((self.board_width, self.board_height)))
        self.canvas.create_image(0, 0, anchor="nw", image=self.board_image)
        self.info_label = tk.Label(self.game_frame, text="", font=("Helvetica", 14))
        self.info_label.grid(row=0, column=1, sticky="nw")
        self.dice_text_label = tk.Label(self.game_frame, text="Metamais kauliņš: ", font=("Helvetica", 12))
        self.dice_text_label.grid(row=1, column=1, sticky="nw")
        init_val = random.randint(1,6)
        self.dice_photo = self.metKaulinAtteli(init_val)
        self.dice_image_label = tk.Label(self.game_frame, image=self.dice_photo)
        self.dice_image_label.grid(row=1, column=2, sticky="nw", padx=5)
        self.dice_image_label.bind("<Button-1>", self.metKaulinu)
        self.message_label = tk.Label(self.game_frame, text="", justify="left", font=("Helvetica", 12))
        self.message_label.grid(row=2, column=1, sticky="nw")
        self.score_frame = tk.Frame(self.game_frame)
        self.score_frame.grid(row=3, column=1, sticky="nw", pady=10)
        self.score_labels = []
        
        self.pawn_images = []
        for player in self.speletaji:
            lbl = tk.Label(self.score_frame, text=f"{player['vards']}: Plāksne {player['laukums']}",
                        fg=player["krasa"], font=("Helvetica", 12), bd=2, relief="ridge", width=20)
            lbl.pack(anchor="w", pady=2)
            self.score_labels.append(lbl)
        self.log_text = tk.Text(self.game_frame, height=10, width=45, state="disabled", font=("Helvetica", 10))
        self.log_text.grid(row=4, column=1, columnspan=2, sticky="nw", pady=5)
        for c in ["indianred", "blue", "green", "gold", "purple", "cyan", "orange", "pink"]:
            self.log_text.tag_config(c, foreground=c)
        
        for player in self.speletaji:
            pawn_image = self.spelKaulinAtteli(player["krasa"])
            token = self.canvas.create_image(0, 0, image=pawn_image)
            player["figura_id"] = token
            player["pawn_image"] = pawn_image
            self.pawn_images.append(pawn_image)
        self.atjaunotFiguruPozicijas()
        self.atjaunotInfoEtiketi()
        self.atjaunotRezLapu()

    def metKaulinAtteli(self, dice_value):
        dice_files = ["dice1.png", "dice2.png", "dice3.png", "dice4.png", "dice5.png", "dice6.png"]
        img = Image.open(dice_files[dice_value - 1])
        w, h = img.size
        new_w, new_h = int(w * 0.5), int(h * 0.5)
        img = img.resize((new_w, new_h))
        return ImageTk.PhotoImage(img)

    def spelKaulinAtteli(self, color):
        pawn_files = {"indianred": "red_pawn.png", "blue": "blue_pawn.png",
                      "green": "green_pawn.png", "gold": "yellow_pawn.png",
                      "purple": "purple_pawn.png", "cyan": "cyan_pawn.png",
                      "orange": "orange_pawn.png", "pink": "pink_pawn.png"}
        img = Image.open(pawn_files[color])
        orig_w, orig_h = img.size
        scale = min((self.tile_width * 0.7) / orig_w, (self.tile_height * 0.7) / orig_h)
        new_w, new_h = int(orig_w * scale), int(orig_h * scale)
        img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(img)

    def spelKaulinAtteli_tournament(self, color, board):
        pawn_files = {"indianred": "red_pawn.png", "blue": "blue_pawn.png",
                      "green": "green_pawn.png", "gold": "yellow_pawn.png",
                      "purple": "purple_pawn.png", "cyan": "cyan_pawn.png",
                      "orange": "orange_pawn.png", "pink": "pink_pawn.png"}
        img = Image.open(pawn_files[color])
        orig_w, orig_h = img.size
        scale = min((board["tile_width"] * 0.7) / orig_w, (board["tile_height"] * 0.7) / orig_h)
        new_w, new_h = int(orig_w * scale), int(orig_h * scale)
        img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(img)

    def metKaulinu(self, event=None):
        if event is not None:
            current_player = self.speletaji[self.aktiviSpeletaji[self.aktualaisIndekss]]
            if not current_player.get("human", True):
                return
        if self.animating or not self.aktiviSpeletaji or self.dice_on_cooldown:
            return
        self.dice_on_cooldown = True
        self.animating = True
        self.animetKaulinu(0)
        self._play_random_sound("diceThrow", 4)

    def animetKaulinu(self, cycle):
        dice_value = random.randint(1,6)
        self.dice_photo = self.metKaulinAtteli(dice_value)
        self.dice_image_label.config(image=self.dice_photo)
        self.dice_text_label.config(text=f"Metamais kauliņš: {dice_value}")
        if cycle < 10:
            self.root.after(80, self.animetKaulinu, cycle+1)
        else:
            self.apstradatKaulMetienu(dice_value)
            self.animating = False

    def apstradatKaulMetienu(self, roll):
        aktSpeletajs = self.speletaji[self.aktiviSpeletaji[self.aktualaisIndekss]]
        self.dice_text_label.config(text=f"Metamais kauliņš: {roll}")
        vecais = aktSpeletajs["laukums"]
        jauns = vecais + roll
        if jauns > 120:
            extra = jauns - 120
            final_tile = 120 if (extra % 2 == 0) else 119
            def pec_120_sasniegsanas():
                self.pievienotLogu(f"{aktSpeletajs['vards']} uzlēca uz 120. plāksni!", aktSpeletajs["krasa"])
                def pec_atleksanas():
                    self.pievienotLogu(f"{aktSpeletajs['vards']} atlec uz {final_tile}. plāksnes!", aktSpeletajs["krasa"])
                    aktSpeletajs["laukums"] = final_tile
                    self.atjaunotFiguruPozicijas()
                    if final_tile in self.ladders:
                        dest = self.ladders[final_tile]
                        def pec_trepes():
                            self.pievienotLogu(f"{aktSpeletajs['vards']} uzkāpa uz trepītēm un nonāca uz {dest}. plāksni!", aktSpeletajs["krasa"])
                            aktSpeletajs["laukums"] = dest
                            self.atjaunotFiguruPozicijas()
                            self.atjaunotRezLapu()
                            self.beigtGajiensParbaude(roll, aktSpeletajs)
                        self.animetFiguruKustibu(aktSpeletajs, final_tile, dest, callback=pec_trepes)
                    else:
                        self.beigtGajiensParbaude(roll, aktSpeletajs)
                self.animetFiguruKustibu_parasto(aktSpeletajs, 120, final_tile, callback=pec_atleksanas)
            self.animetFiguruKustibu_parasto(aktSpeletajs, vecais, 120, callback=pec_120_sasniegsanas)
        else:
            def pec_parastas_kustibas():
                self.pievienotLogu(f"{aktSpeletajs['vards']} pārvietojas no {vecais}. uz {jauns}. plāksni!", aktSpeletajs["krasa"])
                if jauns in self.ladders:
                    dest = self.ladders[jauns]
                    def pec_trepites_kustibas():
                        self.pievienotLogu(f"{aktSpeletajs['vards']} uzkāpa uz trepītēm un nonāca uz {dest}. plāksni!", aktSpeletajs["krasa"])
                        aktSpeletajs["laukums"] = dest
                        self.atjaunotFiguruPozicijas()
                        self.atjaunotRezLapu()
                        self.beigtGajiensParbaude(roll, aktSpeletajs)
                    self.animetFiguruKustibu(aktSpeletajs, jauns, dest, callback=pec_trepites_kustibas)
                else:
                    aktSpeletajs["laukums"] = jauns
                    self.atjaunotFiguruPozicijas()
                    self.beigtGajiensParbaude(roll, aktSpeletajs)
            self.animetFiguruKustibu_parasto(aktSpeletajs, vecais, jauns, callback=pec_parastas_kustibas)

    def animetFiguruKustibu(self, speletajs, start_tile, end_tile, steps=15, callback=None):
        self._play_random_sound("Whoosh", 5)
        start_x, start_y = self.iegutFlizesCentru(start_tile)
        end_x, end_y = self.iegutFlizesCentru(end_tile)
        total_dx = end_x - start_x
        total_dy = end_y - start_y
        step_dx = total_dx / steps
        step_dy = total_dy / steps
        def animate_step(step):
            if step < steps:
                new_x = start_x + step_dx * (step + 1)
                new_y = start_y + step_dy * (step + 1)
                self.canvas.coords(speletajs["figura_id"], new_x, new_y)
                self.root.after(self.animation_delay, animate_step, step+1)
            else:
                self.canvas.coords(speletajs["figura_id"], end_x, end_y)
                if callback:
                    callback()
                self.atjaunotRezLapu()
        animate_step(0)

    def animetFiguruKustibu_parasto(self, speletajs, start_tile, end_tile, callback=None):
        self._play_random_sound("Whoosh", 5)
        if start_tile < end_tile:
            intermediate_tiles = list(range(start_tile + 1, end_tile + 1))
        else:
            intermediate_tiles = list(range(start_tile - 1, end_tile - 1, -1))
        def continue_movement(index, current_tile):
            if index >= len(intermediate_tiles):
                if callback:
                    callback()
                self.atjaunotRezLapu()
                return
            next_tile = intermediate_tiles[index]
            start_x, start_y = self.iegutFlizesCentru(current_tile)
            end_x, end_y = self.iegutFlizesCentru(next_tile)
            steps = self.animation_steps
            step_dx = (end_x - start_x) / steps
            step_dy = (end_y - start_y) / steps
            def animate_step(step):
                if step < steps:
                    new_x = start_x + step_dx * (step + 1)
                    new_y = start_y + step_dy * (step + 1)
                    self.canvas.coords(speletajs["figura_id"], new_x, new_y)
                    self.root.after(self.animation_delay, animate_step, step+1)
                else:
                    self.canvas.coords(speletajs["figura_id"], end_x, end_y)
                    continue_movement(index + 1, next_tile)
            animate_step(0)
        continue_movement(0, start_tile)

    def iegutFlizesCentru(self, tile):
        row = (tile - 1) // self.columns
        pos_in_row = (tile - 1) % self.columns
        col = pos_in_row if row % 2 == 0 else self.columns - 1 - pos_in_row
        x = col * self.tile_width + self.tile_width / 2
        y = self.board_height - (row * self.tile_height + self.tile_height / 2)
        return x, y

    def atjaunotFiguruPozicijas(self):
        pawns_by_tile = {}
        for speletajs in self.speletaji:
            tile = speletajs["laukums"]
            pawns_by_tile.setdefault(tile, []).append(speletajs)
        for tile, pawns in pawns_by_tile.items():
            center_x, center_y = self.iegutFlizesCentru(tile)
            if len(pawns) == 1:
                self.canvas.coords(pawns[0]["figura_id"], center_x, center_y)
            else:
                radius = min(self.tile_width, self.tile_height) * 0.3
                angle_step = 2 * math.pi / len(pawns)
                for index, speletajs in enumerate(pawns):
                    angle = index * angle_step
                    x = center_x + radius * math.cos(angle)
                    y = center_y + radius * math.sin(angle)
                    self.canvas.coords(speletajs["figura_id"], x, y)

    def atjaunotInfoEtiketi(self):
        if self.aktiviSpeletaji:
            aktSpeletajs = self.speletaji[self.aktiviSpeletaji[self.aktualaisIndekss]]
            info = f"Piešķirtā kārta: {aktSpeletajs['vards']}"
            self.info_label.config(text=info, fg=aktSpeletajs["krasa"], bd=2, relief="ridge", bg="silver", width=30)
            if not aktSpeletajs.get("human", True):
                self.root.after(1000, self.metKaulinu)
        else:
            self.info_label.config(text="Spēles beigas!", fg="black")
        self.atjaunotRezLapu()

    def atjaunotRezLapu(self):
        for i, speletajs in enumerate(self.speletaji):
            text = f"{speletajs['vards']}: Plāksne {speletajs['laukums']}"
            bg = "silver"
            if self.aktiviSpeletaji and i == self.aktiviSpeletaji[self.aktualaisIndekss]:
                bg = "floralwhite"
            try:
                self.score_labels[i].config(text=text, bg=bg)
            except Exception:
                pass

    def pievienotLogu(self, message, color=None):
        self.log_text.config(state="normal")
        tag = color if color else ""
        self.log_text.insert(tk.END, message + "\n", tag)
        self.log_text.config(state="disabled")
        self.log_text.see(tk.END)

    def beigtGajiensParbaude(self, roll, aktSpeletajs):
        if aktSpeletajs["laukums"] == 120:
            self.pievienotLogu(f"{aktSpeletajs['vards']} ir finišējis!", aktSpeletajs["krasa"])
            self.beiguKartiba.append(aktSpeletajs["vards"])
            del self.aktiviSpeletaji[self.aktualaisIndekss]
            if self.aktiviSpeletaji:
                self.aktualaisIndekss %= len(self.aktiviSpeletaji)
        else:
            if roll not in (6, 1):
                self.aktualaisIndekss = (self.aktualaisIndekss + 1) % len(self.aktiviSpeletaji)
            else:
                self.pievienotLogu(f"{aktSpeletajs['vards']} uzmet {roll} un tagad met atkal!", aktSpeletajs["krasa"])
        self.atjaunotInfoEtiketi()
        self.root.after(200, self.atiestatKaulinu)
        if len(self.aktiviSpeletaji) == 1:
            palicis = self.speletaji[self.aktiviSpeletaji[0]]
            self.beiguKartiba.append(palicis["vards"])
            self.aktiviSpeletaji.clear()
            self.beigtSpele()
        elif not self.aktiviSpeletaji:
            self.beigtSpele()

    def beigtSpele(self):
        self.play_sound("yay.wav")
        self.game_frame.pack_forget()
        if self.game_mode.get() == "regular":
            for speletajs in self.speletaji:
                if speletajs.get("human", True):
                    name = speletajs["vards"]
                    self.player_stats[name]["regular_games"] += 1
            if self.beiguKartiba:
                winner = self.beiguKartiba[0]
                for player in self.speletaji:
                    if player["vards"] == winner and player.get("human", True):
                        self.player_stats[winner]["regular_wins"] += 1
                        break
            placement_list = self.beiguKartiba
        else:
            for player in self.tournament_players:
                if player.get("human", True):
                    name = player["vards"]
                    self.player_stats[name]["tournament_games"] += 1
                if self.beiguKartiba:
                    winner = self.beiguKartiba[0]
                    for player in self.tournament_players:
                        if player["vards"] == winner and player.get("human", True):
                            self.player_stats[winner]["tournament_wins"] += 1
                            break
            if self.final_round_started and self.beiguKartiba:
                placement_list = self.beiguKartiba + self.tournament_nonfinalists_left + self.tournament_nonfinalists_right
            else:
                placement_list = self.tournament_winners + self.tournament_nonfinalists_left + self.tournament_nonfinalists_right

        self.save_stats()
        self.placement_frame = tk.Frame(self.root, bd=2, relief="ridge")
        self.placement_frame.pack(padx=20, pady=20, fill="both", expand=True)
        title_label = tk.Label(self.placement_frame, text="🎪 Spēles beigas! 🎪", font=("Helvetica", 18, "bold"))
        title_label.pack(pady=(20, 5))
        subtitle_label = tk.Label(self.placement_frame, text="Iegūtās vietas:", font=("Helvetica", 14))
        subtitle_label.pack(pady=(0, 20))
        positions_frame = tk.Frame(self.placement_frame)
        positions_frame.pack(pady=10, fill="both", expand=True)
        placement = 1
        for vards in placement_list:
            color = "black"
            players_list = self.speletaji if self.game_mode.get() == "regular" else self.tournament_players
            for player in players_list:
                if player["vards"] == vards:
                    color = player["krasa"]
                    break
            player_frame = tk.Frame(self.placement_frame, bd=2, relief="ridge", padx=10, pady=5)
            player_frame.pack(fill="x", padx=30, pady=5)
            medal = ""
            if placement == 1:
                medal = "🥇 "
            elif placement == 2:
                medal = "🥈 "
            elif placement == 3:
                medal = "🥉 "
            position_label = tk.Label(player_frame, text=f"{medal}{placement}. vieta:", font=("Helvetica", 14))
            position_label.pack(side=tk.LEFT, padx=(5, 10))
            name_label = tk.Label(player_frame, text=f"{vards}", font=("Helvetica", 14, "bold"), fg=color)
            name_label.pack(side=tk.LEFT)
            if self.game_mode.get() == "tournament":
                stat_text = ""
                for player in players_list:
                    if player["vards"] == vards:
                        if player.get("human", True):
                            stats = self.player_stats[vards]
                            stat_text = f"Spēles: {stats['tournament_games']}, Uzvaras: {stats['tournament_wins']}"
                        else:
                            stat_text = "Spēles: N/A, Uzvaras: N/A"
                        break
                stat_label = tk.Label(player_frame, text=stat_text, font=("Helvetica", 12))
                stat_label.pack(side=tk.RIGHT)
            placement += 1
        for col in range(5):
            self.placement_frame.grid_columnconfigure(col, weight=1)
        self.restart_button = tk.Button(self.placement_frame, text="Jauna spēle",
                                command=lambda: [self.play_sound("button.mp3"), self.restartetSpele()],
                                font=("Helvetica", 12), bg="#4CAF50", fg="white", padx=20, pady=10)
        self.restart_button.pack(pady=20)

    def restartetSpele(self):
        if self.placement_frame:
            self.placement_frame.destroy()
            self.placement_frame = None
        if self.game_frame:
            self.game_frame.destroy()
            self.game_frame = None
        if hasattr(self, 'tournament_frame') and self.tournament_frame:
            self.tournament_frame.destroy()
            self.tournament_frame = None
        self.root.geometry("")
        self.in_game = False 
        self.setup_frame.pack(padx=10, pady=10)
        self.dice_on_cooldown = False

    def atiestatKaulinu(self):
        self.dice_on_cooldown = False

    def _play_random_sound(self, prefix, count):
        self.play_sound(f"{prefix}{random.randint(1, count)}.wav")

    # ------------------- Turnīra režīma Metodes -------------------

    def createTournamentBoard(self, players, parent_frame, board_side):
        board = {}
        board["players"] = players
        board["active"] = list(range(len(players)))
        board["current"] = 0
        board["finished_order"] = []
        board["finished_recorded"] = False
        board["canvas"] = tk.Canvas(parent_frame, width=400, height=400)
        board["canvas"].pack(padx=5, pady=5)
        board["board_width"] = 400
        board["board_height"] = 400
        board["columns"] = 10
        board["rows"] = 12
        board["tile_width"] = board["board_width"] / board["columns"]
        board["tile_height"] = board["board_height"] / board["rows"]
        board_image = ImageTk.PhotoImage(Image.open("circus_board.png").resize((400,400)))
        board["canvas"].create_image(0, 0, anchor="nw", image=board_image)
        board["board_image"] = board_image
        board["info_label"] = tk.Label(parent_frame, text="", font=("Helvetica", 12, "bold"))
        board["info_label"].pack()
        init_val = random.randint(1,6)
        board["dice_photo"] = self.metKaulinAtteli(init_val)
        board["dice_label"] = tk.Label(parent_frame, image=board["dice_photo"])
        board["dice_label"].pack(padx=5, pady=5)
        board["dice_label"].bind("<Button-1>", lambda e, b=board: self.tournamentDiceThrow(b, e))
        board["log_text"] = tk.Text(parent_frame, height=5, width=60, state="disabled", font=("Helvetica", 10))
        board["log_text"].pack(pady=5)
        for c in ["indianred", "blue", "green", "gold", "purple", "cyan", "orange", "pink"]:
            board["log_text"].tag_config(c, foreground=c)
        board["score_frame"] = tk.Frame(parent_frame)
        board["score_frame"].pack(pady=5)
        board["score_labels"] = []
        for player in players:
            lbl = tk.Label(board["score_frame"], text=f"{player['vards']}: Plāksne {player['laukums']}",
                        fg=player["krasa"], font=("Helvetica", 12), bd=2, relief="ridge", width=20)
            lbl.pack(anchor="w", pady=2)
            board["score_labels"].append(lbl)
        
        board["pawn_images"] = []
        for player in players:
            pawn_image = self.spelKaulinAtteli_tournament(player["krasa"], board)
            token = board["canvas"].create_image(0, 0, image=pawn_image)
            player["figura_id"] = token
            player["pawn_image"] = pawn_image
            board["pawn_images"].append(pawn_image)
        self.tournamentUpdatePositions(board)
        self.tournamentUpdateInfo(board)
        self.tournamentUpdateScores(board)
        board["animating"] = False
        board["dice_on_cooldown"] = False
        board["animation_delay"] = 30
        board["animation_steps"] = 8
        return board

    def tournamentDiceThrow(self, board, event=None):
        if not board["active"]:
            return
        current_index = board["active"][board["current"]]
        player = board["players"][current_index]
        if event is not None and not player.get("human", True):
            return
        if board["animating"] or not board["active"] or board["dice_on_cooldown"]:
            return
        board["dice_on_cooldown"] = True
        board["animating"] = True
        self.tournamentAnimateDice(board, 0)
        self._play_random_sound("diceThrow", 4)

    def tournamentAnimateDice(self, board, cycle):
        dice_value = random.randint(1,6)
        board["dice_photo"] = self.metKaulinAtteli(dice_value)
        board["dice_label"].config(image=board["dice_photo"])
        board["info_label"].config(text=f"Metamais kauliņš: {dice_value}")
        if cycle < 10:
            self.root.after(80, self.tournamentAnimateDice, board, cycle+1)
        else:
            self.tournamentProcessDice(board, dice_value)
            board["animating"] = False

    def tournamentProcessDice(self, board, roll):
        current_index = board["active"][board["current"]]
        player = board["players"][current_index]
        prev_tile = player["laukums"]
        new_tile = prev_tile + roll
        if new_tile > 120:
            extra = new_tile - 120
            final_tile = 120 if (extra % 2 == 0) else 119
            def after_bounce():
                player["laukums"] = final_tile
                self.tournamentUpdatePositions(board)
                self.tournamentLog(board, f"{player['vards']} pārvietojas uz {final_tile}. plāksni!", player["krasa"])
                if final_tile in self.ladders:
                    dest = self.ladders[final_tile]
                    def after_ladder():
                        player["laukums"] = dest
                        self.tournamentUpdatePositions(board)
                        self.tournamentLog(board, f"{player['vards']} uzkāpa uz trepītēm un nonāca uz {dest}. plāknsi!", player["krasa"])
                        self.tournamentEndTurn(board, roll)
                    self.tournamentAnimateLadder(board, player, final_tile, dest, callback=after_ladder)
                else:
                    self.tournamentEndTurn(board, roll)
            self.tournamentAnimateMovement(board, player, prev_tile, 120,
                callback=lambda: self.tournamentAnimateMovement(board, player, 120, final_tile, callback=after_bounce))
        else:
            def after_move():
                player["laukums"] = new_tile
                self.tournamentUpdatePositions(board)
                self.tournamentLog(board, f"{player['vards']} pārvietojas no {prev_tile}. uz {new_tile}. plāksni!", player["krasa"])
                if new_tile in self.ladders:
                    dest = self.ladders[new_tile]
                    def after_ladder():
                        player["laukums"] = dest
                        self.tournamentUpdatePositions(board)
                        self.tournamentLog(board, f"{player['vards']} uzkāpa uz trepītēm un nonāca uz {dest}. plāksni!", player["krasa"])
                        self.tournamentEndTurn(board, roll)
                    self.tournamentAnimateLadder(board, player, new_tile, dest, callback=after_ladder)
                else:
                    self.tournamentEndTurn(board, roll)
            self.tournamentAnimateMovement(board, player, prev_tile, new_tile, callback=after_move)

    def tournamentAnimateMovement(self, board, player, start_tile, end_tile, callback=None):
        if start_tile < end_tile:
            intermediate_tiles = list(range(start_tile + 1, end_tile + 1))
        else:
            intermediate_tiles = list(range(start_tile - 1, end_tile - 1, -1))
        def continue_movement(index, current_tile):
            if index >= len(intermediate_tiles):
                if callback: callback()
                try:
                    self.tournamentUpdateScores(board)
                except Exception:
                    pass
                return
            next_tile = intermediate_tiles[index]
            start_x, start_y = self.tournamentGetTileCenter(board, current_tile)
            end_x, end_y = self.tournamentGetTileCenter(board, next_tile)
            steps = board["animation_steps"]
            dx = (end_x - start_x) / steps
            dy = (end_y - start_y) / steps
            def animate_step(step):
                if step < steps:
                    board["canvas"].move(player["figura_id"], round(dx), round(dy))
                    self.root.after(board["animation_delay"], animate_step, step+1)
                else:
                    board["canvas"].coords(player["figura_id"], end_x, end_y)
                    continue_movement(index + 1, next_tile)
            animate_step(0)
        continue_movement(0, start_tile)

    def tournamentAnimateLadder(self, board, player, start_tile, end_tile, steps=15, callback=None):
        self._play_random_sound("Whoosh", 5)
        start_x, start_y = self.tournamentGetTileCenter(board, start_tile)
        end_x, end_y = self.tournamentGetTileCenter(board, end_tile)
        dx = (end_x - start_x) / steps
        dy = (end_y - start_y) / steps
        def animate_step(step):
            if step < steps:
                board["canvas"].move(player["figura_id"], round(dx), round(dy))
                self.root.after(board["animation_delay"], animate_step, step+1)
            else:
                board["canvas"].coords(player["figura_id"], end_x, end_y)
                if callback:
                    callback()
                try:
                    self.tournamentUpdateScores(board)
                except Exception:
                    pass
        animate_step(0)

    def tournamentGetTileCenter(self, board, tile):
        row = (tile - 1) // board["columns"]
        pos_in_row = (tile - 1) % board["columns"]
        col = pos_in_row if row % 2 == 0 else board["columns"] - 1 - pos_in_row
        x = col * board["tile_width"] + board["tile_width"] / 2
        y = board["board_height"] - (row * board["tile_height"] + board["tile_height"] / 2)
        return x, y

    def tournamentUpdatePositions(self, board):
        positions = {}
        for player in board["players"]:
            tile = player["laukums"]
            positions.setdefault(tile, []).append(player)
        for tile, players in positions.items():
            center_x, center_y = self.tournamentGetTileCenter(board, tile)
            if len(players) == 1:
                board["canvas"].coords(players[0]["figura_id"], center_x, center_y)
            else:
                radius = min(board["tile_width"], board["tile_height"]) * 0.3
                angle_step = 2 * math.pi / len(players)
                for index, player in enumerate(players):
                    angle = index * angle_step
                    x = center_x + radius * math.cos(angle)
                    y = center_y + radius * math.sin(angle)
                    board["canvas"].coords(player["figura_id"], x, y)

    def tournamentUpdateInfo(self, board):
        if board["active"]:
            current_index = board["active"][board["current"]]
            player = board["players"][current_index]
            board["info_label"].config(text=f"Piešķirtā kārta: {player['vards']}", fg=player["krasa"])
            if not player.get("human", True):
                self.root.after(1000, lambda: self.tournamentDiceThrow(board))
        else:
            board["info_label"].config(text="Spēles beigas!", fg="black")

    def tournamentUpdateScores(self, board):
        for i, player in enumerate(board["players"]):
            text = f"{player['vards']}: Plāksne {player['laukums']}"
            bg = "silver"
            if board["active"] and i == board["active"][board["current"]]:
                bg = "floralwhite"
            try:
                board["score_labels"][i].config(text=text, bg=bg)
            except Exception:
                pass

    def tournamentLog(self, board, message, color=None):
        board["log_text"].config(state="normal")
        tag = color if color else ""
        board["log_text"].insert(tk.END, message + "\n", tag)
        board["log_text"].config(state="disabled")
        board["log_text"].see(tk.END)

    def tournamentEndTurn(self, board, roll):
        current_index = board["active"][board["current"]]
        player = board["players"][current_index]
        if player["laukums"] >= 120:
            self.tournamentLog(board, f"{player['vards']} finišējis!", player["krasa"])
            board["finished_order"].append(player["vards"])
            if len(board["finished_order"]) == 2:
                board["active"] = []
            else:
                board["active"].remove(board["active"][board["current"]])
                if board["active"]:
                    board["current"] %= len(board["active"])
        else:
            if roll not in (6, 1):
                board["current"] = (board["current"] + 1) % len(board["active"])
            else:
                self.tournamentLog(board, f"{player['vards']} uzmet {roll} un met atkal!", player["krasa"])
        self.tournamentUpdateInfo(board)
        board["dice_on_cooldown"] = False

        if not board["active"]:
            if not board.get("finished_recorded"):
                finished_names = board["finished_order"][:]
                for p in board["players"]:
                    if p["vards"] not in finished_names:
                        board["finished_order"].append(p["vards"])
                board["finished_recorded"] = True
                winners = board["finished_order"][:2]
                losers = board["finished_order"][2:]
                board["winners"] = winners
                board["losers"] = losers
                self.tournamentLog(board, 
                    f"Spēle noslēgusies.\nFinālisti: {', '.join(winners)};\nDiskvalificētie: {', '.join(losers)}",
                    "black")
                for winner in winners:
                    self.tournament_winners.append(winner)
                if board == self.left_board:
                    self.tournament_nonfinalists_left = losers
                elif board == self.right_board:
                    self.tournament_nonfinalists_right = losers

            if self.left_board and self.right_board and not self.final_round_started:
                if not self.left_board["active"] and not self.right_board["active"]:
                    self.startFinalRound_tournament()
    # --------------------------------------------------------------------

    def startFinalRound_tournament(self):
        self.final_round_started = True
        final_players = []
        for winner_name in self.tournament_winners:
            for player in self.tournament_players:
                if player["vards"] == winner_name:
                    final_players.append(player)
                    break
        for player in final_players:
            player["laukums"] = 1
            player["beidzis"] = False
        self.tournament_frame.destroy()
        self.setup_frame.pack_forget()
        self.game_frame = tk.Frame(self.root)
        self.game_frame.pack(padx=10, pady=10)

        self.canvas = tk.Canvas(self.game_frame, width=self.board_width, height=self.board_height)
        self.canvas.grid(row=0, column=0, rowspan=6, padx=5, pady=5)
        self.board_image = ImageTk.PhotoImage(self.open_board_image("circus_board.png", self.board_width, self.board_height))
        self.canvas.create_image(0, 0, anchor="nw", image=self.board_image)

        self.info_label = tk.Label(self.game_frame, text="", font=("Helvetica", 14))
        self.info_label.grid(row=0, column=1, sticky="nw")

        dice_frame = tk.Frame(self.game_frame)
        dice_frame.grid(row=1, column=1, columnspan=2, sticky="w")

        self.dice_text_label = tk.Label(dice_frame, text="Metamais kauliņš: ", font=("Helvetica", 12))
        self.dice_text_label.pack(side="left", padx=(0, 60))

        init_val = random.randint(1, 6)
        self.dice_photo = self.metKaulinAtteli(init_val)
        self.dice_image_label = tk.Label(dice_frame, image=self.dice_photo)
        self.dice_image_label.pack(side="left")

        self.message_label = tk.Label(self.game_frame, text="", justify="left", font=("Helvetica", 12))
        self.message_label.grid(row=2, column=1, sticky="nw")

        self.iesatijumi_game_btn = tk.Button(
            self.game_frame,
            text="⚙️ Iestatījumi",
            command=lambda: [self.play_sound("button.mp3"), self.show_iesatijumi(mode="game")],
            font=("Helvetica", 12, "bold"),
            bg="#337ab7",
            fg="white"
        )
        self.iesatijumi_game_btn.grid(row=3, column=1, sticky="nw", padx=5)

        self.score_frame = tk.Frame(self.game_frame)
        self.score_frame.grid(row=4, column=1, sticky="nw", pady=10)
        self.score_labels = []
        for player in final_players:
            lbl = tk.Label(
                self.score_frame,
                text=f"{player['vards']}: Plāksne {player['laukums']}",
                fg=player["krasa"],
                font=("Helvetica", 12),
                bd=2,
                relief="ridge",
                width=30
            )
            lbl.pack(anchor="w", pady=2)
            self.score_labels.append(lbl)

        self.log_text = tk.Text(self.game_frame, height=10, width=45, state="disabled", font=("Helvetica", 10))
        self.log_text.grid(row=5, column=1, columnspan=2, sticky="nw", pady=5)
        for c in ["indianred", "blue", "green", "gold", "purple", "cyan", "orange", "pink"]:
            self.log_text.tag_config(c, foreground=c)

        self.speletaji = final_players
        self.aktiviSpeletaji = list(range(len(self.speletaji)))
        self.aktualaisIndekss = 0
        self.beiguKartiba = []

        self.pawn_images = []
        for player in self.speletaji:
            pawn_image = self.spelKaulinAtteli(player["krasa"])
            token = self.canvas.create_image(0, 0, image=pawn_image)
            player["figura_id"] = token
            player["pawn_image"] = pawn_image
            self.pawn_images.append(pawn_image)

        self.atjaunotFiguruPozicijas()
        self.atjaunotInfoEtiketi()
        self.tournament_placement = self.beiguKartiba + self.tournament_nonfinalists_left + self.tournament_nonfinalists_right
        self.atjaunotRezLapu()

    def open_board_image(self, path, width, height):
        from PIL import Image
        img = Image.open(path)
        return img.resize((width, height))
