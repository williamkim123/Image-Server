# Copyright 2015 gRPC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""The Python implementation of the GRPC helloworld.Greeter server."""

from concurrent import futures
import logging

import grpc
import image_pb2
import image_pb2_grpc

import numpy as np
from server_tools import decode_image, rotate_image, mean_filter


class NLImageServiceServicer(image_pb2_grpc.NLImageServiceServicer):
    def RotateImage(self, request, context):
        print("applying rotation")

        # decode to numpy array in Python
        img = decode_image(request.image)
        img = rotate_image(img, request.rotation)
        
        return image_pb2.NLImage(
            color=request.image.color,
            data=img.tobytes(),
            width=img.shape[0],
            height=img.shape[1]
        )

    def MeanFilter(self, request, context):
        print("applying mean")

        # decode to numpy array in Python
        img = decode_image(request)
        img = mean_filter(img)
        return image_pb2.NLImage(
            color=request.color,
            data=img.tobytes(),
            width=img.shape[0],
            height=img.shape[1]
        )


def serve(host="[::]", port=50051):
    print("Running server")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    image_pb2_grpc.add_NLImageServiceServicer_to_server(NLImageServiceServicer(), server)
    server.add_insecure_port(f'{host}:{port}')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default='[::]', help='specify host id')
    parser.add_argument('--port', default=50051, help='specify port number')
    args = vars(parser.parse_args())
    # logging.basicConfig()
    serve(args['host'], args['port'])

    serve()
