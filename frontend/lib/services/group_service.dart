import 'package:dio/dio.dart';
import 'api_client.dart';
import '../models/api_response.dart';
import '../models/group.dart';

class GroupService {
  final ApiClient _apiClient = ApiClient();

  Future<Map<String, dynamic>> createGroup(String name, {String? description}) async {
    try {
      final response = await _apiClient.dio.post(
        '/user/group',
        data: {
          'name': name,
          if (description != null) 'description': description,
        },
      );

      return {
        'inviteCode': response.data['inviteCode'],
        'groupName': response.data['groupName'],
        'ownerId': response.data['ownerId'],
        'resultCode': response.data['resultCode'],
        'resultMessage': ResultMessage.fromJson(response.data['resultMessage']),
      };
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }

  Future<Map<String, dynamic>> addMember(String inviteCode) async {
    try {
      final response = await _apiClient.dio.post(
        '/user/group/add',
        data: {'inviteCode': inviteCode},
      );

      return {
        'resultCode': response.data['resultCode'],
        'resultMessage': ResultMessage.fromJson(response.data['resultMessage']),
      };
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }

  Future<Map<String, dynamic>> removeMember(String username, int groupId) async {
    try {
      final response = await _apiClient.dio.delete(
        '/user/group',
        data: {
          'user_name': username,
          'group_id': groupId,
        },
      );

      return {
        'resultCode': response.data['resultCode'],
        'resultMessage': ResultMessage.fromJson(response.data['resultMessage']),
      };
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }

  Future<Map<String, dynamic>> getMembers(int groupId) async {
    try {
      final response = await _apiClient.dio.get(
        '/user/group',
        queryParameters: {'group_id': groupId},
      );

      return {
        'groupId': response.data['groupId'],
        'groupName': response.data['groupName'],
        'inviteCode': response.data['inviteCode'],
        'members': response.data['members'],
        'resultCode': response.data['resultCode'],
        'resultMessage': ResultMessage.fromJson(response.data['resultMessage']),
      };
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }

  String _handleError(DioException e) {
    if (e.response != null) {
      final resultMessage = e.response?.data['resultMessage'];
      if (resultMessage != null) {
        return resultMessage['en'] ?? 'An error occurred';
      }
    }
    return e.message ?? 'Network error';
  }
}
