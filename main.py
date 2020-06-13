import gi
import os

import pandas as pd

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gio, Pango

from lib.io import Importer
from lib.portfolio import Portfolio

STORE_FILE = "data.csv"


class Main(object):
    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file("main.glade")
        self.builder.connect_signals(self)
        self.main_box = self.builder.get_object("main_box")
        self.window = self.builder.get_object("main_window")
        self.add_dialog = self.builder.get_object("add_dialog")
        self.main_menu = self.builder.get_object("main_menu")
        self.menu_button = self.builder.get_object("menu_button")
        self.header = self.builder.get_object("header")
        self.portfolio_view = self.builder.get_object("portfolio_view")
        self.transactions_view = self.builder.get_object("transactions_view")
        self.transactions_store = self.builder.get_object("transactions_store")
        self.portfolio_store = self.builder.get_object("portfolio_store")
        self._transactions_df = pd.DataFrame()
        if os.path.isfile(STORE_FILE):
            self.load_csv()
        self.main_menu.show_all()
        self.window.show_all()

    @property
    def transactions_df(self):
        if self._transactions_df.empty:
            self._transactions_df = pd.read_csv(STORE_FILE)
        return self._transactions_df

    @transactions_df.setter
    def transactions_df(self, dataframe):
        self._transactions_df = dataframe
        dataframe.to_csv(STORE_FILE)

    def on_destroy(self, *args):
        Gtk.main_quit()

    def on_calculate_clicked(self, button):
        print("1 mil!")

    def on_add_clicked(self, button):
        #self.progress_bar.set_fraction(self.progress_bar.get_fraction() + 0.01)
        self.add_dialog.run()

    def on_cancel_clicked(self, button, *args):
        self.add_dialog.hide()

    def on_add_transaction_clicked(self, button):
        product_name = self.builder.get_object("add_product_name").get_text()
        isin = self.builder.get_object("add_isin").get_text()
        price = int(self.builder.get_object("add_price").get_text())
        number_of_items = int(self.builder.get_object("add_number_of_items").get_text())
        date_time = pd.to_datetime(
            self.builder.get_object("add_date_time").get_text(),
            infer_datetime_format=True
        )
        self.transactions_df = self.transactions_df.append(
            {
                "Date_Time": date_time,
                "Product": product_name,
                "ISIN": isin,
                "Price": price,
                "Number": number_of_items,
                "Exchange": "NYSE",  # placeholders
                "Local value": price * number_of_items,
                "Value": price * number_of_items,
                "Fee": 0,
                "Total": price * number_of_items,
            }, ignore_index=True)
        self.load_csv()
        self.add_dialog.hide()

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

    def load_csv(self, filename=None):
        if filename:
            csv_importer = Importer(filename)
            self.transactions_df = csv_importer.import_csv()
        portfolio = Portfolio(self.transactions_df)
        portfolio_data = portfolio.plain_view()
        self.populate(
            self.transactions_view,
            self.transactions_df,
            self.transactions_store,
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
            self.portfolio_store
        )

    def populate(self, view, data, store, cols=None):
        """Populates given view with the data"""
        # TODO convert stores to properties to properly update
        if cols:
            data = data[cols]
        rows = (row for _, row in data.iterrows())
        store.clear()
        for row in rows:
            row[0] = str(row[0])  # convert datetime to str
            store.append(list(row))
        view.set_model(store)
        renderer = Gtk.CellRendererText()
        for index, column in enumerate(data.columns):
            view.append_column(
                Gtk.TreeViewColumn(column, renderer, text=index),
            )


if __name__ == "__main__":
    main = Main()
    Gtk.main()