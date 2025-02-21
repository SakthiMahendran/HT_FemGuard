import 'package:flutter/material.dart';
import 'package:local_auth/local_auth.dart';
import 'package:shared_preferences/shared_preferences.dart';

class LoginScreen extends StatefulWidget {
  const LoginScreen({Key? key}) : super(key: key);

  @override
  _LoginScreenState createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final _formKey = GlobalKey<FormState>();
  final TextEditingController _userIdController = TextEditingController();
  final TextEditingController _passwordController = TextEditingController();
  final LocalAuthentication auth = LocalAuthentication();

  bool _isLoading = false;
  bool _canUseBiometrics = false;
  bool _fingerprintLoginEnabled = false;

  @override
  void initState() {
    super.initState();
    _checkBiometricAvailability();
    _loadFingerprintPreference();
  }

  /// Check if the device supports biometrics
  Future<void> _checkBiometricAvailability() async {
    try {
      bool canCheckBiometrics = await auth.canCheckBiometrics;
      List<BiometricType> availableBiometrics = await auth.getAvailableBiometrics();

      setState(() {
        _canUseBiometrics = canCheckBiometrics && availableBiometrics.isNotEmpty;
      });
    } catch (e) {
      setState(() {
        _canUseBiometrics = false;
      });
    }
  }

  /// Load user's fingerprint login preference
  Future<void> _loadFingerprintPreference() async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    setState(() {
      _fingerprintLoginEnabled = prefs.getBool('fingerprintLoginEnabled') ?? false;
    });
  }

  /// For development: bypass the login checks entirely
  Future<void> _devBypassLogin() async {
    setState(() {
      _isLoading = true;
    });

    // Simulate a brief delay to show a loading indicator (optional)
    await Future.delayed(const Duration(milliseconds: 500));

    setState(() {
      _isLoading = false;
    });

    // Directly navigate to '/home' without any authentication
    Navigator.pushReplacementNamed(context, '/home');
  }

  /// Handle fingerprint login
  Future<void> _loginWithFingerprint() async {
    try {
      bool didAuthenticate = await auth.authenticate(
        localizedReason: 'Authenticate to login to FemGuard',
        options: const AuthenticationOptions(
          stickyAuth: true,
          useErrorDialogs: true,
          biometricOnly: true,
        ),
      );

      if (didAuthenticate) {
        // Navigate to home screen after fingerprint auth success
        Navigator.pushReplacementNamed(context, '/home');
      }
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Fingerprint authentication failed: $e')),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(24.0),
          child: Form(
            key: _formKey,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const SizedBox(height: 60),
                Center(
                  child: Text(
                    'FemGuard Login (Dev Bypass)',
                    style: Theme.of(context).textTheme.headlineSmall?.copyWith(
                          fontWeight: FontWeight.bold,
                        ),
                  ),
                ),
                const SizedBox(height: 40),
                TextFormField(
                  controller: _userIdController,
                  decoration: const InputDecoration(
                    labelText: 'User ID',
                    prefixIcon: Icon(Icons.person),
                    border: OutlineInputBorder(),
                  ),
                ),
                const SizedBox(height: 20),
                TextFormField(
                  controller: _passwordController,
                  decoration: const InputDecoration(
                    labelText: 'Password',
                    prefixIcon: Icon(Icons.lock),
                    border: OutlineInputBorder(),
                  ),
                  obscureText: true,
                ),
                const SizedBox(height: 30),

                // Dev Bypass Login Button
                SizedBox(
                  width: double.infinity,
                  height: 50,
                  child: ElevatedButton(
                    onPressed: _isLoading ? null : _devBypassLogin,
                    child: _isLoading
                        ? const CircularProgressIndicator(
                            valueColor: AlwaysStoppedAnimation<Color>(Colors.white),
                          )
                        : const Text('Dev Bypass Login'),
                  ),
                ),
                const SizedBox(height: 20),

                // Show "Login with Fingerprint" only if biometrics are supported & enabled
                if (_canUseBiometrics && _fingerprintLoginEnabled)
                  SizedBox(
                    width: double.infinity,
                    height: 50,
                    child: OutlinedButton.icon(
                      icon: const Icon(Icons.fingerprint),
                      label: const Text('Login with Fingerprint'),
                      onPressed: _loginWithFingerprint,
                    ),
                  ),

                const SizedBox(height: 20),
                Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    const Text("Don't have an account?"),
                    TextButton(
                      onPressed: () {
                        Navigator.pushNamed(context, '/register');
                      },
                      child: const Text('Register'),
                    ),
                  ],
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
