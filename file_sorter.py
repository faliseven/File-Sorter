import os
import shutil
import threading
import time
import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image

CATEGORIES = {
    'JPEG Images': ['.jpg', '.jpeg'],
    'PNG Images': ['.png'],
    'GIF Images': ['.gif'],
    'Bitmap Images': ['.bmp'],
    'SVG Images': ['.svg'],
    'WebP Images': ['.webp'],
    'TIFF Images': ['.tiff', '.tif'],
    'ICO Icons': ['.ico'],
    'HEIC Images': ['.heic'],
    'RAW Images': ['.raw', '.cr2', '.nef', '.orf', '.sr2', '.arw', '.dng', '.rw2', '.pef', '.srw'],
    'EXR Images': ['.exr'],
    'DDS Images': ['.dds'],
    'TGA Images': ['.tga'],
    'Screenshots': ['screenshot', 'screen', 'snip', '.snagit'],
    'Wallpapers': ['wallpaper', 'фон', 'background'],
    'Icons': ['.icns', '.icon'],
    'ZIP Archives': ['.zip'],
    'RAR Archives': ['.rar'],
    '7z Archives': ['.7z'],
    'TAR Archives': ['.tar'],
    'GZ Archives': ['.gz'],
    'BZ2 Archives': ['.bz2'],
    'XZ Archives': ['.xz'],
    'ISO Images': ['.iso'],
    'CAB Archives': ['.cab'],
    'ARJ Archives': ['.arj'],
    'LZ Archives': ['.lz'],
    'ACE Archives': ['.ace'],
    'SIT Archives': ['.sit'],
    'JAR Archives': ['.jar'],
    'APK Packages': ['.apk'],
    'DMG Images': ['.dmg'],
    'Split Archives': ['.001', '.002', '.003'],
    'ALZ Archives': ['.alz'],
    'ARC Archives': ['.arc'],
    'CBR Comics': ['.cbr'],
    'CBZ Comics': ['.cbz'],
    'LHA Archives': ['.lha'],
    'LZH Archives': ['.lzh'],
    'PAK Archives': ['.pak'],
    'PART Files': ['.part'],
    'Windows Executables': ['.exe'],
    'MSI Installers': ['.msi'],
    'Batch Files': ['.bat'],
    'Shell Scripts': ['.sh'],
    'Android Packages': ['.apk'],
    'COM Executables': ['.com'],
    'Java Archives': ['.jar'],
    'WSF Scripts': ['.wsf'],
    'Mac DMG': ['.dmg'],
    'PKG Installers': ['.pkg'],
    'Mac Apps': ['.app'],
    'Binary Files': ['.bin'],
    'Command Files': ['.command'],
    'Gadget Files': ['.gadget'],
    'VBS Scripts': ['.vbs'],
    'PowerShell Scripts': ['.ps1', '.psm1'],
    'Screensavers': ['.scr'],
    'MSU Updates': ['.msu'],
    'Registry Files': ['.reg'],
    'CMD Scripts': ['.cmd'],
    'DLLs': ['.dll'],
    'Drivers': ['.sys', '.inf', '.cat', '.drv'],
    'VMware Images': ['.vmdk'],
    'VirtualBox Images': ['.vdi'],
    'Hyper-V Images': ['.vhd', '.vhdx'],
    'OVA/OVF': ['.ova', '.ovf'],
    'QEMU Images': ['.qcow2'],
    'VM IMG': ['.img'],
    'VM Configs': ['.vmx', '.nvram', '.vmxf', '.vmsd', '.vbox', '.vbox-prev'],
    'Visual Studio Solutions': ['.sln'],
    'C# Projects': ['.csproj'],
    'C++ Projects': ['.vcxproj'],
    'Xcode Projects': ['.xcodeproj', '.xcworkspace'],
    'Sublime Projects': ['.sublime-project'],
    'JetBrains Projects': ['.idea', '.iml', '.ipr', '.iws'],
    'Other IDE Projects': ['.workspace'],
    'Makefiles': ['Makefile', '.make'],
    'CMake': ['CMakeLists.txt', '.cmake'],
    'Gradle': ['build.gradle'],
    'Maven': ['pom.xml'],
    'Gulp': ['gulpfile.js'],
    'Grunt': ['Gruntfile.js'],
    'PDF': ['.pdf'],
    'Word': ['.doc', '.docx'],
    'Excel': ['.xls', '.xlsx'],
    'PowerPoint': ['.ppt', '.pptx'],
    'Text': ['.txt'],
    'CSV': ['.csv'],
    'RTF': ['.rtf'],
    'ODT': ['.odt'],
    'ODS': ['.ods'],
    'ODP': ['.odp'],
    'Markdown': ['.md'],
    'ReStructuredText': ['.rst'],
    'TeX': ['.tex'],
    'Apple Pages': ['.pages'],
    'Apple Numbers': ['.numbers'],
    'Apple Keynote': ['.key'],
    'MOBI': ['.mobi'],
    'AZW': ['.azw', '.azw3'],
    'LOG': ['.log'],
    'Presentations': ['.pps', '.ppsx'],
    'Spreadsheets': ['.tsv', '.xlsb'],
    'Notes': ['.note', '.onenote', '.evernote', '.enex', '.nb'],
    'MP4 Video': ['.mp4'],
    'AVI Video': ['.avi'],
    'MKV Video': ['.mkv'],
    'MOV Video': ['.mov'],
    'WMV Video': ['.wmv'],
    'FLV Video': ['.flv'],
    'WebM Video': ['.webm'],
    'MPEG Video': ['.mpeg', '.mpg'],
    '3GP Video': ['.3gp'],
    'VOB Video': ['.vob'],
    'TS Video': ['.ts'],
    'M4V Video': ['.m4v'],
    'RM Video': ['.rm'],
    'SWF Video': ['.swf'],
    'DIVX Video': ['.divx'],
    'ASF Video': ['.asf'],
    'OGV Video': ['.ogv'],
    'MTS Video': ['.mts'],
    'M2TS Video': ['.m2ts'],
    'F4V Video': ['.f4v'],
    'MPE Video': ['.mpe'],
    'MPV Video': ['.mpv'],
    'Screencasts': ['screencast', 'screenrec'],
    'MP3 Audio': ['.mp3'],
    'WAV Audio': ['.wav'],
    'FLAC Audio': ['.flac'],
    'AAC Audio': ['.aac'],
    'OGG Audio': ['.ogg'],
    'WMA Audio': ['.wma'],
    'M4A Audio': ['.m4a'],
    'AIFF Audio': ['.aiff'],
    'ALAC Audio': ['.alac'],
    'AMR Audio': ['.amr'],
    'MIDI Audio': ['.mid', '.midi'],
    'OPUS Audio': ['.opus'],
    'RA Audio': ['.ra'],
    'AU Audio': ['.au'],
    'AIF Audio': ['.aif'],
    'XM Audio': ['.xm'],
    'MOD Audio': ['.mod'],
    'IT Audio': ['.it'],
    'S3M Audio': ['.s3m'],
    'Ringtones': ['.m4r'],
    'TrueType Fonts': ['.ttf'],
    'OpenType Fonts': ['.otf'],
    'Web Fonts': ['.woff', '.woff2', '.eot'],
    'Bitmap Fonts': ['.fon', '.fnt', '.bdf', '.sfd'],
    'Type1 Fonts': ['.pfa', '.pfb', '.afm'],
    'Python': ['.py', '.pyc', '.pyo', '.pyw'],
    'JavaScript': ['.js'],
    'TypeScript': ['.ts'],
    'PHP': ['.php'],
    'Ruby': ['.rb'],
    'Perl': ['.pl'],
    'Lua': ['.lua'],
    'Groovy': ['.groovy'],
    'Scala': ['.scala'],
    'R': ['.r'],
    'Julia': ['.jl'],
    'Jupyter Notebooks': ['.ipynb'],
    'Shell Scripts': ['.sh', '.bash', '.zsh', '.csh', '.ksh'],
    'Batch Files': ['.bat', '.cmd'],
    'SQLite': ['.sqlite', '.sqlite3'],
    'SQL': ['.sql'],
    'Access': ['.mdb', '.accdb'],
    'DBF': ['.dbf'],
    'NDF': ['.ndf'],
    'LDF': ['.ldf'],
    'SDF': ['.sdf'],
    'Parquet': ['.parquet'],
    'Feather': ['.feather'],
    'HDF5': ['.h5'],
    'DTA': ['.dta'],
    'ARFF': ['.arff'],
    'DAT': ['.dat'],
    'INI Configs': ['.ini'],
    'CFG Configs': ['.cfg'],
    'YAML Configs': ['.yaml', '.yml'],
    'JSON Configs': ['.json'],
    'TOML Configs': ['.toml'],
    'ENV Configs': ['.env'],
    'CNF Configs': ['.cnf'],
    'Log Files': ['.log', '.out', '.err', '.trace'],
    'Dumps': ['.dmp', '.mdmp', '.core', '.crash', '.minidump'],
    'Registry': ['.reg'],
    'EFI': ['.efi'],
    'BIN': ['.bin'],
    'ICNS': ['.icns'],
    'CUR': ['.cur'],
    'DRV': ['.drv'],
    'LOCK': ['.lock'],
    'SWP': ['.swp'],
    'OLD': ['.old'],
    'EPUB': ['.epub'],
    'MOBI': ['.mobi'],
    'AZW3': ['.azw3'],
    'FB2': ['.fb2'],
    'DJVU': ['.djvu'],
    'LIT': ['.lit'],
    'PRC': ['.prc'],
    'CBZ': ['.cbz'],
    'CBR': ['.cbr'],
    'PDB': ['.pdb'],
    'OPF': ['.opf'],
    'Torrents': ['.torrent'],
    'PSD': ['.psd'],
    'AI': ['.ai'],
    'XD': ['.xd'],
    'Sketch': ['.sketch'],
    'Figma': ['.fig'],
    'CDR': ['.cdr'],
    'INDD': ['.indd'],
    'IDML': ['.idml'],
    'Affinity': ['.afdesign', '.afphoto', '.afpub'],
    'ASE': ['.ase'],
    'ABR': ['.abr'],
    'PAT': ['.pat'],
    'DWG': ['.dwg'],
    'DXF': ['.dxf'],
    'STEP': ['.step', '.stp'],
    'IGES': ['.iges', '.igs'],
    'SolidWorks': ['.sldprt', '.sldasm'],
    'Inventor': ['.ipt', '.iam'],
    'Fusion360': ['.f3d'],
    'OBJ': ['.obj'],
    'STL': ['.stl'],
    'PRT': ['.prt'],
    'CATIA': ['.catpart', '.catproduct'],
    'FBX': ['.fbx'],
    'DAE': ['.dae'],
    '3DS': ['.3ds'],
    'BLEND': ['.blend'],
    'PLY': ['.ply'],
    'GLTF': ['.gltf', '.glb'],
    'C4D': ['.c4d'],
    'MAX': ['.max'],
    'MA/MB': ['.ma', '.mb'],
    'LWO/LWS': ['.lwo', '.lws'],
    'X3D': ['.x3d'],
    'HEX': ['.hex'],
    'IMG': ['.img'],
    'ROM': ['.rom'],
    'FW': ['.fw'],
    'UPD': ['.upd'],
    'ELF': ['.elf'],
    'SB': ['.sb'],
    'S19': ['.s19'],
    'Favicon': ['favicon.ico'],
    'PEM': ['.pem'],
    'CRT': ['.crt'],
    'CER': ['.cer'],
    'DER': ['.der'],
    'PFX': ['.pfx'],
    'P12': ['.p12'],
    'KEY': ['.key'],
    'CSR': ['.csr'],
    'JKS': ['.jks'],
    'Keystore': ['.keystore'],
    'Game Saves': ['.sav', '.save', '.dsv', '.gci', '.srm', '.state', '.ess', '.zsv'],
    'Game ROMs': ['.nes', '.sfc', '.smc', '.gba', '.gb', '.gbc', '.nds', '.n64', '.z64', '.bin', '.iso', '.cue', '.img', '.md', '.sms', '.gg', '.pce', '.sg', '.ws', '.wsc', '.ngp', '.ngc', '.cdi', '.gdi', '.xci', '.nsp', '.cia', '.3ds', '.wad', '.dol', '.elf'],
    'Game Patches': ['.ips', '.ups', '.bps', '.ppf', '.xdelta', '.aps'],
    'Game Mods': ['.mod', '.vpk', '.wad', '.pk3', '.pk4', '.bsa', '.esp', '.esm', '.ba2', '.rpf', '.oiv'],
    'Game Assets': ['.dat', '.bsa', '.rpf', '.arc', '.gcf', '.vpk', '.uasset', '.utx', '.umx', '.upk', '.pakchunk'],
    'Game Maps': ['.bsp', '.map', '.nav', '.dem', '.lin', '.p2c', '.vmf', '.vmt', '.vtf', '.ain', '.lmp', '.rmf', '.wad'],
    'Game Textures': ['.vtf', '.dds', '.tga', '.bmp', '.png', '.jpg', '.jpeg', '.gif'],
    'Game Audio': ['.wem', '.bnk', '.xma', '.adx', '.hca', '.at9'],
    'Game Scripts': ['.nut', '.sc', '.gsc', '.inc', '.sma', '.amxx'],
    'CMS': ['.tpl', '.twig', '.smarty', '.blade.php', '.htaccess'],
    'Web HTML': ['.html', '.htm'],
    'Web CSS': ['.css', '.scss', '.sass', '.less'],
    'Web JS': ['.js', '.jsx'],
    'Web TS': ['.ts', '.tsx'],
    'Web PHP': ['.php'],
    'Web ASP': ['.asp', '.aspx'],
    'Web JSP': ['.jsp'],
    'Web Vue': ['.vue'],
    'Web Svelte': ['.svelte'],
    'Web EJS': ['.ejs'],
    'Web Pug': ['.pug', '.jade'],
    'Flash SWF': ['.swf'],
    'Flash FLV': ['.flv'],
    'Flash FLA': ['.fla'],
    'Flash AS': ['.as'],
    'Flash XFL': ['.xfl'],
    'Shortcuts': ['.lnk', '.url', '.desktop', '.webloc', '.pif'],
    'Cheats/Trainers': ['.cht', '.trainer', '.ct', '.pat', '.gct'],
    'Maps/GIS': ['.shp', '.kml', '.kmz', '.gpx', '.osm', '.geojson', '.tab', '.mif', '.sid'],
    'Readme/License': ['readme', 'license', 'copying', 'changelog', 'notice'],
    'Other': [],
    'Folders': [],
}

