class ResultMessage {
  final String en;
  final String vn;

  ResultMessage({required this.en, required this.vn});

  factory ResultMessage.fromJson(Map<String, dynamic> json) {
    return ResultMessage(
      en: json['en'] ?? '',
      vn: json['vn'] ?? '',
    );
  }
}

class ApiResponse<T> {
  final String resultCode;
  final ResultMessage resultMessage;
  final T? data;

  ApiResponse({
    required this.resultCode,
    required this.resultMessage,
    this.data,
  });

  bool get isSuccess => resultCode.startsWith('00');
  
  String get message => resultMessage.en;
}
