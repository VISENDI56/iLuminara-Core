import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../services/auth_service.dart';
import '../services/storage_service.dart';
import '../services/connectivity_service.dart';
import '../widgets/voice_recorder_widget.dart';
import '../widgets/voice_notes_list.dart';

/// Home screen for Community Health Workers
/// Compassionate UI with offline-first capabilities
class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  int _selectedIndex = 0;

  @override
  Widget build(BuildContext context) {
    final authService = context.watch<AuthService>();
    final connectivityService = context.watch<ConnectivityService>();
    final storageService = context.watch<StorageService>();

    return Scaffold(
      appBar: AppBar(
        title: const Text('iLuminara'),
        elevation: 0,
        backgroundColor: Theme.of(context).colorScheme.primary,
        foregroundColor: Colors.white,
        actions: [
          // Connectivity indicator
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 8),
            child: Chip(
              avatar: Icon(
                connectivityService.isOnline 
                    ? Icons.cloud_done_rounded 
                    : Icons.cloud_off_rounded,
                size: 18,
                color: connectivityService.isOnline 
                    ? Colors.green.shade700 
                    : Colors.orange.shade700,
              ),
              label: Text(
                connectivityService.connectionType,
                style: const TextStyle(fontSize: 12),
              ),
              backgroundColor: connectivityService.isOnline
                  ? Colors.green.shade50
                  : Colors.orange.shade50,
            ),
          ),
          
          // Sync indicator
          if (storageService.pendingUploads > 0)
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 8),
              child: Chip(
                avatar: storageService.isSyncing
                    ? const SizedBox(
                        width: 16,
                        height: 16,
                        child: CircularProgressIndicator(strokeWidth: 2),
                      )
                    : Icon(
                        Icons.sync_problem_rounded,
                        size: 18,
                        color: Colors.orange.shade700,
                      ),
                label: Text(
                  '${storageService.pendingUploads} pending',
                  style: const TextStyle(fontSize: 12),
                ),
                backgroundColor: Colors.orange.shade50,
              ),
            ),
          
          // User menu
          PopupMenuButton<String>(
            icon: const Icon(Icons.account_circle_rounded),
            onSelected: (value) {
              if (value == 'logout') {
                _handleLogout();
              } else if (value == 'sync') {
                storageService.syncNow();
              }
            },
            itemBuilder: (context) => [
              PopupMenuItem(
                enabled: false,
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      authService.currentUser?.displayName ?? 'Community Health Worker',
                      style: const TextStyle(fontWeight: FontWeight.bold),
                    ),
                    const SizedBox(height: 4),
                    Text(
                      authService.currentUser?.email ?? '',
                      style: TextStyle(
                        fontSize: 12,
                        color: Colors.grey[600],
                      ),
                    ),
                  ],
                ),
              ),
              const PopupMenuDivider(),
              if (storageService.pendingUploads > 0)
                const PopupMenuItem(
                  value: 'sync',
                  child: Row(
                    children: [
                      Icon(Icons.sync_rounded),
                      SizedBox(width: 8),
                      Text('Sync now'),
                    ],
                  ),
                ),
              const PopupMenuItem(
                value: 'logout',
                child: Row(
                  children: [
                    Icon(Icons.logout_rounded),
                    SizedBox(width: 8),
                    Text('Sign out'),
                  ],
                ),
              ),
            ],
          ),
        ],
      ),
      body: IndexedStack(
        index: _selectedIndex,
        children: const [
          _RecordTab(),
          _VoiceNotesTab(),
          _ProfileTab(),
        ],
      ),
      bottomNavigationBar: NavigationBar(
        selectedIndex: _selectedIndex,
        onDestinationSelected: (index) {
          setState(() {
            _selectedIndex = index;
          });
        },
        destinations: const [
          NavigationDestination(
            icon: Icon(Icons.mic_outlined),
            selectedIcon: Icon(Icons.mic_rounded),
            label: 'Record',
          ),
          NavigationDestination(
            icon: Icon(Icons.folder_outlined),
            selectedIcon: Icon(Icons.folder_rounded),
            label: 'Voice Notes',
          ),
          NavigationDestination(
            icon: Icon(Icons.person_outline_rounded),
            selectedIcon: Icon(Icons.person_rounded),
            label: 'Profile',
          ),
        ],
      ),
    );
  }

  Future<void> _handleLogout() async {
    final confirmed = await showDialog<bool>(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Sign out'),
        content: const Text('Are you sure you want to sign out?'),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context, false),
            child: const Text('Cancel'),
          ),
          ElevatedButton(
            onPressed: () => Navigator.pop(context, true),
            child: const Text('Sign out'),
          ),
        ],
      ),
    );

    if (confirmed == true && mounted) {
      await context.read<AuthService>().signOut();
    }
  }
}

/// Record tab with voice recorder
class _RecordTab extends StatelessWidget {
  const _RecordTab();

  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(24),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          // Welcome message
          Text(
            'Record Health Observation',
            style: Theme.of(context).textTheme.headlineMedium,
          ),
          const SizedBox(height: 8),
          Text(
            'Record voice notes with location data for patient observations',
            style: Theme.of(context).textTheme.bodyLarge?.copyWith(
              color: Colors.grey[600],
            ),
          ),
          const SizedBox(height: 32),
          
          // Voice recorder widget
          const VoiceRecorderWidget(),
          
          const SizedBox(height: 32),
          
