# Wake Detection Behavior (v1.2.0)

## New Real-Time Wake Detection

### Flow Diagram

```
[WOL Packet Sent]
        ↓
[Start Monitoring Port Status]
        ↓
┌───────────────────────────────┐
│  Check Every 1 Second         │
│  Maximum 30 Seconds           │
└───────────────────────────────┘
        ↓
    ┌───────┐
    │ Check │ → Port UP? ──YES──→ [Launch MSTSC Immediately] ✅
    └───────┘                     (e.g., after 3 seconds)
        │
        NO
        ↓
    Progress Update
    (every 5 seconds)
        ↓
    Elapsed < 30s?
        │
        ├─ YES → [Check Again]
        │
        └─ NO → [Timeout Error] ❌
                    ↓
              [Prompt User]
              Continue anyway? (y/n)
                    ↓
              ├─ y → [Launch MSTSC]
              └─ n → [Exit]
```

## Example Output

### Fast Boot (3 seconds)
```
📡 Sending WOL packet...
✅ WOL packet sent successfully

⏳ Waiting for PC to wake up (checking port 4 status)...
✅ PC is awake! (port 4 up after 3 seconds)

🖥️  Connecting to Remote Desktop...
```

### Slow Boot (15 seconds)
```
📡 Sending WOL packet...
✅ WOL packet sent successfully

⏳ Waiting for PC to wake up (checking port 4 status)...
   Still waiting... (5/30s)
   Still waiting... (10/30s)
✅ PC is awake! (port 4 up after 15 seconds)

🖥️  Connecting to Remote Desktop...
```

### Timeout (30+ seconds)
```
📡 Sending WOL packet...
✅ WOL packet sent successfully

⏳ Waiting for PC to wake up (checking port 4 status)...
   Still waiting... (5/30s)
   Still waiting... (10/30s)
   Still waiting... (15/30s)
   Still waiting... (20/30s)
   Still waiting... (25/30s)

❌ Timeout: Could not detect PC wake up after 30 seconds
   The PC may still be booting, or WOL may have failed.
   Continue to Remote Desktop anyway? (y/n): 
```

## Configuration Impact

### With LAN Port Configured (Recommended)
- **Monitoring**: Real-time port status checks every 1 second
- **Max Wait**: 30 seconds
- **Connection**: Immediate upon detection
- **Timeout**: Prompt to continue or abort

### Without LAN Port (Port = 0)
- **Wait**: Simple 5-second sleep (legacy behavior)
- **No monitoring**: Assumes PC will be ready
- **Connection**: After 5 seconds

## Benefits

1. **Faster Connections**: No unnecessary waiting if PC boots quickly
2. **Reliable Detection**: Confirms PC is actually awake before connecting
3. **Error Handling**: Clear feedback if WOL fails
4. **User Control**: Option to proceed manually if detection fails
5. **Progress Updates**: Visual feedback during wait
