import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../services/groq_service.dart';
import '../config/api_config.dart';

class ChatbotScreen extends StatefulWidget {
  const ChatbotScreen({super.key});

  @override
  State<ChatbotScreen> createState() => _ChatbotScreenState();
}

class _ChatbotScreenState extends State<ChatbotScreen> {
  final TextEditingController _messageController = TextEditingController();
  final ScrollController _scrollController = ScrollController();
  final List<ChatMessage> _messages = [];
  bool _isLoading = false;
  GroqService? _groqService;

  // Quick suggestion questions
  final List<String> _quickSuggestions = [
    'Thực phẩm nào tốt cho tim mạch?',
    'Cách bảo quản rau củ quả đúng cách',
    'Chế độ ăn cho người tiểu đường',
    'Thực phẩm giàu protein cho người tập gym',
    'Cách nấu ăn để giữ dinh dưỡng',
  ];

  @override
  void initState() {
    super.initState();
    _loadChatHistory();
    _initializeGroqService();
  }

  Future<void> _initializeGroqService() async {
    // Load API key from config
    const apiKey = ApiConfig.groqApiKey;
    
    setState(() {
      _groqService = GroqService(apiKey);
    });
  }

  Future<void> _loadChatHistory() async {
    final history = await GroqService.loadChatHistory();
    setState(() {
      _messages.addAll(history);
    });
    _scrollToBottom();
  }

  Future<void> _saveChatHistory() async {
    await GroqService.saveChatHistory(_messages);
  }

