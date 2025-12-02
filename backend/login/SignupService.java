
import java.util.HashMap;
import java.util.Map;

public class SignupService {
    // Simulating a database with a HashMap
    private Map<String, User> userDatabase = new HashMap<>();

    public boolean signup(String username, String password) {
        if (userDatabase.containsKey(username)) {
            System.out.println("Username already exists!");
            return false;
        }
        User newUser = new User(username, password);
        userDatabase.put(username, newUser);
        System.out.println("Signup successful for user: " + username);
        return true;
    }

    public Map<String, User> getUserDatabase() {
        return userDatabase;
    }
}
