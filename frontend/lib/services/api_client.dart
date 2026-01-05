import 'package:dio/dio.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import '../config/api_config.dart';

class ApiClient {
  static final ApiClient _instance = ApiClient._internal();
  factory ApiClient() => _instance;

  late Dio dio;
  final _storage = const FlutterSecureStorage();
  final List<RequestOptions> _requestQueue = [];
  bool _isRefreshing = false;

  ApiClient._internal() {
    dio = Dio(BaseOptions(
      baseUrl: ApiConfig.baseUrl,
      connectTimeout: ApiConfig.connectTimeout,
      receiveTimeout: ApiConfig.receiveTimeout,
      headers: {
        'Content-Type': 'application/json; charset=utf-8',
      },
      contentType: 'application/json; charset=utf-8',
      responseType: ResponseType.json,
    ));

    _setupInterceptors();
  }

  void _setupInterceptors() {
    // Request interceptor - Add auth token
    dio.interceptors.add(InterceptorsWrapper(
      onRequest: (options, handler) async {
        final accessToken = await _storage.read(key: 'access_token');
        if (accessToken != null) {
          options.headers['Authorization'] = 'Bearer $accessToken';
        }
        return handler.next(options);
      },
      onError: (error, handler) async {
        if (error.response?.statusCode == 401) {
          // Token expired, try to refresh
          if (!_isRefreshing) {
            _isRefreshing = true;
            try {
              final refreshToken = await _storage.read(key: 'refresh_token');
              if (refreshToken != null) {
                final response = await dio.post(
                  '/auth/refresh',
                  data: {'refreshToken': refreshToken},
                );

                if (response.statusCode == 200) {
                  final newAccessToken = response.data['accessToken'];
                  await _storage.write(key: 'access_token', value: newAccessToken);

                  // Retry original request
                  error.requestOptions.headers['Authorization'] = 'Bearer $newAccessToken';
                  final retryResponse = await dio.fetch(error.requestOptions);
                  _isRefreshing = false;
                  return handler.resolve(retryResponse);
                }
              }
            } catch (e) {
              // Refresh failed, logout user
              await _storage.deleteAll();
              _isRefreshing = false;
            }
          }
        }
        return handler.next(error);
      },
    ));
  }

  Future<void> saveTokens(String accessToken, String refreshToken) async {
    await _storage.write(key: 'access_token', value: accessToken);
    await _storage.write(key: 'refresh_token', value: refreshToken);
  }

  Future<void> clearTokens() async {
    await _storage.deleteAll();
  }

  Future<String?> getAccessToken() async {
    return await _storage.read(key: 'access_token');
  }

  Future<String?> getRefreshToken() async {
    return await _storage.read(key: 'refresh_token');
  }
}
