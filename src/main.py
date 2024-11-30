import gi

gi.require_version("Gtk", "3.0")
from povview.utils.utils import setup_goocanvas

setup_goocanvas()
from gi.repository import Gtk, GooCanvas

from lib.main_menu import Main_menu
from povview.elements.objects.cone import Cone
from povview.elements.objects.ovus import Ovus
from povview.parser import Parser
from povview.tracer import Tracer


TEST_CONE = {
    "type": "cone",
    "top_center": [0, 0, 0],
    "top_radius": 100.0,
    "bottom_center": [0, -150, 0],
    "bottom_radius": 50.0,
    "object_modifiers": [],
}
TEST_OVUS = {
    "type": "ovus",
    "bottom_radius": 100.0,
    "top_radius": 150.0,
    "object_modifiers": [],
}

COLORS = {
    "White": (1, 1, 1),
    "Black": (0, 0, 0),
    "Red": (1, 0, 0),
    "Green": (0, 1, 0),
    "Blue": (0, 0, 1),
    "Yellow": (1, 1, 0),
    "Orange": (1, 0.5, 0),
    "Cyan": (0, 1, 1),
    "Purple": (1, 0, 1),
}


class Views(Gtk.Grid):
    def __init__(self):
        super().__init__(row_spacing=4, column_spacing=4, margin=4)

        self.objs = []

        self.views = {}
        for x, y, lbl in [(0, 0, "xy"), (1, 0, "zy"), (0, 1, "zx"), (1, 1, "Tracer")]:
            frame = Gtk.Frame(label=lbl, label_xalign=0.04, hexpand=True, vexpand=True)
            frame.connect("size-allocate", self.on_frame_size_allocate)
            self.attach(frame, x, y, 1, 1)

            canvas = GooCanvas.Canvas(
                automatic_bounds=False, bounds_from_origin=False, bounds_padding=10
            )
            frame.add(canvas)
            self.views[lbl] = {"frame": frame, "canvas": canvas}

            # Block scroll events on the canvas
            canvas.connect("scroll-event", self.on_scroll_event)

    def on_scroll_event(self, widget, event):
        return True

    def on_frame_size_allocate(self, widget, allocation):
        self.frame_width = widget.get_allocated_width()
        self.frame_height = widget.get_allocated_height()
        self.center_canvases()

    def center_canvases(self):
        for i, view in enumerate(self.views.values()):
            if i == 3:
                continue
            canvas = view["canvas"]
            canvas.set_bounds(
                -self.frame_width / 2,
                -self.frame_height / 2,
                self.frame_width,
                self.frame_height,
            )

    def clear_views(self):
        for view in self.views:
            root = self.views[view]["canvas"].get_root_item()
            for i in range(root.get_n_children() - 1, -1, -1):
                root.get_child(i).remove()

    def full_clear_views(self):
        for view in self.views:
            root = self.views[view]["canvas"].get_root_item()
            for i in range(root.get_n_children() - 1, -1, -1):
                root.get_child(i).remove()
        self.objs.clear()

    def add_object(self, obj, **kwargs):
        if kwargs.get("subdiv"):
            obj.set_params(**kwargs)
        self.objs.append(obj)

    def draw(self):
        if not len(self.objs):
            return

        for obj in self.objs:
            obj.draw_on(self.views)

    def trace(self, tracer):
        if not len(self.objs):
            return

        tracer.trace_scene()
        tracer.draw_on(self.views, (self.frame_width, self.frame_height))


