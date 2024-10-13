import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

class RestaurantChatApp extends StatefulWidget {
  @override
  _RestaurantChatAppState createState() => _RestaurantChatAppState();
}

class _RestaurantChatAppState extends State<RestaurantChatApp> {
  final TextEditingController _controller = TextEditingController();
  String _suggestions = "";

  // Function to send input to FastAPI and get suggestions
  Future<void> getSuggestions(String query) async {
    final response = await http.post(
      Uri.parse('https://allyai-1.onrender.com/suggest_restaurant'),
      headers: {"Content-Type": "application/json"},
      body: jsonEncode({"query": query}),
    );

    if (response.statusCode == 200) {
      final responseData = jsonDecode(response.body);
      setState(() {
        _suggestions = responseData['suggestions'].join(', ');
      });
    } else {
      setState(() {
        _suggestions = "Error getting suggestions!";
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Restaurant Chat Assistant'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(8.0),
        child: Column(
          children: [
            TextField(
              controller: _controller,
              decoration: InputDecoration(
                labelText: 'What kind of restaurant are you looking for?',
              ),
            ),
            SizedBox(height: 10),
            ElevatedButton(
              onPressed: () {
                getSuggestions(_controller.text);
              },
              child: Text('Get Suggestions'),
            ),
            SizedBox(height: 20),
            Text(
              'Suggestions: $_suggestions',
              style: TextStyle(fontSize: 16),
            ),
          ],
        ),
      ),
    );
  }
}

void main() {
  runApp(MaterialApp(home: RestaurantChatApp()));
}
