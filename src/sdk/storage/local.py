from .types import Storable

def pin(media: Storable):
    ...


# def pin_cid(cid_list: iter, remote: bool):
#     """Pin CID into Local/Remote node from list

#     :param cid_list: List of cid to pin
#     :param remote: Pin in remote edge node if true
#     :return: cid list after pin
#     """
#     for cid in cid_list:
#         logger.log.notice(f"Pinning cid: {cid}")
#         pin(cid) if not remote else remote_pin(cid)
#     return cid_list
