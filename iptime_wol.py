#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IPTIME router WOL module
Login to IPTIME router and send WOL packets
"""

import requests
import json
from typing import Optional


class IPTimeWOL:
    """IPTIME router WOL class"""
    
    def __init__(self, router_url: str, router_id: str, router_pw: str):
        """
        Args:
            router_url: Router URL (e.g., http://192.168.0.1:80)
            router_id: Router login ID
            router_pw: Router login password
        """
        self.router_url = router_url.rstrip('/')
        self.router_id = router_id
        self.router_pw = router_pw
        self.session = requests.Session()
        self.session_id: Optional[str] = None
    
    def login(self) -> bool:
        """
        Login to router
        
        Returns:
            True if login successful
            
        Raises:
            Exception: Login failed
        """
        url = f"{self.router_url}/cgi/service.cgi"
        
        headers = {
            'Accept': '*/*',
            'Accept-Language': 'ko;q=0.7',
            'Cache-Control': 'no-store',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json; charset=utf-8',
            'Origin': self.router_url,
            'Referer': f'{self.router_url}/ui/',
            'Sec-GPC': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36'
        }
        
        data = {
            "method": "session/login",
            "params": {
                "id": self.router_id,
                "pw": self.router_pw
            }
        }
        
        try:
            response = self.session.post(
                url,
                headers=headers,
                json=data,
                verify=False,
                timeout=10
            )
            
            response.raise_for_status()
            
            # Extract session ID from cookies
            if 'efm_session_id' in self.session.cookies:
                self.session_id = self.session.cookies['efm_session_id']
                print(f"✅ Router login successful (session: {self.session_id[:8]}...)")
                return True
            else:
                # Check response body
                result = response.json()
                if result.get('result') == 'success' or result.get('error') is None:
                    print("✅ Router login successful")
                    return True
                else:
                    raise Exception(f"Login failed: {result}")
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Router connection failed: {e}")
        except json.JSONDecodeError as e:
            raise Exception(f"Router response parsing failed: {e}")
    
    def send_wol(self, mac_address: str) -> bool:
        """
        Send WOL packet
        
        Args:
            mac_address: MAC address of PC to wake (e.g., 10:FF:E0:38:F4:D5)
            
        Returns:
            True if WOL sent successfully
            
        Raises:
            Exception: WOL transmission failed
        """
        url = f"{self.router_url}/cgi/service.cgi"
        
        headers = {
            'Accept': '*/*',
            'Accept-Language': 'ko;q=0.7',
            'Cache-Control': 'no-store',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json; charset=utf-8',
            'Origin': self.router_url,
            'Referer': f'{self.router_url}/ui/wol',
            'Sec-GPC': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36'
        }
        
        data = {
            "method": "wol/signal",
            "params": [mac_address]
        }
        
        try:
            response = self.session.post(
                url,
                headers=headers,
                json=data,
                verify=False,
                timeout=10
            )
            
            response.raise_for_status()
            
            result = response.json()
            
            # Check success
            if result.get('result') == 'success' or result.get('error') is None:
                print(f"✅ WOL packet sent successfully (MAC: {mac_address})")
                return True
            else:
                raise Exception(f"WOL transmission failed: {result}")
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"WOL packet transmission failed: {e}")
        except json.JSONDecodeError as e:
            raise Exception(f"Router response parsing failed: {e}")
    
    def send_wol_packet(self, mac_address: str):
        """
        Login and send WOL packet (integrated method)
        
        Args:
            mac_address: MAC address of PC to wake
            
        Raises:
            Exception: Login or WOL transmission failed
        """
        print(f"📡 Connecting to router... ({self.router_url})")
        
        # Login
        self.login()
        
        # Send WOL
        print(f"📤 Sending WOL packet... (MAC: {mac_address})")
        self.send_wol(mac_address)

    def get_port_link_status(self):
        """Query router for port link status.

        Returns:
            List of port status dicts as returned by the router, e.g.
            [{"type":"wan","port":1,"link":"1000f"}, {"type":"lan","port":4,"link":"100f"}, ...]
        """
        url = f"{self.router_url}/cgi/service.cgi"

        headers = {
            'Accept': '*/*',
            'Accept-Language': 'ko;q=0.5',
            'Cache-Control': 'no-store',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json; charset=utf-8',
            'Origin': self.router_url,
            'Referer': f'{self.router_url}/ui/port_setup',
            'Sec-GPC': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36'
        }

        data = {
            "method": "port/link/status"
        }

        try:
            response = self.session.post(
                url,
                headers=headers,
                json=data,
                verify=False,
                timeout=10
            )
            response.raise_for_status()
            result = response.json()
            return result.get('result', [])
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to query port link status: {e}")
        except json.JSONDecodeError as e:
            raise Exception(f"Router response parsing failed: {e}")

    @staticmethod
    def _link_value_is_up(link_value: Optional[str]) -> bool:
        """Return True if link_value indicates the port link is up (e.g., '100f', '1000f')."""
        if not link_value:
            return False
        try:
            lv = str(link_value).lower()
            return lv.endswith('f')  # e.g., 10f/100f/1000f
        except Exception:
            return False

    def is_lan_port_up(self, lan_port: int) -> bool:
        """Check if the given LAN port has link up.

        Args:
            lan_port: LAN port number (e.g., 1-4)

        Returns:
            True if link is up
        """
        status_list = self.get_port_link_status()
        for item in status_list:
            try:
                if item.get('type') == 'lan' and int(item.get('port')) == int(lan_port):
                    return self._link_value_is_up(item.get('link'))
            except Exception:
                continue
        return False


# Disable SSL warnings
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
