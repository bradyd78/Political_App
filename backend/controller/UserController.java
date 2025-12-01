import org.springframework.web.bind.annotation.*;
import java.util.ArrayList;
import java.util.List;

@RestController
@RequestMapping("/api/users")
public class UserController {

    // In-memory "database"
    private List<User> users = new ArrayList<>();

    //Signup endpoint
    @PostMapping("/signup")
    public String signup(@RequestBody User newUser) {
        // Check if username already exists
        for (User u : users) {
            if (u.getUsername().equalsIgnoreCase(newUser.getUsername())) {
                return "User already exists";
            }
        }
        users.add(newUser);
        return "User created successfully";
    }

    //Login endpoint
    @PostMapping("/login")
    public String login(@RequestBody User loginUser) {
        for (User u : users) {
            if (u.getUsername().equalsIgnoreCase(loginUser.getUsername())
                    && u.getPassword().equals(loginUser.getPassword())) {
                return "Login successful";
            }
        }
        return "Invalid credentials";
    }

    //Get all users
    @GetMapping
    public List<User> getAllUsers() {
        return users;
    }
}

