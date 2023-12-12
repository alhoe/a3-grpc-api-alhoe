from __future__ import print_function

import logging

import grpc
import a3_pb2_grpc

import tester

def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    print("Will try to greet world ...")
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = a3_pb2_grpc.a3Stub(channel)
        print("Stub created")
        response = tester.test(stub)
    print(f"Top Reply under Top Comment: {response}" )


if __name__ == "__main__":
    logging.basicConfig()
    run()
