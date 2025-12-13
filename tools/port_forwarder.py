#!/usr/bin/env python3
import asyncio
import logging

MAPPINGS = [
    (4377, '127.0.0.1', 8501),
    (3271, '127.0.0.1', 8502),
    (3413, '127.0.0.1', 8501),
]


async def handle_client(local_reader, local_writer, remote_host, remote_port):
    try:
        remote_reader, remote_writer = await asyncio.open_connection(remote_host, remote_port)
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


async def start_forward(local_port, remote_host, remote_port):
    server = await asyncio.start_server(lambda r, w: handle_client(r, w, remote_host, remote_port), '0.0.0.0', local_port)
    logging.info(f'Forwarding 0.0.0.0:{local_port} -> {remote_host}:{remote_port}')
    async with server:
        await server.serve_forever()


async def main():
    logging.basicConfig(level=logging.INFO)
    tasks = []
    for local, host, remote in MAPPINGS:
        tasks.append(asyncio.create_task(start_forward(local, host, remote)))
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
