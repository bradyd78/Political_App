public class SettingsController {
    private Settings settings;

    // Initialize with default settings
    public SettingsController() {
        this.settings = new Settings("Light", true, "en");
    }

    // Update theme
    public void updateTheme(String theme) {
        settings.setTheme(theme);
        System.out.println("Theme updated to: " + theme);
    }

    // Toggle notifications
    public void toggleNotifications() {
        boolean current = settings.isNotificationsEnabled();
        settings.setNotificationsEnabled(!current);
        System.out.println("Notifications are now: " + (settings.isNotificationsEnabled() ? "Enabled" : "Disabled"));
    }

    // Change language
    public void changeLanguage(String language) {
        settings.setLanguage(language);
        System.out.println("Language changed to: " + language);
    }

    // Display current settings
    public void displaySettings() {
        System.out.println(settings);
    }
}