ABOUT_TEXT = """
File Sorter v5.0\n\nАвтор: Fal1sev4n\n\nхочу шаурму похавать\n\nGitHub: https://github.com/faliseven
"""

LANGUAGES = {
    'ru': {
        'select_folder': 'Папка для сортировки:',
        'categories': 'Категории для сортировки:',
        'recursive': 'Сортировать во вложенных папках',
        'select_all': 'Выбрать все',
        'deselect_all': 'Снять все',
        'about': 'О программе',
        'undo': 'Возврат',
        'sort': 'Сортировать',
        'preview': 'Предпросмотр',
        'open_folder': 'Открыть папку',
        'close': 'Закрыть',
        'plan': 'План сортировки',
        'no_history': 'Нет истории для отката!',
        'undo_success': 'Все файлы возвращены на место!',
        'undo_partial': 'Некоторые файлы не удалось вернуть: {}',
        'choose_folder': 'Выберите папку!',
        'choose_category': 'Выберите хотя бы одну категорию!',
        'sorted_files': 'Отсортировано файлов: {}',
        'done': 'Готово',
        'skipped': 'Пропущен: {}',
        'moved': '{} → {}',
        'moved_folder': 'Папка: {} → Folders',
        'error': 'Ошибка: {} — {}',
        'error_folder': 'Ошибка (папка): {} — {}',
        'undo': 'Возврат',
        'preview_stays': '{} → (останется на месте)',
        'lang': 'Язык',
        'browse': 'Обзор',
    },
    'en': {
        'select_folder': 'Folder to sort:',
        'categories': 'Categories to sort:',
        'recursive': 'Sort in subfolders',
        'select_all': 'Select all',
        'deselect_all': 'Deselect all',
        'about': 'About',
        'undo': 'Undo',
        'sort': 'Sort',
        'preview': 'Preview',
        'open_folder': 'Open folder',
        'close': 'Close',
        'plan': 'Sort plan',
        'no_history': 'No undo history!',
        'undo_success': 'All files restored!',
        'undo_partial': 'Some files could not be restored: {}',
        'choose_folder': 'Please select a folder!',
        'choose_category': 'Please select at least one category!',
        'sorted_files': 'Files sorted: {}',
        'done': 'Done',
        'skipped': 'Skipped: {}',
        'moved': '{} → {}',
        'moved_folder': 'Folder: {} → Folders',
        'error': 'Error: {} — {}',
        'error_folder': 'Error (folder): {} — {}',
        'undo': 'Undo',
        'preview_stays': '{} → (will stay)',
        'lang': 'Language',
        'browse': 'Browse',
    }
}

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class GlowButton(ctk.CTkButton):
    def __init__(self, master=None, **kwargs):
        glow_color = kwargs.pop('glow_color', '#00e0ff')
        super().__init__(master, **kwargs)
        self._glow_color = glow_color
        self._normal_color = self.cget('fg_color')
        if isinstance(self._normal_color, list):
            self._normal_color = self._normal_color[0]
        self._glow_alpha = 0
        self._glow_animating = False
        self._glow_target = 0
        self._hover_bg = '#23272f'
        self._normal_bg = self.cget('fg_color')
        if isinstance(self._normal_bg, list):
            self._normal_bg = self._normal_bg[0]
        self.bind('<Enter>', self._on_enter)
        self.bind('<Leave>', self._on_leave)
    def _on_enter(self, event=None):
        self._glow_target = 1
        if not self._glow_animating:
            self._glow_animating = True
            self._animate_glow()
        self.configure(fg_color=self._blend_colors(self._normal_bg, self._glow_color, 0.12))
    def _on_leave(self, event=None):
        self._glow_target = 0
        if not self._glow_animating:
            self._glow_animating = True
            self._animate_glow()
        self.configure(fg_color=self._normal_bg)
    def _animate_glow(self):
        step = 0.15
        if self._glow_target == 1 and self._glow_alpha < 1.0:
            self._glow_alpha = min(self._glow_alpha + step, 1.0)
            color = self._blend_colors(self._normal_color, self._glow_color, self._glow_alpha)
            self.configure(border_color=color, border_width=3)
            self.after(25, self._animate_glow)
        elif self._glow_target == 0 and self._glow_alpha > 0.0:
            self._glow_alpha = max(self._glow_alpha - step, 0.0)
            color = self._blend_colors(self._normal_color, self._glow_color, self._glow_alpha)
            self.configure(border_color=color, border_width=3)
            self.after(25, self._animate_glow)
        else:
            if self._glow_target == 0:
                self.configure(border_color=self._normal_color, border_width=0)
            else:
                self.configure(border_color=self._glow_color, border_width=3)
            self._glow_animating = False
    def _blend_colors(self, c1, c2, alpha):
        alpha = max(0.0, min(1.0, alpha))
        def hex_to_rgb(h):
            h = h.lstrip('#')
            return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
        def rgb_to_hex(rgb):
            return '#%02x%02x%02x' % rgb
        if isinstance(c1, list):
            c1 = c1[0]
        if isinstance(c2, list):
            c2 = c2[0]
        r1, g1, b1 = hex_to_rgb(c1 if c1 else '#23272f')
        r2, g2, b2 = hex_to_rgb(c2)
        r = int(r1 + (r2 - r1) * alpha)
        g = int(g1 + (g2 - g1) * alpha)
        b = int(b1 + (b2 - b1) * alpha)
        r = max(0, min(255, r))
        g = max(0, min(255, g))
        b = max(0, min(255, b))
        return rgb_to_hex((r, g, b))

