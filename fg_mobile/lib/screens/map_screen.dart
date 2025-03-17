import 'package:flutter/material.dart';

class MapScreen extends StatelessWidget {
  const MapScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Text(
        'Live Threat Map',
        style: Theme.of(context).textTheme.headlineSmall,
      ),
    );
  }
}
