

# def add_dir(_dir: Directory) -> Hash:
#     """Add directory to ipfs

#     :param _dir: Directory to add to IPFS
#     :return: The resulting CID
#     """
#     directory, path_exists = resolve_root_for(_dir)

#     if not path_exists:  # Check if path exist if not just pin_cid_list
#         raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), directory)

#     # avoid pin by default /reference/http/api/#http-commands
#     # hash needed to encode to bytes16 and hex
#     args = (
#         directory,
#         "--recursive",
#         "--quieter",
#         "--cid-version=1",
#         "--pin=false",
#         "--hash=blake2b-208",
#     )

#     _hash = exec_command("add", *args)
#     return Hash(_hash.strip())

