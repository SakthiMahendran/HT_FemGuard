import 'package:flutter/material.dart';

class ComplaintScreen extends StatelessWidget {
  const ComplaintScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Text(
        'Complaint Portal',
        style: Theme.of(context).textTheme.headlineSmall,
      ),
    );
  }
}
