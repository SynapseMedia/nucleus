# import pytest
# from src.sdk.scheme import util
# from marshmallow.exceptions import ValidationError

# cid = "bafyjvzacdiboycugrim5jwmqc2si7f5p2c4d27panotak6t4coma"
# hls_dag = {
#     "Links": [
#         {"Name": "hls"},
#     ]
# }

# expected_hls_output = {
#     "route": cid,
#     "index": {
#         "hls": "/movie/hls/index.m3u8",
#     },
# }

# image_dag = {
#     "Links": [
#         {"Name": "small.jpg"},
#         {"Name": "medium.jpg"},
#         {"Name": "large.jpg"},
#     ]
# }

# expected_image_output = {
#     "route": cid,
#     "index": {
#         "small": "/image/small.jpg",
#         "medium": "/image/medium.jpg",
#         "large": "/image/large.jpg",
#     },
# }


# # Unit tests
# def test_fit_image_from_dag(mocker):
#     """Should return valid image scheme fit for MediaScheme"""

#     mocker.patch("src.sdk.scheme.util.dag_get", return_value=image_dag)
#     assert util.fit_image_from_dag(cid) == expected_image_output


# # Unit tests
# def test_fit_video_hls_from_dag(mocker):
#     """Should return valid video scheme fit for MediaScheme hls"""

#     mocker.patch("src.sdk.scheme.util.dag_get", return_value=hls_dag)
#     assert util.fit_video_from_dag(cid) == expected_hls_output


# # Unit tests
# def test_fit_video_dash_from_dag(mocker):
#     """Should return valid video scheme fit for MediaScheme dash"""

#     dash_dag = {
#         "Links": [
#             {"Name": "dash"},
#         ]
#     }

#     expected_dash_output = {
#         "route": cid,
#         "index": {
#             "dash": "/movie/dash/index.mpd",
#         },
#     }

#     mocker.patch("src.sdk.scheme.util.dag_get", return_value=dash_dag)
#     assert util.fit_video_from_dag(cid) == expected_dash_output


# # Unit tests
# def test_multimedia_resources_from_dag(mocker):
#     """Should return valid scheme fit for MultiMediaScheme"""

#     mocker.patch(
#         "src.sdk.scheme.util.fit_video_from_dag",
#         return_value=expected_hls_output,
#     )
#     mocker.patch(
#         "src.sdk.scheme.util.fit_image_from_dag",
#         return_value=expected_image_output,
#     )

#     assert util.multimedia_resources_from_dag(cid)


# # Unit tests
# def test_fail_multimedia_resources_from_dag(mocker):
#     """Should fail with invalid scheme fit for MultiMediaScheme"""

#     mocker.patch(
#         "src.sdk.scheme.util.fit_video_from_dag",
#         return_value=expected_hls_output.pop("route"),
#     )
#     mocker.patch(
#         "src.sdk.scheme.util.fit_image_from_dag",
#         return_value=expected_image_output,
#     )

#     with pytest.raises(ValidationError):
#         assert util.multimedia_resources_from_dag(cid)
