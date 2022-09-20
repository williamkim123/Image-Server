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
"""The Python implementation of the GRPC helloworld.Greeter client."""

from __future__ import print_function

import logging

import grpc
import image_pb2
import image_pb2_grpc

import cv2
import numpy as np

from server_tools import decode_image


def run(host='localhost', port=50051, input=None, output=None, rotate=None, mean=None):
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.

    with grpc.insecure_channel(f'{host}:{port}') as channel:
        stub = image_pb2_grpc.NLImageServiceStub(channel)
        # read image as numpy array
        img = cv2.imread(input)

        # create NLI image object
        color = False
        if img.shape[-1] == 3:
            color = True
        image = image_pb2.NLImage(
            color=color, 
            data=img.tobytes(),
            width=img.shape[0],
            height=img.shape[1])

        # create mean request
        if mean:
            # send request to server
            image = stub.MeanFilter(image)

        # create rotate request
        if rotate:
            request = image_pb2.NLImageRotateRequest()
            rotation_enum = {
                'NONE': image_pb2.NLImageRotateRequest.NONE,
                'NINETY_DEG': image_pb2.NLImageRotateRequest.NINETY_DEG,
                'ONE_EIGHTY_DEG': image_pb2.NLImageRotateRequest.ONE_EIGHTY_DEG,
                'TWO_SEVENTY_DEG': image_pb2.NLImageRotateRequest.TWO_SEVENTY_DEG
            }
            
            request = image_pb2.NLImageRotateRequest(
                rotation=rotation_enum[rotate],
                image=image)
            
            # send request to server
            image = stub.RotateImage(request)
    
    processed_image = decode_image(image)
    print(f'...writing file {output}')
    cv2.imwrite(output, processed_image)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', help='specify host id', required=True)
    parser.add_argument('--port', help='specify port number', required=True)
    parser.add_argument('--input', help='', required=True)
    parser.add_argument('--output', help='', required=True)
    parser.add_argument('--rotate', help='', default='NONE', choices=['NONE', 'NINETY_DEG', 'ONE_EIGHTY_DEG', 'TWO_SEVENTY_DEG'])
    parser.add_argument('--mean', help='',action='store_true')
    args = vars(parser.parse_args())
    # logging.basicConfig()
    run(
        host=args['host'],
        port=args['port'],
        input=args['input'], 
        output=args['output'],
        rotate=args['rotate'], 
        mean=args['mean']
        )
    # run(input='sample-image.png', 
    #     output='processed-sample-image.png',
    #     # rotate='TWO_SEVENTY_DEG', 
    #     mean=True
    #     )
