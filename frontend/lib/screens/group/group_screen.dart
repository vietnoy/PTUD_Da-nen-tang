import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:provider/provider.dart';
import '../../services/group_service.dart';
import '../../models/group.dart';
import '../../providers/auth_provider.dart';

class GroupScreen extends StatefulWidget {
  final int groupId;

  const GroupScreen({super.key, required this.groupId});

  @override
  State<GroupScreen> createState() => _GroupScreenState();
}

class _GroupScreenState extends State<GroupScreen> {
  final _groupService = GroupService();
  List<GroupMember> _members = [];
  String _groupName = '';
  String? _inviteCode;
  bool _isLoading = false;

  @override
  void initState() {
    super.initState();
    _loadMembers();
  }

  Future<void> _loadMembers() async {
    setState(() => _isLoading = true);

    try {
      final result = await _groupService.getMembers(widget.groupId);
      print('🔥 FRESH CODE: API returned inviteCode = ${result['inviteCode']}');

      // Parse members OUTSIDE setState
      final members = (result['members'] as List)
          .map((json) => GroupMember.fromJson(json))
          .toList();
      print('🔥 Members parsed: ${members.length}');

      setState(() {
        _members = members;
        _groupName = result['groupName'] ?? 'Group';
        _inviteCode = result['inviteCode'] as String?;
        _isLoading = false;
        print('🔥 INSIDE setState: _inviteCode = $_inviteCode, members = ${_members.length}');
      });

      print('🔥 AFTER setState: _inviteCode = $_inviteCode');
    } catch (e) {
      setState(() {
        _isLoading = false;
      });
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Failed to load members: ${e.toString()}'),
            backgroundColor: Colors.red,
          ),
        );
      }
    }
  }

  Future<void> _addMember() async {
    final controller = TextEditingController();

    final result = await showDialog<String>(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Join Group'),
        content: TextField(
          controller: controller,
          decoration: const InputDecoration(
            labelText: 'Invite Code',
            hintText: 'Enter 6-character invite code',
          ),
          autofocus: true,
          maxLength: 6,
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('Cancel'),
          ),
          TextButton(
            onPressed: () => Navigator.pop(context, controller.text),
            child: const Text('Join'),
          ),
        ],
      ),
    );

    if (result != null && result.isNotEmpty) {
      try {
        final response = await _groupService.addMember(result);
        final newGroupId = response['groupId'] as int;

        if (mounted) {
          // Update the auth provider with the new active group
          final authProvider = Provider.of<AuthProvider>(context, listen: false);
          await authProvider.setActiveGroup(newGroupId);

          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(
              content: Text('Successfully joined the group!'),
              backgroundColor: Colors.green,
            ),
          );

          // Navigate back to home so user can see their new group
          Navigator.pop(context, true);
        }
      } catch (e) {
        if (mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(
              content: Text('Failed to join group: ${e.toString()}'),
              backgroundColor: Colors.red,
            ),
          );
        }
      }
    }
  }

  Future<void> _removeMember(GroupMember member) async {
    final authProvider = Provider.of<AuthProvider>(context, listen: false);
    final currentUsername = authProvider.user?.username;
    final isRemovingSelf = currentUsername == member.username;

    final confirm = await showDialog<bool>(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Remove Member'),
        content: Text(
          isRemovingSelf
            ? 'Are you sure you want to leave this group?'
            : 'Remove ${member.name} from the group?'
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context, false),
            child: const Text('Cancel'),
          ),
          TextButton(
            onPressed: () => Navigator.pop(context, true),
            child: Text(
              isRemovingSelf ? 'Leave' : 'Remove',
              style: const TextStyle(color: Colors.red),
            ),
          ),
        ],
      ),
    );

    if (confirm == true) {
      try {
        await _groupService.removeMember(member.username, widget.groupId);
        if (mounted) {
          if (isRemovingSelf) {
            // User left the group - navigate back to home
            ScaffoldMessenger.of(context).showSnackBar(
              const SnackBar(
                content: Text('You have left the group'),
                backgroundColor: Colors.green,
              ),
            );
            Navigator.pop(context, true); // Return true to indicate group change
          } else {
            // Someone else was removed - reload the member list
            ScaffoldMessenger.of(context).showSnackBar(
              const SnackBar(
                content: Text('Member removed successfully'),
                backgroundColor: Colors.green,
              ),
            );
            _loadMembers();
          }
        }
      } catch (e) {
        if (mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(
              content: Text('Failed to remove member: ${e.toString()}'),
              backgroundColor: Colors.red,
            ),
          );
        }
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    print('BUILD: _inviteCode = "$_inviteCode", isNull = ${_inviteCode == null}');
    return Scaffold(
      appBar: AppBar(
        title: Text(_groupName.isEmpty ? 'Group Members' : _groupName),
      ),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator())
          : Column(
              children: [
                if (_inviteCode != null) ...[
                  Card(
                    margin: const EdgeInsets.all(16),
                    color: Theme.of(context).primaryColor.withOpacity(0.1),
                    child: Padding(
                      padding: const EdgeInsets.all(16),
                      child: Row(
                        children: [
                          Icon(
                            Icons.qr_code,
                            color: Theme.of(context).primaryColor,
                            size: 32,
                          ),
                          const SizedBox(width: 16),
                          Expanded(
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Text(
                                  'Invite Code',
                                  style: TextStyle(
                                    fontSize: 12,
                                    color: Colors.grey[600],
                                  ),
                                ),
                                const SizedBox(height: 4),
                                Text(
                                  _inviteCode!,
                                  style: TextStyle(
                                    fontSize: 24,
                                    fontWeight: FontWeight.bold,
                                    color: Theme.of(context).primaryColor,
                                    letterSpacing: 2,
                                  ),
                                ),
                              ],
                            ),
                          ),
                          IconButton(
                            icon: const Icon(Icons.copy),
                            onPressed: () async {
                              await Clipboard.setData(
                                  ClipboardData(text: _inviteCode!));
                              if (mounted) {
                                ScaffoldMessenger.of(context).showSnackBar(
                                  const SnackBar(
                                    content: Text('Code copied to clipboard'),
                                    duration: Duration(seconds: 2),
                                  ),
                                );
                              }
                            },
                            tooltip: 'Copy invite code',
                          ),
                        ],
                      ),
                    ),
                  ),
                ],
                Expanded(
                  child: _members.isEmpty
                      ? Center(
                          child: Column(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              Icon(
                                Icons.group,
                                size: 80,
                                color: Colors.grey[400],
                              ),
                              const SizedBox(height: 16),
                              Text(
                                'No members in group',
                                style: TextStyle(
                                  fontSize: 18,
                                  color: Colors.grey[600],
                                ),
                              ),
                            ],
                          ),
                        )
                      : RefreshIndicator(
                          onRefresh: _loadMembers,
                          child: ListView.builder(
                            itemCount: _members.length,
                            itemBuilder: (context, index) {
                              final member = _members[index];
                              final isOwner = member.role == 'owner';

                              return Card(
                                margin: const EdgeInsets.symmetric(
                                  horizontal: 16,
                                  vertical: 8,
                                ),
                                child: ListTile(
                                  leading: CircleAvatar(
                                    backgroundColor: Theme.of(context)
                                        .primaryColor
                                        .withOpacity(0.2),
                                    backgroundImage: member.avatar != null
                                        ? NetworkImage(member.avatar!)
                                        : null,
                                    child: member.avatar == null
                                        ? Icon(
                                            Icons.person,
                                            color:
                                                Theme.of(context).primaryColor,
                                          )
                                        : null,
                                  ),
                                  title: Text(
                                    member.name,
                                    style: const TextStyle(
                                        fontWeight: FontWeight.bold),
                                  ),
                                  subtitle: Column(
                                    crossAxisAlignment:
                                        CrossAxisAlignment.start,
                                    children: [
                                      Text('@${member.username}'),
                                      if (isOwner)
                                        Container(
                                          margin:
                                              const EdgeInsets.only(top: 4),
                                          padding: const EdgeInsets.symmetric(
                                            horizontal: 8,
                                            vertical: 2,
                                          ),
                                          decoration: BoxDecoration(
                                            color:
                                                Colors.amber.withOpacity(0.2),
                                            borderRadius:
                                                BorderRadius.circular(12),
                                          ),
                                          child: const Text(
                                            'OWNER',
                                            style: TextStyle(
                                              fontSize: 10,
                                              color: Colors.amber,
                                              fontWeight: FontWeight.bold,
                                            ),
                                          ),
                                        ),
                                    ],
                                  ),
                                  trailing: isOwner
                                      ? const Icon(Icons.star,
                                          color: Colors.amber)
                                      : IconButton(
                                          icon: const Icon(Icons.remove_circle,
                                              color: Colors.red),
                                          onPressed: () => _removeMember(member),
                                        ),
                                ),
                              );
                            },
                          ),
                        ),
                ),
              ],
            ),
      floatingActionButton: FloatingActionButton(
        onPressed: _addMember,
        child: const Icon(Icons.person_add),
      ),
    );
  }
}
