from basemmu import BaseMMU

class ClockMMU(BaseMMU):
    
    def __init__(self, frames):
        super().__init__(frames)
        self.clock_hand = 0
        self.reference_bits = [False] * frames
        
    def select_victim_frame(self):
        # Clock algorithm
        while True:
            if self.clock_hand in self.frame_table:
                if self.reference_bits[self.clock_hand]:
                    self.reference_bits[self.clock_hand] = False
                else:
                    victim_frame = self.clock_hand
                    self.clock_hand = (self.clock_hand + 1) % self.frames
                    return victim_frame
                    
            self.clock_hand = (self.clock_hand + 1) % self.frames
                
    def update_access_info(self, page_number, is_write):
        if page_number in self.page_table:
            frame_number = self.page_table[page_number]
            self.reference_bits[frame_number] = True
            
    def load_page(self, page_number, frame_number):
        super().load_page(page_number, frame_number)
        self.reference_bits[frame_number] = True
        
    def evict_page(self, frame_number):
        self.reference_bits[frame_number] = False
        return super().evict_page(frame_number)