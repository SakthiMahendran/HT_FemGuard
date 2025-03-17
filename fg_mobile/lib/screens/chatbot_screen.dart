import 'package:flutter/material.dart';

class ChatbotScreen extends StatelessWidget {
  const ChatbotScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Text(
        'Chatbot Screen',
        style: Theme.of(context).textTheme.headlineSmall,
      ),
    );
  }
}
