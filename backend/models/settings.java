public class Settings {
    private String theme;          // e.g., "Light" or "Dark"
    private boolean notificationsEnabled;
    private String language;       // e.g., "en", "es"

    // Constructor
    public Settings(String theme, boolean notificationsEnabled, String language) {
        this.theme = theme;
        this.notificationsEnabled = notificationsEnabled;
        this.language = language;
    }

    // Getters and Setters
    public String getTheme() {
        return theme;
    }

    public void setTheme(String theme) {
        this.theme = theme;
    }

    public boolean isNotificationsEnabled() {
        return notificationsEnabled;
    }

    public void setNotificationsEnabled(boolean notificationsEnabled) {
        this.notificationsEnabled = notificationsEnabled;
    }

    public String getLanguage() {
        return language;
    }

    public void setLanguage(String language) {
        this.language = language;
    }

    @Override
    public String toString() {
        return "Settings {" +
                "theme='" + theme + '\'' +
                ", notificationsEnabled=" + notificationsEnabled +
                ", language='" + language + '\'' +
                '}';
    }
}
