
public class LoginService {
    private SignupService signupService;

    public LoginService(SignupService signupService) {
        this.signupService = signupService;
    }

    public boolean login(String username, String password) {
        User user = signupService.getUserDatabase().get(username);
        if (user != null && user.getPassword().equals(password)) {
            System.out.println("Login successful for user: " + username);
            return true;
        }
        System.out.println("Invalid username or password!");
        return false;
    }
}
