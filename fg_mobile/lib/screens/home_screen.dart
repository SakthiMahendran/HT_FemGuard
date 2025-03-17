import 'package:flutter/material.dart';

class HomeScreen extends StatelessWidget {
  const HomeScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('FemGuard Home'),
      ),
      body: Center(
        child: Text(
          'Welcome to FemGuard!',
          style: Theme.of(context).textTheme.headlineSmall,
        ),
      ),
    );
  }
}
