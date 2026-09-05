#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MSTSC (Remote Desktop) connection module
Execute Windows Remote Desktop Connection
"""

import os
import subprocess
import tempfile
from pathlib import Path
from typing import Optional


class MSTSCConnector:
    """MSTSC connection class"""
    
    def __init__(self, server: str, username: Optional[str] = None, password: Optional[str] = None):
        """
        Args:
            server: Server address (e.g., 192.168.0.100:3389 or domain.com:3389)
            username: Username (optional)
            password: Password (optional)
        """
        self.server = server
        self.username = username
        self.password = password
        
        # Separate server address and port
        if ':' in server:
            self.host, port_str = server.rsplit(':', 1)
            self.port = int(port_str)
        else:
            self.host = server
            self.port = 3389  # Default RDP port
    
    def create_rdp_file(self) -> Path:
        """
        Create RDP connection file
        
        Returns:
            Path to created RDP file
        """
        # Create temporary RDP file
        temp_dir = Path(tempfile.gettempdir())
        rdp_file = temp_dir / "wol_mstsc_temp.rdp"
        
        # Write RDP file content (멀티모니터 + 최소 해상도)
        rdp_content = [
            "use multimon:i:1",  # 모든 데스크탑 확장(멀티모니터)
            "screen mode id:i:2",  # Full screen
            # desktopwidth/height는 멀티모니터일 때 자동 적용
            "session bpp:i:8",  # 색상 깊이(최소, 네트워크 대역폭 최소화)
            "compression:i:1",
            "keyboardhook:i:2",
            "audiocapturemode:i:0",
            "videoplaybackmode:i:1",
            "connection type:i:7",
            "networkautodetect:i:1",
            "bandwidthautodetect:i:1",
            "displayconnectionbar:i:1",
            "enableworkspacereconnect:i:0",
            "disable wallpaper:i:0",
            "allow font smoothing:i:1",
            "allow desktop composition:i:1",
            "disable full window drag:i:0",
            "disable menu anims:i:0",
            "disable themes:i:0",
            "disable cursor setting:i:0",
            "bitmapcachepersistenable:i:1",
            f"full address:s:{self.host}:{self.port}",
            "audiomode:i:0",
            "redirectprinters:i:0",
            "redirectcomports:i:0",
            "redirectsmartcards:i:0",
            "redirectclipboard:i:1",
            "redirectposdevices:i:0",
            "autoreconnection enabled:i:1",
            "authentication level:i:0",
            "prompt for credentials:i:0",
            "negotiate security layer:i:1",
            "remoteapplicationmode:i:0",
            "alternate shell:s:",
            "shell working directory:s:",
            "gatewayhostname:s:",
            "gatewayusagemethod:i:0",
            "gatewaycredentialssource:i:0",
            "gatewayprofileusagemethod:i:0",
            "promptcredentialonce:i:0",
            "gatewaybrokeringtype:i:0",
            "use redirection server name:i:0",
            "rdgiskdcproxy:i:0",
            "kdcproxyname:s:",
        ]
        
        # Add username if provided
        if self.username:
            rdp_content.append(f"username:s:{self.username}")
        
        # Write file
        with open(rdp_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(rdp_content))
        
        return rdp_file
    
    def connect(self):
        """
        Execute Remote Desktop connection
        
        Raises:
            Exception: Connection failed
        """
        try:
            print(f"🖥️  Preparing Remote Desktop connection...")
            print(f"   Server: {self.host}:{self.port}")
            if self.username:
                print(f"   User: {self.username}")
            
            # Create RDP file
            rdp_file = self.create_rdp_file()
            print(f"   RDP file created: {rdp_file}")
            
            # Execute MSTSC
            # /v: Specify server address
            # /f: Full screen
            # Pass RDP file as argument
            
            cmd = ['mstsc', str(rdp_file)]
            
            print(f"   Executing command: {' '.join(cmd)}")
            
            # Run in background (async)
            subprocess.Popen(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP
            )
            
            print("✅ Remote Desktop client launched")
            print("   💡 Will auto-login if saved credentials exist")
            print("   💡 Otherwise, please login manually")
            
        except FileNotFoundError:
            raise Exception("MSTSC not found. Please check if Windows Remote Desktop is installed")
        except Exception as e:
            raise Exception(f"Remote Desktop connection failed: {e}")
    
    def connect_simple(self):
        """
        Simple MSTSC connection (without RDP file)
        
        Raises:
            Exception: Connection failed
        """
        try:
            print(f"🖥️  Connecting to Remote Desktop... ({self.host}:{self.port})")
            
            # Execute in format: mstsc /v:server_address:port
            cmd = ['mstsc', f'/v:{self.host}:{self.port}']
            
            subprocess.Popen(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP
            )
            
            print("✅ Remote Desktop client launched")
            
        except FileNotFoundError:
            raise Exception("MSTSC not found. Please check if Windows Remote Desktop is installed")
        except Exception as e:
            raise Exception(f"Remote Desktop connection failed: {e}")
