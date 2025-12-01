public class User {
    private String username;
    private String password;

    //No-args constructor
    public User() {
    }

    //constructor
    public User(String username, String password) {
        this.username = username;
        this.password = password;
    }

    //Getters and Setters
    public String getUsername() {
        return username;
    }

    public void setUsername(String username) {
        this.username = username;
    }

    public String getPassword() {
        return password;
    }

    //never expose raw passwords in real apps
    public void setPassword(String password) {
        this.password = password;
    }

    @Override
    public String toString() {
        return "User {" +
                "username='" + username + '\'' +
                ", password='[PROTECTED]'}";
    }
}

