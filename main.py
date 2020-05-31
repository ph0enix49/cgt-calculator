import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gio, Pango

from lib.io import Importer
from lib.portfolio import Portfolio


class Main(object):
    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file("main.glade")
        self.builder.connect_signals(self)
        self.main_box = self.builder.get_object("main_box")
        self.window = self.builder.get_object("main_window")
        self.main_menu = self.builder.get_object("main_menu")
        self.menu_button = self.builder.get_object("menu_button")
        self.header = self.builder.get_object("header")
        test_menu = Gtk.MenuItem(label="lp")
        self.main_menu.append(test_menu)
        self.portfolio_view = self.builder.get_object("portfolio_view")
        self.transactions_view = self.builder.get_object("transactions_view")
        self.main_menu.show_all()
        self.window.show_all()

    def on_destroy(self, *args):
        Gtk.main_quit()

    def on_button_clicked(self, button):
        #self.progress_bar.set_fraction(self.progress_bar.get_fraction() + 0.01)
        print("Hello World!")
    
    def on_import_clicked(self, button):
        dialog = Gtk.FileChooserDialog(
            title="Please choose a file",
            parent=self.window,
            action=Gtk.FileChooserAction.OPEN,
        )
        dialog.add_buttons(
            Gtk.STOCK_CANCEL,
            Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OPEN,
            Gtk.ResponseType.OK
        )
        filter_text = Gtk.FileFilter()
        filter_text.set_name("CSV files")
        filter_text.add_mime_type("text/csv")
        dialog.add_filter(filter_text)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            csv_file = dialog.get_filename()
            self.load_csv(csv_file)
        dialog.hide()

    def load_csv(self, filename):
        csv_importer = Importer(filename)
        transations_data = csv_importer.import_csv()
        portfolio = Portfolio(transations_data)
        portfolio_data = portfolio.plain_view()
        self.populate(
            self.transactions_view,
            transations_data,
            [
                "Date_Time",  # move to settings
                "Product",
                "Exchange",
                "Number",
                "Price",
                "Local value",
                "Value",
                "Exchange rate",
                "Fee",
                "Total",
            ]
            )
        self.populate(
            self.portfolio_view,
            portfolio_data,
        )

    def populate(self, view, data, cols=None):
        """Populates given view with the data"""
        if cols:
            data = data[cols]
        # create a store
        store = Gtk.ListStore(*([str] * len(data.columns)))
        for row in data.values:
            converted = [str(x) for x in row]
            store.append(converted)
        view.set_model(store)
        renderer = Gtk.CellRendererText()
        for index, column in enumerate(data.columns):
            view.append_column(
                Gtk.TreeViewColumn(column, renderer, text=index),
            )

if __name__ == "__main__":
    main = Main()
    Gtk.main()