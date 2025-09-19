from basemmu import BaseMMU

class LruMMU(BaseMMU):
    
    def __init__(self, frames):
        super().__init__(frames)
        self.access_order = []  # track access order
        
    def select_victim_frame(self):
        # Find least recently used page
        lru_page = None
        lru_time = float('inf')
        
        for page_number in self.page_table:
            if page_number in self.access_order:
                page_time = self.access_order.index(page_number)
                if page_time < lru_time:
                    lru_time = page_time
                    lru_page = page_number
                    
        if lru_page is None:
            lru_page = next(iter(self.page_table))
            
        return self.page_table[lru_page]
        
    def update_access_info(self, page_number, is_write):
        if page_number in self.access_order:
            self.access_order.remove(page_number)
        self.access_order.append(page_number)
        
        # clean up old entries
        pages_in_memory = set(self.page_table.keys())
        self.access_order = [page for page in self.access_order if page in pages_in_memory]
        
    def load_page(self, page_number, frame_number):
        super().load_page(page_number, frame_number)
        self.update_access_info(page_number, False)
        
    def evict_page(self, frame_number):
        frame_info = self.frame_table[frame_number]
        page_number = frame_info['page_number']
        
        if page_number in self.access_order:
            self.access_order.remove(page_number)
            
        return super().evict_page(frame_number)