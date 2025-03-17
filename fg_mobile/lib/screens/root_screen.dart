import 'package:flutter/material.dart';
import 'home_screen.dart';
import 'register_screen.dart';
import 'complaint_screen.dart';
import 'map_screen.dart';
import 'chatbot_screen.dart';

class RootScreen extends StatefulWidget {
  const RootScreen({Key? key}) : super(key: key);

  @override
  _RootScreenState createState() => _RootScreenState();
}

class _RootScreenState extends State<RootScreen> {
  int _selectedIndex = 0;

  // This would come from secure storage or SharedPreferences in a real app
  bool _fingerprintEnabled = false;

  // List of pages for the bottom nav bar
  final List<Widget> _screens = const [
    HomeScreen(),
    RegisterScreen(),
    ComplaintScreen(),
    MapScreen(),
    ChatbotScreen(),
  ];

  void _onItemTapped(int index) {
    setState(() {
      _selectedIndex = index;
    });
  }

  void _toggleFingerprintLogin() {
    setState(() {
      _fingerprintEnabled = !_fingerprintEnabled;
    });

    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(_fingerprintEnabled
            ? 'Fingerprint login enabled'
            : 'Fingerprint login disabled'),
      ),
    );

    // In a real app, store this in SharedPreferences or a similar
    // persistent store, so that on the next login,
    // your LoginScreen knows to show "Login with Fingerprint".
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('FemGuard'),
        actions: [
          PopupMenuButton<String>(
            onSelected: (String value) {
              if (value == 'fingerprint') {
                _toggleFingerprintLogin();
              }
              // You could add more items: e.g., 'profile', 'logout', etc.
            },
            itemBuilder: (BuildContext context) {
              return [
                PopupMenuItem<String>(
                  value: 'fingerprint',
                  child: Row(
                    children: [
                      const Icon(Icons.fingerprint, color: Colors.black54),
                      const SizedBox(width: 10),
                      Text(_fingerprintEnabled
                          ? 'Disable Fingerprint Login'
                          : 'Enable Fingerprint Login'),
                    ],
                  ),
                ),
              ];
            },
            icon: const Icon(Icons.person), // Profile icon
          ),
        ],
      ),
      body: _screens[_selectedIndex],
      bottomNavigationBar: BottomNavigationBar(
        type: BottomNavigationBarType.fixed,
        currentIndex: _selectedIndex,
        onTap: _onItemTapped,
        items: const [
          BottomNavigationBarItem(
            icon: Icon(Icons.home),
            label: 'Home',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.app_registration),
            label: 'Register',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.assignment),
            label: 'Complaint',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.map),
            label: 'Map',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.chat),
            label: 'Chatbot',
          ),
        ],
      ),
    );
  }
}
