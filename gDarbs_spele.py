# gDarbs_spele.py
import tkinter as tk
from spele_gui import SpeleGUI
from spele_metodes import SpeleMetodes

class CirksSpele(SpeleGUI, SpeleMetodes):
    def __init__(self, root):
        # Initialize GUI and game logic components.
        SpeleGUI.__init__(self, root)
        SpeleMetodes.__init__(self)
        self.load_stats()
        
        self.speletaji = []          # Regular mode players list.
        self.aktiviSpeletaji = []    # Indices for active players.
        self.aktualaisIndekss = 0     # Current player index.
        self.beiguKartiba = []       # Finishing order.
        self.figuruKrasas = ["indianred", "blue", "green", "gold"]
        self.ladders = { 
            9: 11, 14: 30, 34: 97, 36: 45, 40: 58,
            52: 68, 59: 80, 65: 83, 72: 94, 92: 108, 96: 116,
            16: 1, 19: 3, 25: 7, 50: 32, 53: 8,
            63: 57, 71: 51, 87: 67, 102: 81, 107: 23, 112: 90,
            117: 98, 119: 101
        }
        self.columns = 10
        self.rows = 12
        self.board_width = 764
        self.board_height = 764
        self.tile_width = self.board_width / self.columns
        self.tile_height = self.board_height / self.rows
        self.animating = False
        self.dice_on_cooldown = False
        self.animation_delay = 30
        self.animation_steps = 8
        
        self.tournament_players = []      
        self.left_board = None
        self.right_board = None
        self.tournament_winners = []      
        self.tournament_nonfinalists_left = []   
        self.tournament_nonfinalists_right = []  
        self.tournament_placement = []    
        self.final_round_started = False

if __name__ == "__main__":
    root = tk.Tk()
    root.resizable(False, False)
    game = CirksSpele(root)
    root.mainloop()
