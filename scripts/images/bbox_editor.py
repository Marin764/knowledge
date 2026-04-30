import os
import json
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

# Find the project root
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..'))
METADATA_DIR = os.path.join(PROJECT_ROOT, "assets", "star_rail_controls", "metadata", "screens")

class BBoxEditor(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Game UI Bounding Box Editor")
        self.geometry("1400x900")

        self.manifest_files = []
        self.current_manifest_path = None
        self.current_manifest_data = None
        self.current_image = None
        self.current_photo = None
        self.canvas_image_id = None
        
        self.rects = [] # list of dicts: {'control': dict, 'rect_id': int, 'text_id': int, 'bg_id': int}
        self.selected_rect = None
        self.drag_mode = None # 'move', 'resize_l', 'resize_r', 'resize_t', 'resize_b', 'resize_tl', 'resize_tr', 'resize_bl', 'resize_br'
        self.start_x = 0
        self.start_y = 0
        self.start_bbox = []

        self.setup_ui()
        self.load_file_list()

    def setup_ui(self):
        # Top Toolbar
        toolbar = ttk.Frame(self)
        toolbar.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        
        ttk.Button(toolbar, text="Save (Ctrl+S)", command=self.save_manifest).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text="Prev", command=self.prev_file).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text="Next", command=self.next_file).pack(side=tk.LEFT, padx=5)
        
        self.status_var = tk.StringVar(value="Ready")
        ttk.Label(toolbar, textvariable=self.status_var).pack(side=tk.RIGHT, padx=10)

        # Main PanedWindow
        paned = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True)

        # Left Listbox
        list_frame = ttk.Frame(paned)
        paned.add(list_frame, weight=1)
        
        self.listbox = tk.Listbox(list_frame)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar = ttk.Scrollbar(list_frame, command=self.listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.config(yscrollcommand=scrollbar.set)
        self.listbox.bind('<<ListboxSelect>>', self.on_select_file)

        # Right Canvas
        canvas_frame = ttk.Frame(paned)
        paned.add(canvas_frame, weight=5)
        
        self.canvas = tk.Canvas(canvas_frame, bg="#2d2d2d", cursor="crosshair")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        v_scroll = ttk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        h_scroll = ttk.Scrollbar(canvas_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        h_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)
        
        self.canvas.bind("<ButtonPress-1>", self.on_mouse_down)
        self.canvas.bind("<B1-Motion>", self.on_mouse_move)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_up)
        
        self.bind("<Control-s>", lambda e: self.save_manifest())

    def load_file_list(self):
        self.listbox.delete(0, tk.END)
        if os.path.exists(METADATA_DIR):
            files = [f for f in os.listdir(METADATA_DIR) if f.endswith('.json')]
            files.sort()
            self.manifest_files = files
            for f in files:
                self.listbox.insert(tk.END, f)
        else:
            self.status_var.set(f"Directory not found: {METADATA_DIR}")

    def on_select_file(self, event):
        selection = self.listbox.curselection()
        if not selection:
            return
        idx = selection[0]
        filename = self.manifest_files[idx]
        self.open_manifest(os.path.join(METADATA_DIR, filename))

    def open_manifest(self, filepath):
        self.current_manifest_path = filepath
        with open(filepath, 'r', encoding='utf-8') as f:
            self.current_manifest_data = json.load(f)
            
        source_rel = self.current_manifest_data.get('source', '')
        source_abs = os.path.abspath(os.path.join(PROJECT_ROOT, source_rel))
        
        if not os.path.exists(source_abs):
            messagebox.showerror("Error", f"Image not found: {source_abs}")
            return
            
        self.current_image = Image.open(source_abs)
        self.current_photo = ImageTk.PhotoImage(self.current_image)
        
        self.canvas.delete("all")
        self.canvas_image_id = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.current_photo)
        self.canvas.config(scrollregion=(0, 0, self.current_image.width, self.current_image.height))
        
        self.rects = []
        self.selected_rect = None
        
        for control in self.current_manifest_data.get('controls', []):
            bbox = control.get('bbox', [0,0,0,0])
            self.draw_control(control, bbox)
            
        self.status_var.set(f"Loaded: {os.path.basename(filepath)}")

    def draw_control(self, control, bbox):
        x, y, w, h = bbox
        
        # Draw background for text
        bg_id = self.canvas.create_rectangle(x, max(0, y-20), x+150, y, fill="black", outline="")
        
        # Draw rect
        rect_id = self.canvas.create_rectangle(x, y, x+w, y+h, outline="yellow", width=2)
        
        # Draw text
        text_id = self.canvas.create_text(x+5, max(0, y-10), text=control.get('control_id', ''), fill="white", anchor=tk.W)
        
        self.rects.append({
            'control': control,
            'rect_id': rect_id,
            'bg_id': bg_id,
            'text_id': text_id
        })

    def get_hit_target(self, x, y):
        TOLERANCE = 8
        # Iterate in reverse to hit top-most items first
        for i in range(len(self.rects)-1, -1, -1):
            r = self.rects[i]
            bbox = r['control']['bbox']
            bx, by, bw, bh = bbox
            
            # Check corners
            if abs(x - bx) < TOLERANCE and abs(y - by) < TOLERANCE: return r, 'resize_tl'
            if abs(x - (bx+bw)) < TOLERANCE and abs(y - by) < TOLERANCE: return r, 'resize_tr'
            if abs(x - bx) < TOLERANCE and abs(y - (by+bh)) < TOLERANCE: return r, 'resize_bl'
            if abs(x - (bx+bw)) < TOLERANCE and abs(y - (by+bh)) < TOLERANCE: return r, 'resize_br'
            
            # Check edges
            if abs(x - bx) < TOLERANCE and by <= y <= by+bh: return r, 'resize_l'
            if abs(x - (bx+bw)) < TOLERANCE and by <= y <= by+bh: return r, 'resize_r'
            if abs(y - by) < TOLERANCE and bx <= x <= bx+bw: return r, 'resize_t'
            if abs(y - (by+bh)) < TOLERANCE and bx <= x <= bx+bw: return r, 'resize_b'
            
            # Check inside
            if bx <= x <= bx+bw and by <= y <= by+bh:
                return r, 'move'
                
        return None, None

    def on_mouse_down(self, event):
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        
        target, mode = self.get_hit_target(x, y)
        
        if self.selected_rect:
            self.canvas.itemconfig(self.selected_rect['rect_id'], outline="yellow", width=2)
            
        self.selected_rect = target
        self.drag_mode = mode
        
        if target:
            self.canvas.itemconfig(target['rect_id'], outline="red", width=3)
            self.start_x = x
            self.start_y = y
            self.start_bbox = list(target['control']['bbox'])
            self.status_var.set(f"Selected: {target['control']['control_id']} | Mode: {mode}")

    def on_mouse_move(self, event):
        if not self.selected_rect or not self.drag_mode:
            return
            
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        
        dx = x - self.start_x
        dy = y - self.start_y
        
        bx, by, bw, bh = self.start_bbox
        
        if self.drag_mode == 'move':
            bx += dx
            by += dy
        elif self.drag_mode == 'resize_l':
            bx += dx
            bw -= dx
        elif self.drag_mode == 'resize_r':
            bw += dx
        elif self.drag_mode == 'resize_t':
            by += dy
            bh -= dy
        elif self.drag_mode == 'resize_b':
            bh += dy
        elif self.drag_mode == 'resize_tl':
            bx += dx
            by += dy
            bw -= dx
            bh -= dy
        elif self.drag_mode == 'resize_tr':
            by += dy
            bw += dx
            bh -= dy
        elif self.drag_mode == 'resize_bl':
            bx += dx
            bw -= dx
            bh += dy
        elif self.drag_mode == 'resize_br':
            bw += dx
            bh += dy
            
        # Ensure minimum size
        if bw < 5: bw = 5
        if bh < 5: bh = 5
        
        self.selected_rect['control']['bbox'] = [int(bx), int(by), int(bw), int(bh)]
        self.update_rect_visual(self.selected_rect)

    def on_mouse_up(self, event):
        self.drag_mode = None

    def update_rect_visual(self, rect_obj):
        x, y, w, h = rect_obj['control']['bbox']
        self.canvas.coords(rect_obj['rect_id'], x, y, x+w, y+h)
        self.canvas.coords(rect_obj['bg_id'], x, max(0, y-20), x+150, y)
        self.canvas.coords(rect_obj['text_id'], x+5, max(0, y-10))

    def save_manifest(self):
        if not self.current_manifest_path or not self.current_manifest_data:
            return
            
        with open(self.current_manifest_path, 'w', encoding='utf-8') as f:
            json.dump(self.current_manifest_data, f, ensure_ascii=False, indent=2)
            
        self.status_var.set(f"Saved: {os.path.basename(self.current_manifest_path)}")
        # Flash border green
        if self.selected_rect:
            self.canvas.itemconfig(self.selected_rect['rect_id'], outline="green")
            self.after(500, lambda: self.canvas.itemconfig(self.selected_rect['rect_id'], outline="red"))

    def next_file(self):
        selection = self.listbox.curselection()
        if selection:
            idx = selection[0]
            if idx < self.listbox.size() - 1:
                self.listbox.selection_clear(0, tk.END)
                self.listbox.selection_set(idx + 1)
                self.listbox.see(idx + 1)
                self.on_select_file(None)

    def prev_file(self):
        selection = self.listbox.curselection()
        if selection:
            idx = selection[0]
            if idx > 0:
                self.listbox.selection_clear(0, tk.END)
                self.listbox.selection_set(idx - 1)
                self.listbox.see(idx - 1)
                self.on_select_file(None)

if __name__ == "__main__":
    app = BBoxEditor()
    app.mainloop()
