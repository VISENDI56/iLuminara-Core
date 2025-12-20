import 'package:flutter/foundation.dart';
import 'package:connectivity_plus/connectivity_plus.dart';
import 'dart:async';

/// Connectivity service to monitor network status
/// Enables offline-first behavior
class ConnectivityService extends ChangeNotifier {
  final Connectivity _connectivity = Connectivity();
  ConnectivityResult _connectionStatus = ConnectivityResult.none;
  late StreamSubscription<ConnectivityResult> _connectivitySubscription;

  ConnectivityService() {
    _initializeConnectivity();
  }

  bool get isOnline => _connectionStatus != ConnectivityResult.none;
  bool get isOffline => _connectionStatus == ConnectivityResult.none;
  ConnectivityResult get connectionStatus => _connectionStatus;

  String get connectionType {
    switch (_connectionStatus) {
      case ConnectivityResult.wifi:
        return 'WiFi';
      case ConnectivityResult.mobile:
        return 'Mobile Data';
      case ConnectivityResult.ethernet:
        return 'Ethernet';
      case ConnectivityResult.bluetooth:
        return 'Bluetooth';
      case ConnectivityResult.vpn:
        return 'VPN';
      case ConnectivityResult.none:
        return 'Offline';
      default:
        return 'Unknown';
    }
  }

  Future<void> _initializeConnectivity() async {
    try {
      // Check initial connectivity status
      _connectionStatus = await _connectivity.checkConnectivity();
      notifyListeners();

      // Listen to connectivity changes
      _connectivitySubscription = _connectivity.onConnectivityChanged.listen(
        (ConnectivityResult result) {
          _connectionStatus = result;
          notifyListeners();
          
          // Log connectivity changes
          debugPrint('Connectivity changed: ${connectionType}');
        },
      );
    } catch (e) {
      debugPrint('Error initializing connectivity: $e');
    }
  }

  @override
  void dispose() {
    _connectivitySubscription.cancel();
    super.dispose();
  }

  /// Force refresh connectivity status
  Future<void> refreshStatus() async {
    try {
      _connectionStatus = await _connectivity.checkConnectivity();
      notifyListeners();
    } catch (e) {
      debugPrint('Error refreshing connectivity: $e');
    }
  }
}
