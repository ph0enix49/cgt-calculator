import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gio, Pango


class Main(object):
    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file("main.glade")
        self.builder.connect_signals(self)
        self.main_box = self.builder.get_object("main_box")
        self.window = self.builder.get_object("main_window")
        self.build_portfolio()
        self.build_transactions()
        """
        self.progress_bar = builder.get_object("progress_bar")
        self.header = builder.get_object("header")
        button = Gtk.Button()
        icon = Gio.ThemedIcon(name="mail-send-receive-symbolic")
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        button.add(image)
        self.header.pack_end(button)
        """
        self.window.show_all()

    def build_portfolio(self):
        store = Gtk.ListStore(str, str, float)
        store.append(["Datadog",
                         "DDOG", 70.05])
        portfolio_view = self.builder.get_object("portfolio_view")
        portfolio_view.set_model(store)

        renderer = Gtk.CellRendererText()
        italic_renderer = Gtk.CellRendererText(
            style=Pango.Style.ITALIC,
            alignment=Pango.Alignment.RIGHT,
        )
        columns = [
            Gtk.TreeViewColumn("Stock", renderer, text=0),
            Gtk.TreeViewColumn("Symbol", renderer, text=1),
            Gtk.TreeViewColumn("Price", italic_renderer, text=2),
        ]
        for col in columns:
            portfolio_view.append_column(col)

    def build_transactions(self):
        store = Gtk.ListStore(str, str, float)
        store.append(["The Art of Computer Programming",
                         "Donald E. Knuth", 25.46])
        transactions_view = self.builder.get_object("transactions_view")
        transactions_view.set_model(store)

        renderer = Gtk.CellRendererText()
        italic_renderer = Gtk.CellRendererText(
            style=Pango.Style.ITALIC,
            alignment=Pango.Alignment.RIGHT,
        )
        columns = [
            Gtk.TreeViewColumn("Title", renderer, text=0),
            Gtk.TreeViewColumn("Author", renderer, text=1),
            Gtk.TreeViewColumn("Price", italic_renderer, text=2),
        ]
        for col in columns:
            transactions_view.append_column(col)
        

    def on_destroy(self, *args):
        Gtk.main_quit()

    def on_button_clicked(self, button):
        #self.progress_bar.set_fraction(self.progress_bar.get_fraction() + 0.01)
        print("Hello World!")


if __name__ == "__main__":
    main = Main()
    Gtk.main()