class MainWindow(Gtk.Window):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.connect("destroy", lambda x: Gtk.main_quit())
        self.set_default_size(800, 600)

        mm = self.make_main_menu()

        self.updating_yaw = False
        self.updating_pitch = False
        self.updating_roll = False

        # --- Subdiv Label and Entry ---
        subdiv_label = Gtk.Label(label="SUBDIVISIONS")
        subdiv_label.set_xalign(0)
        self.subdiv_entry = Gtk.Entry()
        self.subdiv_entry.set_text("10")
        self.subdiv_entry.set_hexpand(True)
        self.subdiv_entry.connect("changed", self.on_params_changed)

        subdiv_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        subdiv_vbox.pack_start(subdiv_label, False, False, 0)
        subdiv_vbox.pack_start(self.subdiv_entry, False, False, 0)

        # --- Resolution Label ---
        resolution_label = Gtk.Label(label="RESOLUTION")
        resolution_label.set_xalign(0)

        # --- Width Entry ---
        width_label = Gtk.Label(label="Width")
        width_label.set_xalign(0)
        self.width_entry = Gtk.Entry()
        self.width_entry.set_text("800")  # Default width
        self.width_entry.set_hexpand(True)
        self.width_entry.connect("changed", self.on_params_changed)

        width_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        width_box.pack_start(width_label, False, False, 0)
        width_box.pack_start(self.width_entry, True, True, 0)

        # --- Height Entry ---
        height_label = Gtk.Label(label="Height")
        height_label.set_xalign(0)
        self.height_entry = Gtk.Entry()
        self.height_entry.set_text("600")  # Default height
        self.height_entry.set_hexpand(True)
        self.height_entry.connect("changed", self.on_params_changed)

        height_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        height_box.pack_start(height_label, False, False, 0)
        height_box.pack_start(self.height_entry, True, True, 0)

        # --- Trace Button ---
        self.trace_button = Gtk.Button(label="Trace")
        self.trace_button.connect("clicked", self.on_trace_button_clicked)
        self.trace_button.set_hexpand(False)
        self.trace_button.set_vexpand(False)

        # --- ComboBox de Presets de Resolución ---
        presets_label = Gtk.Label(label="Presets")
        presets_label.set_xalign(0)

        self.presets_combobox = Gtk.ComboBoxText()
        self.presets_combobox.set_hexpand(False)
        self.presets_combobox.connect("changed", self.on_preset_changed)

        # Añadir opciones de presets
        self.presets_combobox.append_text("800x600")
        self.presets_combobox.append_text("1024x768")
        self.presets_combobox.append_text("1280x720")
        self.presets_combobox.append_text("1920x1080")
        self.presets_combobox.append_text("Custom")
        self.presets_combobox.set_active(0)  # Seleccionar el primer preset por defecto

        self.tracer_model = "ray_tracer"
        # --- Label y ComboBox de Render Mode ---
        render_mode_label = Gtk.Label(label="Render Mode")
        render_mode_label.set_xalign(0)

        self.render_mode_combobox = Gtk.ComboBoxText()
        self.render_mode_combobox.set_hexpand(False)
        self.render_mode_combobox.append_text("Raytracing")
        self.render_mode_combobox.append_text("Pathtracing")
        self.render_mode_combobox.set_active(0)  # Seleccionar "Raytracing" por defecto
        self.render_mode_combobox.connect("changed", self.on_render_mode_changed)

        # --- Box para Width y Height lado a lado ---
        size_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        size_box.pack_start(width_box, False, False, 0)
        size_box.pack_start(height_box, False, False, 0)
        size_box.pack_start(presets_label, False, False, 0)
        size_box.pack_start(self.presets_combobox, False, False, 0)
        size_box.pack_start(render_mode_label, False, False, 0)
        size_box.pack_start(self.render_mode_combobox, False, False, 0)
        size_box.pack_start(self.trace_button, False, False, 0)

        v_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        v_box.pack_start(resolution_label, False, False, 0)
        v_box.pack_start(size_box, False, False, 0)

        # --- Box Horizontal para Resolution, Size y Trace Button ---
        resolution_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        resolution_box.pack_start(v_box, False, False, 0)

        # --- Box Principal Horizontal (Subdiv y Resolution Section) ---
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=200)
        hbox.set_homogeneous(False)

        hbox.pack_start(subdiv_vbox, False, False, 0)
        hbox.pack_start(resolution_box, False, False, 0)

        # --- Initialize Views ---
        self.views = Views()  # Asegúrate de que la clase Views esté definida

        # --- Grid Layout ---
        grid = Gtk.Grid(vexpand=True)
        grid.attach(mm, 0, 0, 2, 1)
        grid.attach(hbox, 0, 1, 2, 1)
        grid.attach(self.views, 0, 2, 2, 1)
        self.add(grid)
        self.show_all()
        self.maximize()

    def run(self):
        Gtk.main()

    def make_main_menu(self):
        mm = Main_menu(["_File", "_Tests"])
        mm.add_items_to(
            "_File",
            (
                ("Open POV file", self.on_open_pov_clicked),
                ("Clear scene", self.on_clear_clicked),
                ("Redraw", self.on_redraw_clicked),
                (None, None),
                ("_Quit", self.on_quit_clicked),
            ),
        )

        mm.add_items_to("_Tests", (("Add Cone to viewer", self.on_add_cone_clicked),))
        mm.add_items_to("_Tests", (("Add Ovus to viewer", self.on_add_ovus_clicked),))

        return mm

    def get_params(self):
        return {
            "subdiv": int(self.subdiv_entry.get_text()),
        }

    def on_preset_changed(self, combobox):
        preset = combobox.get_active_text()
        if preset:
            match preset:
                case "800x600":
                    self.width_entry.set_text("800")
                    self.height_entry.set_text("600")
                case "1024x768":
                    self.width_entry.set_text("1024")
                    self.height_entry.set_text("768")
                case "1280x720":
                    self.width_entry.set_text("1280")
                    self.height_entry.set_text("720")
                case "1920x1080":
                    self.width_entry.set_text("1920")
                    self.height_entry.set_text("1080")
                case "Custom":
                    self.width_entry.set_text("")
                    self.height_entry.set_text("")

    def on_params_changed(self, param):
        self.views.clear_views()
        for obj in self.views.objs:
            obj.set_params(**self.get_params())
        self.views.draw()

    def on_render_mode_changed(self, combo):
        tracer_selected = combo.get_active_text()
        match tracer_selected:
            case "Raytracing":
                self.tracer_model = "ray_tracer"
            case "Pathtracing":
                self.tracer_model = "path_tracer"

    def on_trace_button_clicked(self, menuitem):
        self.views.trace(
            Tracer(
                self.parsed_file["lights"],
                self.parsed_file["cameras"][0],
                self.parsed_file["objects"],
                (int(self.width_entry.get_text()), int(self.height_entry.get_text())),
                model=self.tracer_model,
            )
        )

    def on_add_cone_clicked(self, menuitem):
        self.views.full_clear_views()
        self.views.add_object(
            Cone(
                TEST_CONE,
                **self.get_params(),
            )
        )
        self.views.draw()

    def on_add_ovus_clicked(self, menuitem):
        self.views.full_clear_views()
        self.views.add_object(
            Ovus(
                TEST_OVUS,
                **self.get_params(),
            )
        )
        self.views.draw()

    def on_clear_clicked(self, menuitem):
        self.views.clear_views()

    def on_redraw_clicked(self, menuitem):
        self.views.clear_views()
        for obj in self.views.objs:
            obj.set_params(**self.get_params())
        self.views.draw()

    def on_open_pov_clicked(self, menuitem):
        fc = Gtk.FileChooserDialog(action=Gtk.FileChooserAction.OPEN)
        fc.add_buttons(
            "Cancel", Gtk.ResponseType.CANCEL, "Open", Gtk.ResponseType.ACCEPT
        )

        for f_name, f_pattern in (
            ("POVday files (*.pov)", "*.pov"),
            ("All files (*)", "*"),
        ):
            filter = Gtk.FileFilter()
            filter.set_name(f_name)
            filter.add_pattern(f_pattern)
            fc.add_filter(filter)

        if fc.run() == Gtk.ResponseType.ACCEPT:
            self.file = fc.get_filename()
            print(self.file)

        fc.destroy()

        self.views.full_clear_views()

        self.parsed_file = Parser().parse(self.file)
        objects = self.parsed_file["objects"]

        for obj in objects:
            self.views.add_object(obj, **self.get_params())
        self.views.draw()

    def on_quit_clicked(self, menuitem):
        Gtk.main_quit()


def main(args):
    mainwdw = MainWindow()
    mainwdw.run()

    return 0


if __name__ == "__main__":
    import sys

    sys.exit(main(sys.argv))
