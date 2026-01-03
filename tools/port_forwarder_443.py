# ------------------------------------------------------------------------------
# Copyright (c) 2025 iLuminara (VISENDI56). All Rights Reserved.
# Licensed under the Polyform Shield License 1.0.0.
# 
# COMPETITOR EXCLUSION: Commercial use by entities offering Sovereign/Health OS 
# solutions is STRICTLY PROHIBITED without a commercial license.
# 
# The Sovereign Immune System (Omni-Law) and JEPA-MPC Architecture are 
# proprietary inventions of iLuminara.
# ------------------------------------------------------------------------------

#!/usr/bin/env python3
import asyncio
import logging

LOCAL_PORT = 443
REMOTE_HOST = '127.0.0.1'
REMOTE_PORT = 8503

async def handle_client(local_reader, local_writer):
    try:
        remote_reader, remote_writer = await asyncio.open_connection(REMOTE_HOST, REMOTE_PORT)
    except Exception as e:
        logging.exception('Failed to connect to remote')
        local_writer.close()
        await local_writer.wait_closed()
        return

    async def pipe(reader, writer):
        try:
            while True:
                data = await reader.read(4096)
                if not data:
                    break
                writer.write(data)
                await writer.drain()
        except Exception:
            pass
        finally:
            try:
                writer.close()
            except Exception:
                pass

    await asyncio.gather(pipe(local_reader, remote_writer), pipe(remote_reader, local_writer))


async def main():
    logging.basicConfig(level=logging.INFO)
    try:
        server = await asyncio.start_server(handle_client, '0.0.0.0', LOCAL_PORT)
    except Exception as e:
        logging.exception(f'Failed to bind to port {LOCAL_PORT}')
        return

    logging.info(f'Forwarding 0.0.0.0:{LOCAL_PORT} -> {REMOTE_HOST}:{REMOTE_PORT}')
    async with server:
        await server.serve_forever()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
