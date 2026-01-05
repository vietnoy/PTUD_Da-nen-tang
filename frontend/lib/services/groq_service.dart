import 'dart:convert';
import 'package:dio/dio.dart';
import 'package:shared_preferences/shared_preferences.dart';

/// Service for interacting with Groq AI API
class GroqService {
  static const String _baseUrl = 'https://api.groq.com/openai/v1';
  static const String _model = 'llama-3.3-70b-versatile';
  static const String _systemPrompt =
      'Với vai trò là 1 chuyên gia về dinh dưỡng và thực phẩm, trả lời câu hỏi sau của người dùng';

  final Dio _dio;
  final String _apiKey;

  GroqService(this._apiKey)
      : _dio = Dio(BaseOptions(
          baseUrl: _baseUrl,
          headers: {
            'Authorization': 'Bearer $_apiKey',
            'Content-Type': 'application/json',
          },
          connectTimeout: const Duration(seconds: 30),
          receiveTimeout: const Duration(seconds: 30),
        ));

  /// Send a chat message and get AI response
  Future<String> sendMessage(String message,
      {List<Map<String, String>>? conversationHistory}) async {
    try {
      // Build messages array with system prompt and conversation history
      final messages = <Map<String, String>>[
        {'role': 'system', 'content': _systemPrompt},
      ];

      // Add conversation history if provided
      if (conversationHistory != null && conversationHistory.isNotEmpty) {
        messages.addAll(conversationHistory);
      }

      // Add current user message
      messages.add({'role': 'user', 'content': message});

      final response = await _dio.post(
        '/chat/completions',
        data: {
          'model': _model,
          'messages': messages,
          'temperature': 0.7,
          'max_tokens': 1024,
          'top_p': 1,
          'stream': false,
        },
      );

      if (response.statusCode == 200) {
        final data = response.data;
        
        // Safely extract content from nested response structure
        String content = '';
        try {
          if (data is Map && data.containsKey('choices')) {
            final choices = data['choices'] as List;
            if (choices.isNotEmpty) {
              final firstChoice = choices[0] as Map;
              if (firstChoice.containsKey('message')) {
                final message = firstChoice['message'] as Map;
                content = message['content'] as String? ?? '';
              }
            }
          }
        } catch (e) {
          throw Exception('Failed to parse response: $e');
        }

        if (content.isEmpty) {
          throw Exception('Empty response content from API');
        }

        // Clean up markdown formatting from Groq response
        content = _cleanMarkdownFormatting(content);
        return content;
      } else {
        throw Exception('Failed to get response: ${response.statusCode}');
      }
    } on DioException catch (e) {
      if (e.response != null) {
        throw Exception(
            'API Error: ${e.response?.statusCode} - ${e.response?.data}');
      } else {
        throw Exception('Network Error: ${e.message}');
      }
    } catch (e) {
      throw Exception('Error: $e');
    }
  }

  /// Clean up markdown formatting in AI response
  /// Converts markdown text to plain text while preserving readability
  static String _cleanMarkdownFormatting(String text) {
    // 1. Remove placeholder tokens FIRST - various formats
    // Matches: $1, $1:, $1: (with spaces), etc
    text = text.replaceAll(RegExp(r'\$\d+:\s*'), '');
    text = text.replaceAll(RegExp(r'\$\d+\s+'), '');
    text = text.replaceAll(RegExp(r'\$\d+'), '');
    
    // 2. Remove markdown bold (**text** or __text__)
    text = text.replaceAllMapped(RegExp(r'\*\*([^*]+)\*\*'), (match) => match.group(1) ?? '');
    text = text.replaceAllMapped(RegExp(r'__([^_]+)__'), (match) => match.group(1) ?? '');
    
    // 3. Remove markdown italic (*text* or _text_)
    text = text.replaceAllMapped(RegExp(r'\*([^*]+)\*'), (match) => match.group(1) ?? '');
    text = text.replaceAllMapped(RegExp(r'_([^_]+)_'), (match) => match.group(1) ?? '');
    
    // 4. Remove markdown code (`text`)
    text = text.replaceAllMapped(RegExp(r'`([^`]+)`'), (match) => match.group(1) ?? '');
    
    // 5. Remove code blocks (```code```)
    text = text.replaceAll(RegExp(r'```[\s\S]*?```'), '');
    
    // 6. Convert markdown headers to plain text (#, ##, ###, etc)
    text = text.replaceAll(RegExp(r'^#+\s+', multiLine: true), '');
    
    // 7. Handle markdown links [text](url) -> text
    text = text.replaceAllMapped(RegExp(r'\[([^\]]+)\]\([^\)]+\)'), (match) => match.group(1) ?? '');
    
    // 8. Remove markdown blockquotes (> text)
    text = text.replaceAll(RegExp(r'^>\s+', multiLine: true), '');
    
    // 9. Convert markdown bullet points to text (keep content, remove formatting)
    text = text.replaceAll(RegExp(r'^[\*\-\+]\s+', multiLine: true), '• ');
    
    // 10. Clean up multiple spaces
    text = text.replaceAll(RegExp(r' {2,}'), ' ');
    
    // 11. Clean up excessive newlines (more than 2 consecutive)
    text = text.replaceAll(RegExp(r'\n{3,}'), '\n\n');
    
    // 12. Remove trailing whitespace from each line
    text = text.split('\n').map((line) => line.trimRight()).join('\n');
    
    return text.trim();
  }

  /// Save chat history to local storage
  static Future<void> saveChatHistory(List<ChatMessage> messages) async {
    final prefs = await SharedPreferences.getInstance();
    final messagesJson = messages.map((m) => m.toJson()).toList();
    await prefs.setString('chat_history', jsonEncode(messagesJson));
  }

  /// Load chat history from local storage
  static Future<List<ChatMessage>> loadChatHistory() async {
    final prefs = await SharedPreferences.getInstance();
    final historyJson = prefs.getString('chat_history');
    if (historyJson == null) return [];

    try {
      final List<dynamic> decoded = jsonDecode(historyJson);
      return decoded.map((json) => ChatMessage.fromJson(json)).toList();
    } catch (e) {
      return [];
    }
  }

  /// Clear chat history
  static Future<void> clearChatHistory() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove('chat_history');
  }
}

/// Chat message model
class ChatMessage {
  final String role; // 'user' or 'assistant'
  final String content;
  final DateTime timestamp;

  ChatMessage({
    required this.role,
    required this.content,
    DateTime? timestamp,
  }) : timestamp = timestamp ?? DateTime.now();

  Map<String, dynamic> toJson() => {
        'role': role,
        'content': content,
        'timestamp': timestamp.toIso8601String(),
      };

  factory ChatMessage.fromJson(Map<String, dynamic> json) => ChatMessage(
        role: json['role'] as String,
        content: json['content'] as String,
        timestamp: DateTime.parse(json['timestamp'] as String),
      );

  /// Convert to format for API request
  Map<String, String> toApiFormat() => {
        'role': role,
        'content': content,
      };
}
