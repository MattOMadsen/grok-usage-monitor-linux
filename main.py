#!/usr/bin/env python3
"""
Grok Usage Monitor - System tray app for Zorin OS / Ubuntu
Shows Grok usage (Build / API / Chat) in the top panel.

Features:
- Live menu with progress
- Settings dialog for manual values (persisted)
- Auto-refresh every 5 min
- Color-aware icon

Code reviewed and improved by Grok.
"""

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
from gi.repository import Gtk, AppIndicator3, GLib
import json
import os
from pathlib import Path

CONFIG_DIR = Path.home() / ".config" / "grok-usage-monitor"
CONFIG_FILE = CONFIG_DIR / "config.json"


def load_config():
    """Load usage data from config or return demo data."""
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                # Basic validation
                if "overall_used" in data and "categories" in data:
                    return data
        except Exception as e:
            print(f"Config load error: {e}")
    
    # Default demo data
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


def save_config(data):
    """Save usage data to config file."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Config save error: {e}")


class GrokUsageMonitor:
    def __init__(self):
        self.app_name = "grok-usage-monitor"
        self.indicator = AppIndicator3.Indicator.new(
            self.app_name,
            self._get_icon_for_usage(38),  # initial
            AppIndicator3.IndicatorCategory.APPLICATION_STATUS
        )
        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        
        self.usage_data = load_config()
        self._update_icon()
        self.build_menu()
        
        # Auto-refresh every 5 minutes
        GLib.timeout_add_seconds(300, self.refresh_data)

    def _get_icon_for_usage(self, percent):
        """Return appropriate icon based on usage level."""
        if percent >= 80:
            return "dialog-warning"      # High usage - warning
        elif percent >= 50:
            return "dialog-information"  # Medium
        else:
            return "emblem-ok"          # Low / good

    def _update_icon(self):
        icon = self._get_icon_for_usage(self.usage_data.get("overall_used", 0))
        self.indicator.set_icon(icon)

    def get_usage_data(self):
        # Always return current in-memory data (updated via settings or refresh)
        return self.usage_data

    def build_menu(self):
        menu = Gtk.Menu()

        used = self.usage_data["overall_used"]
        remaining = self.usage_data.get("overall_remaining", 100 - used)

        header = Gtk.MenuItem(label=f"Weekly SuperGrok Limit - {used}% used")
        header.set_sensitive(False)
        menu.append(header)

        bar = "█" * (used // 5) + "░" * (20 - used // 5)
        progress = Gtk.MenuItem(
            label=f"{bar}  {used}% used • {remaining}% remaining"
        )
        progress.set_sensitive(False)
        menu.append(progress)

        menu.append(Gtk.SeparatorMenuItem())

        for cat, data in self.usage_data["categories"].items():
            item = Gtk.MenuItem(label=f"{cat}: {data['percent']}%")
            item.set_sensitive(False)
            menu.append(item)

        menu.append(Gtk.SeparatorMenuItem())

        reset = Gtk.MenuItem(label=f"Resets: {self.usage_data.get('reset_date', 'N/A')}")
        reset.set_sensitive(False)
        menu.append(reset)

        menu.append(Gtk.SeparatorMenuItem())

        # Refresh
        refresh = Gtk.MenuItem(label="Refresh Now")
        refresh.connect("activate", self.on_refresh)
        menu.append(refresh)

        # Settings (NEW)
        settings = Gtk.MenuItem(label="Settings...")
        settings.connect("activate", self.show_settings)
        menu.append(settings)

        # Detailed view
        details = Gtk.MenuItem(label="Open Detailed View")
        details.connect("activate", self.show_detailed_view)
        menu.append(details)

        # About
        about = Gtk.MenuItem(label="About")
        about.connect("activate", self.show_about)
        menu.append(about)

        quit_item = Gtk.MenuItem(label="Quit Grok Usage")
        quit_item.connect("activate", self.quit)
        menu.append(quit_item)

        menu.show_all()
        self.indicator.set_menu(menu)

    def on_refresh(self, widget=None):
        # In future: fetch real data here
        # For now just rebuild with current data
        self._update_icon()
        self.build_menu()

    def show_settings(self, widget):
        """Open settings dialog to manually edit values."""
        win = Gtk.Dialog(title="Grok Usage Monitor - Settings", transient_for=None)
        win.set_default_size(420, 380)
        win.add_button("Cancel", Gtk.ResponseType.CANCEL)
        win.add_button("Save", Gtk.ResponseType.OK)

        content = win.get_content_area()
        content.set_border_width(15)
        content.set_spacing(10)

        # Overall
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        box.pack_start(Gtk.Label(label="Overall used %:"), False, False, 0)
        overall_entry = Gtk.Entry()
        overall_entry.set_text(str(self.usage_data.get("overall_used", 38)))
        box.pack_start(overall_entry, True, True, 0)
        content.pack_start(box, False, False, 5)

        # Categories
        for cat in ["Grok Build", "API", "Chat"]:
            hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
            hbox.pack_start(Gtk.Label(label=f"{cat} %:"), False, False, 0)
            entry = Gtk.Entry()
            entry.set_text(str(self.usage_data["categories"].get(cat, {}).get("percent", 0)))
            entry.set_name(cat)  # store category name
            hbox.pack_start(entry, True, True, 0)
            content.pack_start(hbox, False, False, 5)

        # Reset date
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hbox.pack_start(Gtk.Label(label="Reset date:"), False, False, 0)
        reset_entry = Gtk.Entry()
        reset_entry.set_text(self.usage_data.get("reset_date", ""))
        hbox.pack_start(reset_entry, True, True, 0)
        content.pack_start(hbox, False, False, 10)

        win.show_all()

        response = win.run()
        if response == Gtk.ResponseType.OK:
            try:
                new_data = self.usage_data.copy()
                new_data["overall_used"] = int(overall_entry.get_text())
                new_data["overall_remaining"] = 100 - new_data["overall_used"]

                for child in content.get_children():
                    if isinstance(child, Gtk.Box):
                        for sub in child.get_children():
                            if isinstance(sub, Gtk.Entry) and sub.get_name() in new_data["categories"]:
                                cat = sub.get_name()
                                new_data["categories"][cat]["percent"] = int(sub.get_text())

                new_data["reset_date"] = reset_entry.get_text()

                self.usage_data = new_data
                save_config(self.usage_data)
                self._update_icon()
                self.build_menu()
            except ValueError:
                # Simple error dialog
                err = Gtk.MessageDialog(win, 0, Gtk.MessageType.ERROR,
                                        Gtk.ButtonsType.OK, "Please enter valid numbers!")
                err.run()
                err.destroy()

        win.destroy()

    def show_detailed_view(self, widget):
        win = Gtk.Window(title="Grok Usage - Detailed View")
        win.set_default_size(480, 380)
        win.set_border_width(15)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        win.add(vbox)

        used = self.usage_data["overall_used"]
        remaining = self.usage_data.get("overall_remaining", 100 - used)

        label = Gtk.Label()
        label.set_markup(f"<b>Weekly SuperGrok Heavy Limit</b>\n"
                         f"{used}% used • {remaining}% remaining")
        vbox.pack_start(label, False, False, 0)

        # Daily graph
        graph_label = Gtk.Label()
        graph_text = "<b>Daily use (% of weekly)</b>\n\n"
        for day, values in self.usage_data.get("daily", {}).items():
            total = sum(values.values())
            bar = "█" * (total // 3) + "░" * (10 - total // 3)
            graph_text += f"{day}: {bar} {total}%\n"
        graph_label.set_markup(graph_text)
        graph_label.set_xalign(0.0)
        vbox.pack_start(graph_label, True, True, 0)

        win.show_all()

    def show_about(self, widget):
        about = Gtk.AboutDialog()
        about.set_program_name("Grok Usage Monitor")
        about.set_version("1.1")
        about.set_comments("System tray app for monitoring Grok usage on Linux.\n\n"
                           "Made with Grok • Code reviewed & improved")
        about.set_website("https://github.com/MattOMadsen/grok-usage-monitor-linux")
        about.set_website_label("GitHub Repo")
        about.set_license_type(Gtk.License.MIT_X11)
        about.run()
        about.destroy()

    def refresh_data(self):
        self._update_icon()
        self.build_menu()
        return True

    def quit(self, widget):
        Gtk.main_quit()


if __name__ == "__main__":
    monitor = GrokUsageMonitor()
    Gtk.main()
