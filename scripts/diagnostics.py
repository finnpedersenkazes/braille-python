import brlapi
import sys

# Try several possible brlapi Python APIs in a tolerant way so this
# script works across distributions and versions. It will print what
# it attempted and any errors encountered.
conn = brlapi.Connection()
opened = False
for open_name in ('open', 'connect', 'brlapi_open', 'openConnection'):
	if hasattr(conn, open_name):
		try:
			getattr(conn, open_name)()
			print(f"Opened connection using: {open_name}")
			opened = True
			break
		except Exception as e:
			print(f"Attempt {open_name} failed: {e}")

if not opened:
	# try module-level helpers
	for func in ('open', 'openConnection', 'connect'):
		if hasattr(brlapi, func):
			try:
				getattr(brlapi, func)(conn)
				print(f"Opened connection using brlapi.{func}")
				opened = True
				break
			except Exception as e:
				print(f"Attempt brlapi.{func} failed: {e}")

if not opened:
	print('Could not open brlapi connection. Connection object methods:', dir(conn))
	sys.exit(1)

# Try common write methods
written = False
for write_name in ('writeText', 'brlapi_writeText', 'write_text', 'write'):
	if hasattr(conn, write_name):
		try:
			getattr(conn, write_name)("Hello, Brailliant\n")
			print(f"Wrote text using: {write_name}")
			written = True
			break
		except Exception as e:
			print(f"Attempt {write_name} failed: {e}")

if not written:
	print('No known write method succeeded. Connection object methods:', dir(conn))

try:
	if hasattr(conn, 'close'):
		conn.close()
	elif hasattr(conn, 'disconnect'):
		conn.disconnect()
	else:
		print('No close/disconnect method found on connection object')
except Exception as e:
	print('Error closing connection:', e)