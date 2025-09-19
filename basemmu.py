from abc import ABC, abstractmethod

class BaseMMU(ABC):
    
    def __init__(self, frames):
        self.frames = frames
        self.page_table = {}  # page -> frame mapping
        self.frame_table = {}  # frame -> page info
        self.free_frames = list(range(frames))
        
        self.total_page_faults = 0
        self.total_disk_reads = 0
        self.total_disk_writes = 0
        self.debug_mode = False
        
    def set_debug(self):
        self.debug_mode = True
        
    def reset_debug(self):
        self.debug_mode = False
        
    def get_total_page_faults(self):
        return self.total_page_faults
        
    def get_total_disk_reads(self):
        return self.total_disk_reads
        
    def get_total_disk_writes(self):
        return self.total_disk_writes
        
    def is_page_in_memory(self, page_number):
        return page_number in self.page_table
        
    def debug_print(self, message):
        if self.debug_mode:
            print(message)
            
    def load_page(self, page_number, frame_number):
        self.page_table[page_number] = frame_number
        self.frame_table[frame_number] = {
            'page_number': page_number,
            'dirty_bit': False
        }
        self.total_disk_reads += 1
        self.debug_print(f"  reading page {page_number:x} from disk")
        
    def evict_page(self, frame_number):
        frame_info = self.frame_table[frame_number]
        page_number = frame_info['page_number']
        
        if frame_info['dirty_bit']:
            self.total_disk_writes += 1
            self.debug_print(f"  writing page {page_number:x} to disk")
            
        self.debug_print(f"  evicting page {page_number:x}")
        
        del self.page_table[page_number]
        del self.frame_table[frame_number]
        
        return page_number
        
    def set_dirty_bit(self, page_number):
        if page_number in self.page_table:
            frame_number = self.page_table[page_number]
            self.frame_table[frame_number]['dirty_bit'] = True
            
    def handle_page_fault(self, page_number):
        self.total_page_faults += 1
        self.debug_print(f"  page fault on {page_number:x}")
        
        if self.free_frames:
            frame_number = self.free_frames.pop(0)
            self.load_page(page_number, frame_number)
        else:
            frame_to_evict = self.select_victim_frame()
            self.evict_page(frame_to_evict)
            self.load_page(page_number, frame_to_evict)
            
    @abstractmethod
    def select_victim_frame(self):
        pass
        
    @abstractmethod
    def update_access_info(self, page_number, is_write):
        pass
        
    def read_memory(self, page_number):
        self.debug_print(f"reading from {page_number:x}")
        
        if not self.is_page_in_memory(page_number):
            self.handle_page_fault(page_number)
            
        self.update_access_info(page_number, False)
        
    def write_memory(self, page_number):
        self.debug_print(f"writing to {page_number:x}")
        
        if not self.is_page_in_memory(page_number):
            self.handle_page_fault(page_number)
            
        self.set_dirty_bit(page_number)
        self.update_access_info(page_number, True)