class HoverCheckBox(ctk.CTkCheckBox):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self._normal_bg = self.cget('fg_color')
        if isinstance(self._normal_bg, list):
            self._normal_bg = self._normal_bg[0]
        self._hover_bg = '#313846'
        self.bind('<Enter>', self._on_enter)
        self.bind('<Leave>', self._on_leave)
    def _on_enter(self, event=None):
        self._fade_to(self._hover_bg)
    def _on_leave(self, event=None):
        self._fade_to(self._normal_bg)
    def _fade_to(self, target_color, steps=8, delay=18):
        start_color = self.cget('fg_color')
        if isinstance(start_color, list):
            start_color = start_color[0]
        def hex_to_rgb(h):
            h = h.lstrip('#')
            return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
        def rgb_to_hex(rgb):
            return '#%02x%02x%02x' % rgb
        rgb1 = hex_to_rgb(start_color)
        rgb2 = hex_to_rgb(target_color)
        for i in range(1, steps+1):
            r = int(rgb1[0] + (rgb2[0] - rgb1[0]) * i / steps)
            g = int(rgb1[1] + (rgb2[1] - rgb1[1]) * i / steps)
            b = int(rgb1[2] + (rgb2[2] - rgb1[2]) * i / steps)
            self.after(i*delay, lambda c=rgb_to_hex((r, g, b)): self.configure(fg_color=c))

class FileSorterApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title('File Sorter')
        self.geometry('900x700')
        self.resizable(False, False)
        self.folder_path = ctk.StringVar()
        self.check_vars = {cat: ctk.BooleanVar(value=True) for cat in CATEGORIES}
        self.progress = None
        self.log_box = None
        self.count_label = None
        self.recursive = ctk.BooleanVar(value=False)
        self.last_moves = []
        self.lang = 'ru'
        self.create_widgets()

    def t(self, key, *args):
        return LANGUAGES[self.lang].get(key, key).format(*args)

    def create_widgets(self):
        pad = 12
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)

        
        header = ctk.CTkFrame(self, height=56, corner_radius=16)
        header.grid(row=0, column=0, columnspan=2, sticky='nsew', padx=0, pady=(0, 4))
        header.grid_columnconfigure(0, weight=0)
        header.grid_columnconfigure(1, weight=1)
        header.grid_columnconfigure(2, weight=0)
        
        logo = ctk.CTkLabel(header, text='🗂️', font=('Segoe UI', 28, 'bold'))
        logo.grid(row=0, column=0, padx=18, pady=8)
        
        title = ctk.CTkLabel(header, text='FileSorter', font=('Segoe UI', 22, 'bold'))
        title.grid(row=0, column=1, padx=0, pady=8, sticky='w')
        
        btn_frame = ctk.CTkFrame(header, fg_color='transparent')
        btn_frame.grid(row=0, column=2, padx=12, pady=8, sticky='e')
        GlowButton(btn_frame, text=self.t('about'), command=self.show_about, width=90, glow_color='#00e0ff').pack(side='left', padx=4)
        GlowButton(btn_frame, text=self.t('lang'), command=lambda: self.set_lang('en' if self.lang=='ru' else 'ru'), width=90, glow_color='#00e0ff').pack(side='left', padx=4)
        
        if hasattr(ctk, 'set_appearance_mode'):
            GlowButton(btn_frame, text='🌗', command=self.toggle_theme, width=44, glow_color='#00e0ff').pack(side='left', padx=4)

       
        sidebar = ctk.CTkFrame(self, width=260, corner_radius=16)
        sidebar.grid(row=1, column=0, sticky='nsw', padx=(8, 4), pady=(0, 4))
        sidebar.grid_rowconfigure(2, weight=1)
        ctk.CTkLabel(sidebar, text=self.t('categories'), font=('Segoe UI', 15, 'bold')).pack(anchor='w', padx=16, pady=(12, 2))
        
        self.filter_search = ctk.StringVar()
        search_entry = ctk.CTkEntry(sidebar, textvariable=self.filter_search, width=220, placeholder_text='Поиск...')
        search_entry.pack(padx=16, pady=(0, 8))
        search_entry.bind('<KeyRelease>', self.update_filter_list)
        
        self.filter_scroll = ctk.CTkScrollableFrame(sidebar, width=220, height=420)
        self.filter_scroll.pack(padx=16, pady=(0, 8), fill='both', expand=True)
        self.render_filter_list()
        
        act_frame = ctk.CTkFrame(sidebar, fg_color='transparent')
        act_frame.pack(padx=16, pady=(0, 8), fill='x')
        GlowButton(act_frame, text=self.t('select_all'), command=self.select_all, width=100, glow_color='#00e0ff').pack(side='left', padx=2)
        GlowButton(act_frame, text=self.t('deselect_all'), command=self.deselect_all, width=100, glow_color='#00e0ff').pack(side='left', padx=2)

        
        center = ctk.CTkFrame(self, corner_radius=16)
        center.grid(row=1, column=1, sticky='nsew', padx=(4, 8), pady=(0, 4))
        center.grid_rowconfigure(4, weight=1)
        center.grid_columnconfigure(0, weight=1)
       
        path_frame = ctk.CTkFrame(center, fg_color='transparent')
        path_frame.grid(row=0, column=0, sticky='ew', pady=(18, 4), padx=18)
        ctk.CTkLabel(path_frame, text=self.t('select_folder'), anchor='w').pack(side='left', padx=(0, 8))
        ctk.CTkEntry(path_frame, textvariable=self.folder_path, width=340, state='readonly').pack(side='left', padx=4)
        GlowButton(path_frame, text=self.t('browse'), command=self.browse_folder, width=80, glow_color='#00e0ff').pack(side='left', padx=4)
        
        btns_frame = ctk.CTkFrame(center, fg_color='transparent')
        btns_frame.grid(row=1, column=0, sticky='ew', pady=(8, 4), padx=18)
        GlowButton(btns_frame, text='🔄 ' + self.t('undo'), command=self.undo_last, width=120, height=36, glow_color='#00e0ff').pack(side='left', padx=6)
        GlowButton(btns_frame, text='👁 ' + self.t('preview'), command=self.preview_sort, width=120, height=36, glow_color='#00e0ff').pack(side='left', padx=6)
        GlowButton(btns_frame, text='🗂 ' + self.t('sort'), command=self.start_sort, width=140, height=40, glow_color='#00e0ff').pack(side='left', padx=6)
        GlowButton(btns_frame, text='📂 ' + self.t('open_folder'), command=self.open_folder, width=120, height=36, glow_color='#00e0ff').pack(side='left', padx=6)
        
        self.progress = ctk.CTkProgressBar(center)
        self.progress.grid(row=2, column=0, sticky='ew', padx=18, pady=(8, 0))
        self.progress.set(0)
       
        self.preview_box = ctk.CTkTextbox(center, height=180, width=540, font=('Consolas', 11))
        self.preview_box.grid(row=3, column=0, sticky='nsew', padx=18, pady=(8, 0))
        self.preview_box.configure(state='disabled')
        
        self.count_label = ctk.CTkLabel(center, text='', text_color='#50fa7b', font=('Segoe UI', 14, 'bold'))
        self.count_label.grid(row=4, column=0, pady=(8, 0))

      
        self.log_box = ctk.CTkTextbox(center, height=100, width=540, font=('Consolas', 10))
        self.log_box.grid(row=5, column=0, sticky='nsew', padx=18, pady=(8, 0))
        self.log_box.configure(state='disabled')

      
        status = ctk.CTkFrame(self, height=32, corner_radius=12)
        status.grid(row=2, column=0, columnspan=2, sticky='ew', padx=8, pady=(0, 8))
        self.status_label = ctk.CTkLabel(status, text='Ready', anchor='w', font=('Segoe UI', 11))
        self.status_label.pack(side='left', padx=12)
        self.status_path = ctk.CTkLabel(status, text='', anchor='w', font=('Segoe UI', 11, 'italic'))
        self.status_path.pack(side='left', padx=12)
        self.status_count = ctk.CTkLabel(status, text='', anchor='e', font=('Segoe UI', 11, 'bold'))
        self.status_count.pack(side='right', padx=12)

    def set_lang(self, lang):
        self.lang = lang
        for widget in self.winfo_children():
            widget.destroy()
        self.create_widgets()
        self.show_notification(self.t('lang') + f': {lang.upper()}')

    def show_notification(self, text):
        notif = ctk.CTkToplevel(self)
        notif.overrideredirect(True)
        notif.geometry(f"340x60+{self.winfo_x()+self.winfo_width()-370}+{self.winfo_y()+self.winfo_height()-120}")
        notif.configure(bg='#23272f')
        frame = ctk.CTkFrame(notif, fg_color='#23272f', corner_radius=18)
        frame.pack(expand=True, fill='both')
        inner = ctk.CTkFrame(frame, fg_color='transparent')
        inner.pack(expand=True, fill='both', padx=8, pady=8)
        icon = ctk.CTkLabel(inner, text='ℹ️', font=('Segoe UI', 22))
        icon.pack(side='left', padx=(8, 12))
        label = ctk.CTkLabel(inner, text=text, font=('Segoe UI', 14, 'bold'), text_color='#f8f8f2', bg_color='transparent')
        label.pack(side='left', expand=True, fill='both')
        notif.attributes('-alpha', 0.0)
        self._fade_in(notif, 0.0)
        notif.after(2200, lambda: self._fade_out(notif, 1.0))

    def _fade_in(self, win, alpha):
        try:
            if not win.winfo_exists():
                return
        except Exception:
            return
        if alpha < 1.0:
            win.attributes('-alpha', alpha)
            win.after(20, lambda: self._fade_in(win, alpha + 0.1))
        else:
            win.attributes('-alpha', 1.0)

    def _fade_out(self, win, alpha):
        try:
            if not win.winfo_exists():
                return
        except Exception:
            return
        if alpha > 0.0:
            win.attributes('-alpha', alpha)
            win.after(20, lambda: self._fade_out(win, alpha - 0.1))
        else:
            try:
                win.destroy()
            except Exception:
                pass

    def custom_messagebox(self, type_, title, text):
      
        if type_ == 'info':
            messagebox.showinfo(title, text)
        elif type_ == 'warning':
            messagebox.showwarning(title, text)
        elif type_ == 'error':
            messagebox.showerror(title, text)
        else:
            messagebox.showinfo(title, text)

    def smart_info(self, title, msg):
        self.show_notification(msg)
        self.custom_messagebox('info', title, msg)
    def smart_warn(self, title, msg):
        self.show_notification(msg)
        self.custom_messagebox('warning', title, msg)
    def smart_error(self, title, msg):
        self.show_notification(msg)
        self.custom_messagebox('error', title, msg)

    def show_about(self):
        win = ctk.CTkToplevel(self)
        win.title(self.t('about'))
        win.geometry('420x320')
        win.attributes('-alpha', 0.0)
        txt = ctk.CTkTextbox(win, font=('Segoe UI Variable', 13), width=380, height=220)
        txt.pack(padx=10, pady=10, fill='both', expand=True)
        txt.insert('end', ABOUT_TEXT)
        txt.configure(state='disabled')
        GlowButton(win, text=self.t('close'), command=win.destroy, width=120, glow_color='#00e0ff', font=('Segoe UI Variable', 14, 'bold')).pack(pady=8)
        self._fade_in(win, 0.0)

    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder_path.set(folder)

    def select_all(self):
        for var in self.check_vars.values():
            var.set(True)

    def deselect_all(self):
        for var in self.check_vars.values():
            var.set(False)

    def open_folder(self):
        folder = self.folder_path.get()
        if folder:
            try:
                os.startfile(folder)
            except Exception as e:
                self.smart_error('Ошибка', f'Не удалось открыть папку: {e}')

    def log(self, msg):
        self.log_box.configure(state='normal')
        self.log_box.insert('end', msg + '\n')
        self.log_box.see('end')
        self.log_box.configure(state='disabled')

    def preview_sort(self):
        folder = self.folder_path.get()
        if not folder:
            self.smart_warn(self.t('done'), self.t('choose_folder'))
            return
        selected_cats = [cat for cat, var in self.check_vars.items() if var.get()]
        if not selected_cats:
            self.smart_warn(self.t('done'), self.t('choose_category'))
            return
        files = self._get_files(folder, self.recursive.get())
        plan = []
        for item_path in files:
            item = os.path.basename(item_path)
            if os.path.isdir(item_path):
                if 'Folders' in selected_cats:
                    plan.append(self.t('moved_folder', item))
                continue
            ext = os.path.splitext(item)[1].lower()
            found = False
            for cat in selected_cats:
                if cat == 'Folders':
                    continue
                if ext in CATEGORIES[cat] or any(key in item.lower() for key in CATEGORIES[cat] if not key.startswith('.')):
                    plan.append(self.t('moved', item, cat))
                    found = True
                    break
            if not found:
                plan.append(self.t('preview_stays', item))
        self.show_preview_window(plan)

    def show_preview_window(self, plan):
        win = ctk.CTkToplevel(self)
        win.title(self.t('plan'))
        win.geometry('600x500')
        win.attributes('-alpha', 0.0)
        txt = ctk.CTkTextbox(win, font=('Consolas', 11), width=580, height=440)
        txt.pack(padx=10, pady=10, fill='both', expand=True)
        txt.insert('end', '\n'.join(plan))
        txt.configure(state='disabled')
        GlowButton(win, text=self.t('close'), command=win.destroy, width=120, glow_color='#00e0ff').pack(pady=8)
        self._fade_in(win, 0.0)

    def undo_last(self):
        if not self.last_moves:
            self.smart_info(self.t('undo'), self.t('no_history'))
            return
        errors = 0
        for dest, src in reversed(self.last_moves):
            try:
                os.makedirs(os.path.dirname(src), exist_ok=True)
                shutil.move(dest, src)
            except Exception as e:
                errors += 1
        self.last_moves.clear()
        if errors == 0:
            self.smart_info(self.t('undo'), self.t('undo_success'))
        else:
            self.smart_warn(self.t('undo'), self.t('undo_partial', errors))

    def start_sort(self):
        threading.Thread(target=self.sort_files, daemon=True).start()

    def sort_files(self):
        folder = self.folder_path.get()
        if not folder:
            self.smart_warn(self.t('done'), self.t('choose_folder'))
            return
        selected_cats = [cat for cat, var in self.check_vars.items() if var.get()]
        if not selected_cats:
            self.smart_warn(self.t('done'), self.t('choose_category'))
            return
        self.log_box.configure(state='normal')
        self.log_box.delete('1.0', 'end')
        self.log_box.configure(state='disabled')
        self.count_label.configure(text='')
        files = self._get_files(folder, self.recursive.get())
        total = len(files)
        moved = 0
        self.progress.set(0)
        self.last_moves = []
        for idx, item_path in enumerate(files):
            item = os.path.basename(item_path)
            if os.path.isdir(item_path):
                if 'Folders' in selected_cats:
                    dest_dir = os.path.join(os.path.dirname(item_path), 'Folders')
                    os.makedirs(dest_dir, exist_ok=True)
                    try:
                        shutil.move(item_path, os.path.join(dest_dir, item))
                        self.log(self.t('moved_folder', item))
                        self.last_moves.append((os.path.join(dest_dir, item), item_path))
                        moved += 1
                    except Exception as e:
                        self.log(self.t('error_folder', item, e))
                continue
            ext = os.path.splitext(item)[1].lower()
            moved_flag = False
            for cat in selected_cats:
                if cat == 'Folders':
                    continue
                if ext in CATEGORIES[cat] or any(key in item.lower() for key in CATEGORIES[cat] if not key.startswith('.')):
                    dest_dir = os.path.join(os.path.dirname(item_path), cat)
                    os.makedirs(dest_dir, exist_ok=True)
                    try:
                        shutil.move(item_path, os.path.join(dest_dir, item))
                        self.log(self.t('moved', item, cat))
                        self.last_moves.append((os.path.join(dest_dir, item), item_path))
                        moved += 1
                    except Exception as e:
                        self.log(self.t('error', item, e))
                    moved_flag = True
                    break
            if not moved_flag:
                self.log(self.t('skipped', item))
            self.progress.set((idx + 1) / total)
            self.update_idletasks()
            time.sleep(0.01)
        self.count_label.configure(text=self.t('sorted_files', moved))
        self.smart_info(self.t('done'), self.t('sorted_files', moved))

    def _get_files(self, folder, recursive):
        files = []
        for root, dirs, filenames in os.walk(folder):
            for name in filenames:
                files.append(os.path.join(root, name))
            if recursive:
                for d in dirs:
                    files.append(os.path.join(root, d))
            if not recursive:
                break
        return files

    def toggle_theme(self):
        current = ctk.get_appearance_mode()
        if current == "Dark":
            ctk.set_appearance_mode("Light")
        else:
            ctk.set_appearance_mode("Dark")

    def update_filter_list(self, event=None):
        self.render_filter_list()

    def render_filter_list(self):
        for widget in self.filter_scroll.winfo_children():
            widget.destroy()
        search = self.filter_search.get().lower()
        delay = 0
        for cat in CATEGORIES:
            if search in cat.lower():
                cb = HoverCheckBox(self.filter_scroll, text=cat, variable=self.check_vars[cat])
                cb.pack(anchor='w', padx=8, pady=2)
                cb.configure(fg_color=cb._hover_bg)
                cb.after(delay, lambda w=cb: w._fade_to(w._normal_bg))
                delay += 20

if __name__ == '__main__':
    global app
    app = FileSorterApp()
    app.mainloop() 
