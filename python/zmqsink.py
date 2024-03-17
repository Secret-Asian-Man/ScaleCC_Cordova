#!/usr/bin/env python
# -*- Mode: Python -*-
# vi:si:et:sw=4:sts=4:ts=4

# sinkelement.py
# (c) 2005 Edward Hervey <edward@fluendo.com>
# (c) 2007 Jan Schmidt <jan@fluendo.com>
# Licensed under LGPL
#
# Small test application to show how to write a sink element
# in 20 lines in python and place into the gstreamer registry
# so it can be autoplugged or used from parse_launch.
#
# You can run the example from the source doing from gst-python/:
#
#  $ export GST_PLUGIN_PATH=$GST_PLUGIN_PATH:$PWD/plugin:$PWD/examples/plugins
#  $ GST_DEBUG=python:4 gst-launch-1.0 fakesrc num-buffers=10 ! mysink
import gi
import platform
import sys
import zmq
gi.require_version('GstBase', '1.0')

from gi.repository import Gst, GObject, GstBase
Gst.init(None)
context = zmq.Context()

#
# Simple Sink element created entirely in python
#
class ZmqTextSink(GstBase.BaseSink):
    __gstmetadata__ = ('CustomSink','Sink', 'Sink to ZMQ', 'David Wu, Michael Starch')
    __gproperties__ = {
        "location": (GObject.TYPE_STRING,
                 "Location",
                 "Location of ZMQ binder",
                 "tcp://location:9500",
                 GObject.ParamFlags.READWRITE
                 ),
        "room": (GObject.TYPE_STRING,
                     "Room",
                     "Room to set captions for",
                     "room-101",
                     GObject.ParamFlags.READWRITE
                     ),
    }

    __gsttemplates__ = Gst.PadTemplate.new("sink",
                                           Gst.PadDirection.SINK,
                                           Gst.PadPresence.ALWAYS,
                                           Gst.Caps.from_string("text/x-raw"))

    def __init__(self):
        """ Construct this function """
        self.room = platform.node()
        self.location = None
        self.socket = None

    def do_start(self):
        """ Start the pipeline """
        if self.location is None:
            print("[ERROR] User must set location of ZMQ server", file=sys.stderr)
            return False
        try:
            print(f"[INFO] Connecting to: {self.location}")
            self.socket = context.socket(zmq.PUB)
            self.socket.connect(self.location)
            print(f"[DEBUG] Connected to: {self.location}")
        except Exception as exc:
            print(f"[ERROR] Failed to connect to zmq: {exc}", file=sys.stderr)
            return False
        return True

    def do_set_property(self, prop, value):
        """ Set the location property """
        if prop.name == "location":
            self.location = value
        elif prop.name == "room":
            self.room = value
        else:
            raise AttributeError('unknown property %s' % prop.name)

    def do_render(self, buffer):
        """ Render the buffer"""
        if self.socket is None:
            return
        Gst.info("timestamp(buffer):%s" % (Gst.TIME_ARGS(buffer.pts)))
        text = buffer.extract_dup(0, buffer.get_size())
        self.socket.send_string(f"{self.room} {text.decode()}")
        return Gst.FlowReturn.OK

GObject.type_register(ZmqTextSink)
__gstelementfactory__ = ("zmqtextsink", Gst.Rank.NONE, ZmqTextSink)