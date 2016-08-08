# -*- coding: utf-8 -*-
from __future__ import unicode_literals


class EventNotRegisteredException(Exception):
    pass


class EventMalformedException(Exception):
    pass


class EventHandler(object):

    def __init__(self):
        pass

    def initialize(self):
        pass

    def handle_event(self, event, kwargs):
        raise NotImplementedError("Please implement")


class EventManager(object):

    def __init__(self, *handlers):
        self._registered_events = dict()
        self._handlers = []
        if handlers:
            for handler in handlers:
                self.add_handler(handler)

    def event_report(self):
        for event, (color, parameters) in self._registered_events.iteritems():
            print '-'*80
            print 'Event: {}'.format(event)
            if parameters:
                print 'Parameters:'
                for parameter in parameters:
                    print '* {}'.format(parameter)

    def add_handler(self, event_handler):
        self._handlers.append(event_handler)
        event_handler.initialize()

    def register_event(self, name, color='white', parameters=[]):
        self._registered_events[name] = (color, parameters)

    def emit(self, event, sender=None, level='info', formatted='', data={}):
        if not sender:
            raise ArgumentError('Event needs a sender!')

        levels = ['info', 'warning', 'error', 'critical', 'debug']
        if not level in levels:
            raise ArgumentError('Event level needs to be in: {}'.format(levels))

        if event not in self._registered_events:
            raise EventNotRegisteredException("Event %s not registered..." % event)

        # verify params match event
        color, parameters = self._registered_events[event]
        if parameters:
            for k, v in data.iteritems():
                if k not in parameters:
                    raise EventMalformedException("Event %s does not require parameter %s" % (event, k))

        formatted_msg = formatted.format(**data)

        # send off to the handlers
        for handler in self._handlers:
            handler.handle_event(event, sender, level, formatted_msg, data, color=color)
