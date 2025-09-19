import random
from basemmu import BaseMMU

class RandMMU(BaseMMU):
    
    def __init__(self, frames):
        super().__init__(frames)
        
    def select_victim_frame(self):
        used_frames = list(self.frame_table.keys())
        return random.choice(used_frames)
        
    def update_access_info(self, page_number, is_write):
        # Random doesn't need to track anything
        pass