#!/usr/bin/env python3
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
from gi.repository import Gtk, AppIndicator3, GLib
import sys

class GrokUsageMonitor:
    def __init__(self):
        self.app_name = "grok-usage-monitor"
        self.indicator = AppIndicator3.Indicator.new(
            self.app_name,
            "dialog-information",  # TODO: bedre ikon senere
            AppIndicator3.IndicatorCategory.APPLICATION_STATUS
        )
        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        
        self.usage_data = self.get_usage_data()
        self.build_menu()
        
        # Auto-refresh hvert 5. minut
        GLib.timeout_add_seconds(300, self.refresh_data)

    def get_usage_data(self):
        # Demo-data – udskift denne funktion med rigtig data senere
        return {
            "overall_used": 38,
            "overall_remaining": 62,
            "reset_date": "Jul 16, 2026 at 2:25 PM",
            "categories": {
                "Grok Build": {"percent": 28},
                "API": {"percent": 9},
                "Chat": {"percent": 1}
            },
            "daily": {
                "Sun": {"Grok Build": 0, "API": 0, "Chat": 0},
                "Mon": {"Grok Build": 5, "API": 2, "Chat": 0},
                "Tue": {"Grok Build": 12, "API": 3, "Chat": 1},
                "Wed": {"Grok Build": 8, "API": 4, "Chat": 0},
                "Thu": {"Grok Build": 15, "API": 5, "Chat": 2},
                "Fri": {"Grok Build": 21, "API": 3, "Chat": 1},
                "Sat": {"Grok Build": 3, "API": 1, "Chat": 0}
            }
        }

    def build_menu(self):
        menu = Gtk.Menu()

        header = Gtk.MenuItem(label=f"Weekly SuperGrok Limit - {self.usage_data['overall_used']}% used")
        header.set_sensitive(False)
        menu.append(header)

        progress = Gtk.MenuItem(
            label=f"{'\u2588' * (self.usage_data['overall_used'] // 5)}{'\u2591' * (20 - self.usage_data['overall_used'] // 5)} "
                  f"{self.usage_data['overall_used']}% used • {self.usage_data['overall_remaining']}% remaining"
        )
        progress.set_sensitive(False)
        menu.append(progress)

        menu.append(Gtk.SeparatorMenuItem())

        for cat, data in self.usage_data["categories"].items():
            item = Gtk.MenuItem(label=f"{cat}: {data['percent']}%")
            item.set_sensitive(False)
            menu.append(item)

        menu.append(Gtk.SeparatorMenuItem())

        reset = Gtk.MenuItem(label=f"Resets: {self.usage_data['reset_date']}")
        reset.set_sensitive(False)
        menu.append(reset)

        menu.append(Gtk.SeparatorMenuItem())

        refresh = Gtk.MenuItem(label="Refresh Now")
        refresh.connect("activate", self.on_refresh)
        menu.append(refresh)

        details = Gtk.MenuItem(label="Open Detailed View")
        details.connect("activate", self.show_detailed_view)
        menu.append(details)

        quit_item = Gtk.MenuItem(label="Quit Grok Usage")
        quit_item.connect("activate", self.quit)
        menu.append(quit_item)

        menu.show_all()
        self.indicator.set_menu(menu)

    def on_refresh(self, widget):
        self.usage_data = self.get_usage_data()
        self.build_menu()

    def show_detailed_view(self, widget):
        win = Gtk.Window(title="Grok Usage - Detailed View")
        win.set_default_size(450, 350)
        win.set_border_width(15)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        win.add(vbox)

        label = Gtk.Label()
        label.set_markup(f"<b>Weekly SuperGrok Heavy Limit</b>\n"
                         f"{self.usage_data['overall_used']}% used • {self.usage_data['overall_remaining']}% remaining")
        vbox.pack_start(label, False, False, 0)

        graph_label = Gtk.Label()
        graph_text = "Daily use (% of weekly)\n\n"
        for day, values in self.usage_data["daily"].items():
            total = sum(values.values())
            bar = "\u2588" * (total // 3) + "\u2591" * (10 - total // 3)
            graph_text += f"{day}: {bar} {total}%\n"
        graph_label.set_text(graph_text)
        graph_label.set_xalign(0.0)
        vbox.pack_start(graph_label, True, True, 0)

        win.show_all()

    def refresh_data(self):
        self.usage_data = self.get_usage_data()
        self.build_menu()
        return True  # Fortsæt timeren

    def quit(self, widget):
        Gtk.main_quit()

if __name__ == "__main__":
    monitor = GrokUsageMonitor()
    Gtk.main()
