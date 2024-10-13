// screens/home_page.dart
import 'package:flutter/material.dart';
import '../services/api_service.dart'; // Import the API service

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  HomePageState createState() => HomePageState();
}

class HomePageState extends State<HomePage> {
  final TextEditingController _controller = TextEditingController();
  final List<String> _messages = [];
  final ApiService _apiService = ApiService(); // Instance of ApiService

void _sendMessage() async {
  String message = _controller.text.trim();
  if (message.isNotEmpty) {
    setState(() {
      _messages.add("You: $message"); // Add the user message to the chat
    });

    _controller.clear(); // Clear the input field after sending

    try {
      // Log to verify that the API request is sent
      print("Sending request to the API with message: $message");

      // Fetch suggestions from the backend via ApiService
      List<String> suggestions = await _apiService.getRestaurantSuggestions(message);
      
      // Log to check if the response is received
      print("Suggestions received: $suggestions");

      setState(() {
        _messages.add("Assistant: Here are some suggestions for '$message':");
        for (String suggestion in suggestions) {
          _messages.add(" - $suggestion");
        }
      });
    } catch (e) {
      print('Error fetching suggestions: $e'); // Log error to console
      setState(() {
        _messages.add("Assistant: Error getting suggestions.");
      });
    }
  }
}


  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.grey[200],
      appBar: AppBar(
        title: const Text(
          'Restaurant Chat Assistant',
          style: TextStyle(color: Colors.red),
        ),
      ),
      body: Column(
        children: <Widget>[
          // Chat message area
          Expanded(
            child: ListView.builder(
              itemCount: _messages.length,
              itemBuilder: (context, index) {
                return ListTile(
                  title: Align(
                    alignment: _messages[index].startsWith("You:")
                        ? Alignment.centerLeft
                        : Alignment.centerRight,
                    child: Container(
                      padding: const EdgeInsets.all(10),
                      decoration: BoxDecoration(
                        color: _messages[index].startsWith("You:")
                            ? Colors.blueAccent
                            : Colors.greenAccent,
                        borderRadius: BorderRadius.circular(8),
                      ),
                      child: Text(
                        _messages[index],
                        style: const TextStyle(color: Colors.white),
                      ),
                    ),
                  ),
                );
              },
            ),
          ),
          // Message input and send button
          Padding(
            padding: const EdgeInsets.all(8.0),
            child: Row(
              children: <Widget>[
                Expanded(
                  child: TextField(
                    controller: _controller,
                    decoration: const InputDecoration(
                      labelText: 'What kind of restaurant are you looking for?',
                      border: OutlineInputBorder(),
                    ),
                  ),
                ),
                IconButton(
                  icon: const Icon(Icons.send),
                  onPressed: _sendMessage,
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
