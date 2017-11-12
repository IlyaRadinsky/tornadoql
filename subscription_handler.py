# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

from collections import OrderedDict
from graphql import graphql, format_error
from tornado import websocket
from tornado.escape import json_decode, json_encode
from tornado.log import app_log
from rx import Observer, Observable


GRAPHQL_WS = 'graphql-ws'
WS_PROTOCOL = GRAPHQL_WS

GQL_CONNECTION_INIT = 'connection_init'  # Client -> Server
GQL_CONNECTION_ACK = 'connection_ack'  # Server -> Client
GQL_CONNECTION_ERROR = 'connection_error'  # Server -> Client

# NOTE: This one here don't follow the standard due to connection optimization
GQL_CONNECTION_TERMINATE = 'connection_terminate'  # Client -> Server
GQL_CONNECTION_KEEP_ALIVE = 'ka'  # Server -> Client
GQL_START = 'start'  # Client -> Server
GQL_DATA = 'data'  # Server -> Client
GQL_ERROR = 'error'  # Server -> Client
GQL_COMPLETE = 'complete'  # Server -> Client
GQL_STOP = 'stop'  # Client -> Server


class SubscriptionObserver(Observer):

    def __init__(self, op_id, send_execution_result, send_error, on_close):
        self.op_id = op_id
        self.send_execution_result = send_execution_result
        self.send_error = send_error
        self.on_close = on_close

    def on_next(self, value):
        self.send_execution_result(self.op_id, value)

    def on_completed(self):
        self.on_close()

    def on_error(self, error):
        self.send_error(self.op_id, error)


class GQLSubscriptionHandler(websocket.WebSocketHandler):

    @property
    def schema(self):
        raise NotImplementedError('schema must be provided')

    @property
    def sockets(self):
        raise NotImplementedError('sockets() must be implemented')

    def select_subprotocol(self, subprotocols):
        return WS_PROTOCOL

    def send_message(self, op_id=None, op_type=None, payload=None):
        message = {}
        if op_id is not None:
            message['id'] = op_id
        if op_type is not None:
            message['type'] = op_type
        if payload is not None:
            message['payload'] = payload

        assert message, "You need to send at least one thing"
        json_message = json_encode(message)
        return self.write_message(json_message)

    def send_error(self, op_id, error, error_type=None):
        if error_type is None:
            error_type = GQL_ERROR

        assert error_type in [GQL_CONNECTION_ERROR, GQL_ERROR], (
            'error_type should be one of the allowed error messages'
            ' GQL_CONNECTION_ERROR or GQL_ERROR'
        )

        error_payload = {
            'message': str(error)
        }

        return self.send_message(
            op_id,
            error_type,
            error_payload
        )

    def send_execution_result(self, op_id, execution_result):
        result = self.execution_result_to_dict(execution_result)
        return self.send_message(op_id, GQL_DATA, result)

    def execution_result_to_dict(self, execution_result):
        result = OrderedDict()
        if execution_result.data:
            result['data'] = execution_result.data
        if execution_result.errors:
            result['errors'] = [format_error(error)
                                for error in execution_result.errors]
        return result

    def get_graphql_params(self, payload):
        return {
            'request_string': payload.get('query'),
            'variable_values': payload.get('variables'),
            'operation_name': payload.get('operationName'),
            'context_value': payload.get('context'),
        }

    def open(self):
        app_log.info('open socket %s', self)
        self.sockets.append(self)

    def on_close(self):
        app_log.info('close socket %s', self)
        self.sockets.remove(self)

    def on_message(self, message):
        parsed_message = json_decode(message)
        op_id = parsed_message.get('id')
        op_type = parsed_message.get('type')
        payload = parsed_message.get('payload')

        if op_type == GQL_CONNECTION_INIT:
            return self.on_connection_init(op_id, payload)

        elif op_type == GQL_CONNECTION_TERMINATE:
            return self.on_connection_terminate(op_id)

        elif op_type == GQL_START:
            assert isinstance(payload, dict), "The payload must be a dict"

            params = self.get_graphql_params(payload)
            if not isinstance(params, dict):
                error = Exception(
                    "Invalid params returned from get_graphql_params! return values must be a dict.")
                return self.send_error(op_id, error)

            return self.on_start(op_id, params)

        elif op_type == GQL_STOP:
            return self.on_stop(op_id)

        else:
            return self.send_error(op_id,
                                   Exception('Invalid message type: {}.'.format(op_type)))

    def on_connection_init(self, op_id, payload):
        self.send_message(op_type=GQL_CONNECTION_ACK)

    def on_connection_terminate(self, op_id):
        self.close(code=1011)

    def on_start(self, op_id, params):
        try:
            execution_result = graphql(
                self.schema, **params, allow_subscriptions=True
            )
            assert isinstance(
                execution_result, Observable), "A subscription must return an observable"
            execution_result.subscribe(SubscriptionObserver(
                    op_id,
                    self.send_execution_result,
                    self.send_error,
                    self.on_close
                )
            )
        except Exception as e:
            self.send_error(op_id, str(e))

    def on_stop(self, op_id):
        pass