  void _scrollToBottom() {
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (_scrollController.hasClients) {
        _scrollController.animateTo(
          _scrollController.position.maxScrollExtent,
          duration: const Duration(milliseconds: 300),
          curve: Curves.easeOut,
        );
      }
    });
  }

  Future<void> _sendMessage(String message) async {
    if (message.trim().isEmpty || _groqService == null) return;

    // Check if API key is configured
    if (ApiConfig.groqApiKey == 'your-groq-api-key-here') {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Vui lòng cấu hình GROQ_API_KEY trong api_config.dart'),
          backgroundColor: Colors.orange,
          duration: Duration(seconds: 5),
        ),
      );
      return;
    }

    // Add user message
    final userMessage = ChatMessage(role: 'user', content: message);
    setState(() {
      _messages.add(userMessage);
      _isLoading = true;
    });
    _messageController.clear();
    _scrollToBottom();

    try {
      // Get conversation history for context
      final conversationHistory = _messages
          .map((m) => m.toApiFormat())
          .toList();

      // Send to Groq API
      final response = await _groqService!.sendMessage(
        message,
        conversationHistory: conversationHistory.length > 10
            ? conversationHistory.sublist(conversationHistory.length - 10)
            : conversationHistory,
      );

      // Add assistant response
      final assistantMessage = ChatMessage(
        role: 'assistant',
        content: response,
      );
      setState(() {
        _messages.add(assistantMessage);
      });

      // Save chat history
      await _saveChatHistory();
      _scrollToBottom();
    } catch (e) {
      // Show error message
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text('Lỗi: ${e.toString()}'),
          backgroundColor: Colors.red,
        ),
      );
    } finally {
      setState(() {
        _isLoading = false;
      });
    }
  }

  Future<void> _clearHistory() async {
    final confirmed = await showDialog<bool>(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Xóa lịch sử chat'),
        content: const Text('Bạn có chắc muốn xóa toàn bộ lịch sử chat?'),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context, false),
            child: const Text('Hủy'),
          ),
          TextButton(
            onPressed: () => Navigator.pop(context, true),
            child: const Text('Xóa', style: TextStyle(color: Colors.red)),
          ),
        ],
      ),
    );

    if (confirmed == true) {
      await GroqService.clearChatHistory();
      setState(() {
        _messages.clear();
      });
    }
  }

  @override
  void dispose() {
    _messageController.dispose();
    _scrollController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Trợ lý dinh dưỡng AI'),
        actions: [
          if (_messages.isNotEmpty)
            IconButton(
              icon: const Icon(Icons.delete_outline),
              onPressed: _clearHistory,
              tooltip: 'Xóa lịch sử',
            ),
        ],
      ),
      body: Column(
        children: [
          // Quick suggestions (only show when no messages)
          if (_messages.isEmpty) _buildQuickSuggestions(),

          // Chat messages
          Expanded(
            child: _messages.isEmpty
                ? _buildEmptyState()
                : ListView.builder(
                    controller: _scrollController,
                    padding: const EdgeInsets.all(16),
                    itemCount: _messages.length,
                    itemBuilder: (context, index) {
                      final message = _messages[index];
                      return _buildMessageBubble(message);
                    },
                  ),
          ),

          // Loading indicator
          if (_isLoading)
            const Padding(
              padding: EdgeInsets.all(8.0),
              child: Row(
                children: [
                  SizedBox(width: 16),
                  SizedBox(
                    width: 20,
                    height: 20,
                    child: CircularProgressIndicator(strokeWidth: 2),
                  ),
                  SizedBox(width: 12),
                  Text('Đang suy nghĩ...', style: TextStyle(color: Colors.grey)),
                ],
              ),
            ),

          // Input field
          _buildInputField(),
        ],
      ),
    );
  }

  Widget _buildEmptyState() {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Icon(
            Icons.chat_bubble_outline,
            size: 80,
            color: Colors.grey[300],
          ),
          const SizedBox(height: 16),
          Text(
            'Xin chào! Tôi là trợ lý AI về dinh dưỡng',
            style: TextStyle(
              fontSize: 18,
              color: Colors.grey[600],
              fontWeight: FontWeight.w500,
            ),
          ),
          const SizedBox(height: 8),
          Text(
            'Hãy hỏi tôi bất kỳ câu hỏi nào về thực phẩm và dinh dưỡng',
            style: TextStyle(
              fontSize: 14,
              color: Colors.grey[500],
            ),
            textAlign: TextAlign.center,
          ),
        ],
      ),
    );
  }

  Widget _buildQuickSuggestions() {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.blue[50],
        border: Border(
          bottom: BorderSide(color: Colors.grey[200]!),
        ),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text(
            'Gợi ý câu hỏi:',
            style: TextStyle(
              fontWeight: FontWeight.w600,
              fontSize: 14,
            ),
          ),
          const SizedBox(height: 8),
          Wrap(
            spacing: 8,
            runSpacing: 8,
            children: _quickSuggestions.map((suggestion) {
              return InkWell(
                onTap: () => _sendMessage(suggestion),
                child: Chip(
                  label: Text(
                    suggestion,
                    style: const TextStyle(fontSize: 13),
                  ),
                  backgroundColor: Colors.white,
                  side: BorderSide(color: Colors.blue[200]!),
                ),
              );
            }).toList(),
          ),
        ],
      ),
    );
  }

  Widget _buildMessageBubble(ChatMessage message) {
    final isUser = message.role == 'user';
    return Align(
      alignment: isUser ? Alignment.centerRight : Alignment.centerLeft,
      child: Container(
        margin: const EdgeInsets.only(bottom: 16),
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
        constraints: BoxConstraints(
          maxWidth: MediaQuery.of(context).size.width * 0.75,
        ),
        decoration: BoxDecoration(
          color: isUser ? Colors.blue[600] : Colors.grey[200],
          borderRadius: BorderRadius.circular(16),
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Use SelectableText to allow text selection
            SelectableText(
              message.content,
              style: TextStyle(
                color: isUser ? Colors.white : Colors.black87,
                fontSize: 15,
                height: 1.6, // Better line spacing for readability
                wordSpacing: 0.5,
                letterSpacing: 0.2,
              ),
            ),
            const SizedBox(height: 8),
            Text(
              _formatTime(message.timestamp),
              style: TextStyle(
                color: isUser ? Colors.white70 : Colors.grey[600],
                fontSize: 11,
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildInputField() {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.white,
        boxShadow: [
          BoxShadow(
            color: Colors.grey.withOpacity(0.2),
            blurRadius: 4,
            offset: const Offset(0, -2),
          ),
        ],
      ),
      child: Row(
        children: [
          Expanded(
            child: TextField(
              controller: _messageController,
              decoration: InputDecoration(
                hintText: 'Nhập câu hỏi của bạn...',
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(24),
                ),
                contentPadding: const EdgeInsets.symmetric(
                  horizontal: 16,
                  vertical: 12,
                ),
              ),
              maxLines: null,
              textInputAction: TextInputAction.send,
              onSubmitted: _sendMessage,
              enabled: !_isLoading,
            ),
          ),
          const SizedBox(width: 8),
          IconButton(
            icon: const Icon(Icons.send),
            onPressed: _isLoading
                ? null
                : () => _sendMessage(_messageController.text),
            color: Colors.blue[600],
          ),
        ],
      ),
    );
  }

  String _formatTime(DateTime time) {
    final now = DateTime.now();
    final difference = now.difference(time);

    if (difference.inMinutes < 1) {
      return 'Vừa xong';
    } else if (difference.inHours < 1) {
      return '${difference.inMinutes} phút trước';
    } else if (difference.inDays < 1) {
      return '${difference.inHours} giờ trước';
    } else {
      return '${time.day}/${time.month}/${time.year}';
    }
  }
}
