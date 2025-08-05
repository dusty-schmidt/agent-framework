import asyncio, json, sys
import websockets

WS_URL = 'ws://localhost:8080/ws/stream'

async def main():
    try:
        async with websockets.connect(WS_URL) as ws:
            print('[GOB] :: WS connected to', WS_URL)
            # Trigger an agent run to generate events
            import urllib.request
            req = urllib.request.Request('http://localhost:8080/agents/run', data=b'{"instruction":"ws smoke test"}', headers={'Content-Type': 'application/json', 'x-correlation-id': 'ws-smoke'}, method='POST')
            with urllib.request.urlopen(req) as resp:
                print('[GOB] :: Triggered agents/run:', resp.read().decode())
            # Read a few messages
            for _ in range(3):
                msg = await ws.recv()
                print('[GOB] :: WS event:', msg)
    except Exception as e:
        print('[GOB] :: WS error:', e)
        sys.exit(1)

if __name__ == '__main__':
    asyncio.run(main())
