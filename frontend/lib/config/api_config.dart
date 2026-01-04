class ApiConfig {
  // For Chrome/Web & iOS simulator: use localhost
  // For Android emulator: use 10.0.2.2 (emulator's special alias for host machine)
  // For physical device: use your machine's local IP (find with: ipconfig getifaddr en0)
  static const String baseUrl = 'http://localhost:8000/api/v1';  // Chrome/Web & iOS
  // static const String baseUrl = 'http://10.0.2.2:8000/api/v1';  // Android emulator
  // static const String baseUrl = 'http://192.168.1.X:8000/api/v1';  // Physical device

  static const Duration connectTimeout = Duration(seconds: 30);
  static const Duration receiveTimeout = Duration(seconds: 30);
}
