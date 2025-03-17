import 'package:flutter/material.dart';

class RegisterScreen extends StatefulWidget {
  const RegisterScreen({Key? key}) : super(key: key);

  @override
  _RegisterScreenState createState() => _RegisterScreenState();
}

class _RegisterScreenState extends State<RegisterScreen> {
  final _formKey = GlobalKey<FormState>();

  // Controllers for each field:
  final TextEditingController _nameController = TextEditingController();
  final TextEditingController _dobController = TextEditingController();
  final TextEditingController _aadhaarController = TextEditingController();
  final TextEditingController _phoneController = TextEditingController();
  final TextEditingController _addressController = TextEditingController();
  final TextEditingController _emailController = TextEditingController();
  final TextEditingController _emergencyContactController = TextEditingController();
  final TextEditingController _workingStatusController = TextEditingController();
  final TextEditingController _companySchoolController = TextEditingController();
  final TextEditingController _bloodGroupController = TextEditingController();
  final TextEditingController _medicalIssuesController = TextEditingController();

  final TextEditingController _userIdController = TextEditingController();
  final TextEditingController _passwordController = TextEditingController();

  bool _isLoading = false;
  bool _agreedToConfirmInfo = false; // For the checkbox

  Future<void> _register() async {
    // First, validate the form
    if (!_formKey.currentState!.validate()) {
      return;
    }

    // Check if the user checked the "confirm info" box
    if (!_agreedToConfirmInfo) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Please confirm that all information is correct.')),
      );
      return;
    }

    // Now proceed with registration
    setState(() {
      _isLoading = true;
    });

    // Simulate a backend call
    await Future.delayed(const Duration(seconds: 2));

    setState(() {
      _isLoading = false;
    });

    // On success, navigate back to login (or do auto-login)
    Navigator.pushReplacementNamed(context, '/login');
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
              children: [
                const SizedBox(height: 40),
                Text(
                  'Register on FemGuard',
                  style: Theme.of(context).textTheme.headlineSmall?.copyWith(
                        fontWeight: FontWeight.bold,
                      ),
                ),
                const SizedBox(height: 30),

                // Name
                TextFormField(
                  controller: _nameController,
                  decoration: const InputDecoration(
                    labelText: 'Name',
                    prefixIcon: Icon(Icons.person),
                    border: OutlineInputBorder(),
                  ),
                  validator: (value) {
                    if (value == null || value.isEmpty) {
                      return 'Please enter your Name';
                    }
                    return null;
                  },
                ),
                const SizedBox(height: 20),

                // Date of Birth
                TextFormField(
                  controller: _dobController,
                  decoration: const InputDecoration(
                    labelText: 'Date of Birth (DD/MM/YYYY)',
                    prefixIcon: Icon(Icons.calendar_today),
                    border: OutlineInputBorder(),
                  ),
                  validator: (value) {
                    if (value == null || value.isEmpty) {
                      return 'Please enter your Date of Birth';
                    }
                    return null;
                  },
                ),
                const SizedBox(height: 20),

                // Aadhaar
                TextFormField(
                  controller: _aadhaarController,
                  decoration: const InputDecoration(
                    labelText: 'Aadhaar ID',
                    prefixIcon: Icon(Icons.fingerprint),
                    border: OutlineInputBorder(),
                  ),
                  keyboardType: TextInputType.number,
                  validator: (value) {
                    if (value == null || value.isEmpty) {
                      return 'Please enter your Aadhaar ID';
                    }
                    // Optionally check length == 12
                    return null;
                  },
                ),
                const SizedBox(height: 20),

                // Phone
                TextFormField(
                  controller: _phoneController,
                  decoration: const InputDecoration(
                    labelText: 'Phone Number',
                    prefixIcon: Icon(Icons.phone),
                    border: OutlineInputBorder(),
                  ),
                  keyboardType: TextInputType.phone,
                  validator: (value) {
                    if (value == null || value.isEmpty) {
                      return 'Please enter your Phone Number';
                    }
                    return null;
                  },
                ),
                const SizedBox(height: 20),

                // Residential Address
                TextFormField(
                  controller: _addressController,
                  decoration: const InputDecoration(
                    labelText: 'Residential Address',
                    prefixIcon: Icon(Icons.home),
                    border: OutlineInputBorder(),
                  ),
                  maxLines: 2,
                  validator: (value) {
                    if (value == null || value.isEmpty) {
                      return 'Please enter your Residential Address';
                    }
                    return null;
                  },
                ),
                const SizedBox(height: 20),

                // Email
                TextFormField(
                  controller: _emailController,
                  decoration: const InputDecoration(
                    labelText: 'Email',
                    prefixIcon: Icon(Icons.email),
                    border: OutlineInputBorder(),
                  ),
                  keyboardType: TextInputType.emailAddress,
                  validator: (value) {
                    if (value == null || value.isEmpty) {
                      return 'Please enter your Email';
                    }
                    // Basic check
                    if (!value.contains('@')) {
                      return 'Please enter a valid Email';
                    }
                    return null;
                  },
                ),
                const SizedBox(height: 20),

                // Emergency Contact
                TextFormField(
                  controller: _emergencyContactController,
                  decoration: const InputDecoration(
                    labelText: 'Emergency Contact Number',
                    prefixIcon: Icon(Icons.contact_phone),
                    border: OutlineInputBorder(),
                  ),
                  keyboardType: TextInputType.phone,
                  validator: (value) {
                    if (value == null || value.isEmpty) {
                      return 'Please enter your Emergency Contact Number';
                    }
                    return null;
                  },
                ),
                const SizedBox(height: 20),

                // Working status
                TextFormField(
                  controller: _workingStatusController,
                  decoration: const InputDecoration(
                    labelText: 'Working Status (Student/Working)',
                    prefixIcon: Icon(Icons.work),
                    border: OutlineInputBorder(),
                  ),
                ),
                const SizedBox(height: 20),

                // Company / School
                TextFormField(
                  controller: _companySchoolController,
                  decoration: const InputDecoration(
                    labelText: 'Company/School Name',
                    prefixIcon: Icon(Icons.location_city),
                    border: OutlineInputBorder(),
                  ),
                ),
                const SizedBox(height: 20),

                // Blood Group
                TextFormField(
                  controller: _bloodGroupController,
                  decoration: const InputDecoration(
                    labelText: 'Blood Group',
                    prefixIcon: Icon(Icons.bloodtype),
                    border: OutlineInputBorder(),
                  ),
                ),
                const SizedBox(height: 20),

                // Medical issues
                TextFormField(
                  controller: _medicalIssuesController,
                  decoration: const InputDecoration(
                    labelText: 'Medical Issues (if any)',
                    prefixIcon: Icon(Icons.local_hospital),
                    border: OutlineInputBorder(),
                  ),
                ),
                const SizedBox(height: 20),

                // User ID
                TextFormField(
                  controller: _userIdController,
                  decoration: const InputDecoration(
                    labelText: 'User ID',
                    prefixIcon: Icon(Icons.person_outline),
                    border: OutlineInputBorder(),
                  ),
                  validator: (value) {
                    if (value == null || value.isEmpty) {
                      return 'Please enter a User ID';
                    }
                    return null;
                  },
                ),
                const SizedBox(height: 20),

                // Password
                TextFormField(
                  controller: _passwordController,
                  decoration: const InputDecoration(
                    labelText: 'Password',
                    prefixIcon: Icon(Icons.lock_outline),
                    border: OutlineInputBorder(),
                  ),
                  obscureText: true,
                  validator: (value) {
                    if (value == null || value.isEmpty) {
                      return 'Please enter a Password';
                    }
                    if (value.length < 6) {
                      return 'Password should be at least 6 characters long';
                    }
                    return null;
                  },
                ),
                const SizedBox(height: 20),

                // "I confirm" checkbox
                CheckboxListTile(
                  title: const Text(
                    'I confirm all information provided is true to the best of my knowledge.',
                  ),
                  value: _agreedToConfirmInfo,
                  onChanged: (bool? value) {
                    setState(() {
                      _agreedToConfirmInfo = value ?? false;
                    });
                  },
                  controlAffinity: ListTileControlAffinity.leading,
                ),
                const SizedBox(height: 20),

                // "Confirm details and submit" button
                SizedBox(
                  width: double.infinity,
                  height: 50,
                  child: ElevatedButton(
                    onPressed: _isLoading ? null : _register,
                    child: _isLoading
                        ? const CircularProgressIndicator(
                            valueColor: AlwaysStoppedAnimation<Color>(Colors.white),
                          )
                        : const Text('Confirm Details and Submit'),
                  ),
                ),
                const SizedBox(height: 20),

                // Back to Login
                Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    const Text('Already have an account?'),
                    TextButton(
                      onPressed: () {
                        Navigator.pushReplacementNamed(context, '/login');
                      },
                      child: const Text('Login'),
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