          // Information card
          Card(
            child: Padding(
              padding: const EdgeInsets.all(20),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      Icon(
                        Icons.info_outline_rounded,
                        color: Theme.of(context).colorScheme.primary,
                      ),
                      const SizedBox(width: 12),
                      Text(
                        'How it works',
                        style: Theme.of(context).textTheme.titleMedium,
                      ),
                    ],
                  ),
                  const SizedBox(height: 16),
                  _buildInfoItem(
                    context,
                    Icons.offline_bolt_rounded,
                    'Offline First',
                    'Records are saved locally and sync when online',
                  ),
                  const SizedBox(height: 12),
                  _buildInfoItem(
                    context,
                    Icons.location_on_rounded,
                    'Location Tagged',
                    'GPS coordinates are automatically captured',
                  ),
                  const SizedBox(height: 12),
                  _buildInfoItem(
                    context,
                    Icons.security_rounded,
                    'Private & Secure',
                    'All data is encrypted and GDPR compliant',
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildInfoItem(BuildContext context, IconData icon, String title, String description) {
    return Row(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Icon(
          icon,
          size: 20,
          color: Colors.grey[600],
        ),
        const SizedBox(width: 12),
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                title,
                style: const TextStyle(fontWeight: FontWeight.w600),
              ),
              const SizedBox(height: 2),
              Text(
                description,
                style: TextStyle(
                  fontSize: 13,
                  color: Colors.grey[600],
                ),
              ),
            ],
          ),
        ),
      ],
    );
  }
}

/// Voice notes list tab
class _VoiceNotesTab extends StatelessWidget {
  const _VoiceNotesTab();

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Padding(
          padding: const EdgeInsets.all(24),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                'Voice Notes',
                style: Theme.of(context).textTheme.headlineMedium,
              ),
              const SizedBox(height: 8),
              Text(
                'View and manage your recorded observations',
                style: Theme.of(context).textTheme.bodyLarge?.copyWith(
                  color: Colors.grey[600],
                ),
              ),
            ],
          ),
        ),
        const Expanded(
          child: VoiceNotesList(),
        ),
      ],
    );
  }
}

/// Profile tab
class _ProfileTab extends StatelessWidget {
  const _ProfileTab();

  @override
  Widget build(BuildContext context) {
    final authService = context.watch<AuthService>();
    final storageService = context.watch<StorageService>();

    return SingleChildScrollView(
      padding: const EdgeInsets.all(24),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          // Profile header
          Text(
            'Profile',
            style: Theme.of(context).textTheme.headlineMedium,
          ),
          const SizedBox(height: 32),
          
          // User info card
          Card(
            child: Padding(
              padding: const EdgeInsets.all(24),
              child: Column(
                children: [
                  CircleAvatar(
                    radius: 50,
                    backgroundColor: Theme.of(context).colorScheme.primary,
                    child: Text(
                      authService.currentUser?.displayName?.substring(0, 1).toUpperCase() ?? 'C',
                      style: const TextStyle(
                        fontSize: 36,
                        color: Colors.white,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ),
                  const SizedBox(height: 16),
                  Text(
                    authService.currentUser?.displayName ?? 'Community Health Worker',
                    style: Theme.of(context).textTheme.headlineSmall,
                    textAlign: TextAlign.center,
                  ),
                  const SizedBox(height: 4),
                  Text(
                    authService.currentUser?.email ?? '',
                    style: TextStyle(
                      color: Colors.grey[600],
                    ),
                    textAlign: TextAlign.center,
                  ),
                ],
              ),
            ),
          ),
          const SizedBox(height: 24),
          
          // Statistics card
          Card(
            child: Padding(
              padding: const EdgeInsets.all(24),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    'Statistics',
                    style: Theme.of(context).textTheme.titleLarge,
                  ),
                  const SizedBox(height: 16),
                  _StatRow(
                    label: 'Total Voice Notes',
                    value: storageService.getAllVoiceNotes().length.toString(),
                  ),
                  const Divider(height: 24),
                  _StatRow(
                    label: 'Synced',
                    value: storageService.getAllVoiceNotes()
                        .where((note) => note.isSynced)
                        .length
                        .toString(),
                  ),
                  const Divider(height: 24),
                  _StatRow(
                    label: 'Pending Sync',
                    value: storageService.pendingUploads.toString(),
                  ),
                ],
              ),
            ),
          ),
          const SizedBox(height: 24),
          
          // About card
          Card(
            child: Padding(
              padding: const EdgeInsets.all(24),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    'About',
                    style: Theme.of(context).textTheme.titleLarge,
                  ),
                  const SizedBox(height: 16),
                  Text(
                    'iLuminara is a compassionate health intelligence platform designed '
                    'for Community Health Workers. Built with offline-first capabilities, '
                    'it helps you collect and manage health observations even without '
                    'internet connectivity.',
                    style: TextStyle(color: Colors.grey[700]),
                  ),
                  const SizedBox(height: 16),
                  Text(
                    'Version 1.0.0',
                    style: TextStyle(
                      fontSize: 12,
                      color: Colors.grey[600],
                    ),
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}

class _StatRow extends StatelessWidget {
  final String label;
  final String value;

  const _StatRow({required this.label, required this.value});

  @override
  Widget build(BuildContext context) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceBetween,
      children: [
        Text(
          label,
          style: TextStyle(
            color: Colors.grey[700],
          ),
        ),
        Text(
          value,
          style: const TextStyle(
            fontSize: 18,
            fontWeight: FontWeight.bold,
          ),
        ),
      ],
    );
  }
}
