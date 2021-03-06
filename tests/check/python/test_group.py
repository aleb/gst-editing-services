# -*- coding: utf-8 -*-
#
# Copyright (c) 2015, Thibault Saunier
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the
# Free Software Foundation, Inc., 51 Franklin St, Fifth Floor,
# Boston, MA 02110-1301, USA.

import gi

gi.require_version("Gst", "1.0")
gi.require_version("GES", "1.0")

from gi.repository import Gst  # noqa
from gi.repository import GES  # noqa
import unittest  # noqa

Gst.init(None)
GES.init()


class TestGroup(unittest.TestCase):

    def setUp(self):
        self.timeline = GES.Timeline.new_audio_video()
        self.assertEqual(len(self.timeline.get_tracks()), 2)
        self.layer = self.timeline.append_layer()

    def testCopyGroup(self):
        clip1 = GES.TestClip.new()
        clip1.props.duration = 10

        self.layer.add_clip(clip1)

        self.assertEqual(len(clip1.get_children(False)), 2)

        group = GES.Group.new()
        self.assertTrue(group.add(clip1))

        self.assertEqual(len(group.get_children(False)), 1)

        group_copy = group.copy(True)
        self.assertEqual(len(group_copy.get_children(False)), 0)

        self.assertTrue(group_copy.paste(10))
        clips = self.layer.get_clips()
        self.assertEqual(len(clips), 2)
        self.assertEqual(clips[1].props.start, 10)

        clips[1].edit([], 1, GES.EditMode.EDIT_NORMAL, GES.Edge.EDGE_NONE, 10)
        clips = self.layer.get_clips()
        self.assertEqual(len(clips), 1)

    def testPasteChangedGroup(self):
        clip1 = GES.TestClip.new()
        clip1.props.duration = 10

        clip2 = GES.TestClip.new()
        clip2.props.start = 20
        clip2.props.duration = 10

        self.layer.add_clip(clip1)
        self.layer.add_clip(clip2)

        self.assertEqual(len(clip1.get_children(False)), 2)

        group = GES.Group.new()
        self.assertTrue(group.add(clip1))

        self.assertEqual(len(group.get_children(False)), 1)

        group_copy = group.copy(True)
        self.assertEqual(len(group_copy.get_children(False)), 0)

        self.assertTrue(group.add(clip2))
        self.assertEqual(len(group.get_children(False)), 2)
        self.assertEqual(len(group_copy.get_children(False)), 0)

        self.assertTrue(group_copy.paste(10))
        clips = self.layer.get_clips()
        self.assertEqual(len(clips), 3)
        self.assertEqual(clips[1].props.start, 10)

    def testPasteChangedGroup(self):
        clip1 = GES.TestClip.new()
        clip1.props.duration = 10

        clip2 = GES.TestClip.new()
        clip2.props.start = 20
        clip2.props.duration = 10

        self.layer.add_clip(clip1)
        self.layer.add_clip(clip2)

        self.assertEqual(len(clip1.get_children(False)), 2)

        group = GES.Group.new()
        self.assertTrue(group.add(clip1))

        self.assertEqual(len(group.get_children(False)), 1)

        group_copy = group.copy(True)
        self.assertEqual(len(group_copy.get_children(False)), 0)

        self.assertTrue(group.add(clip2))
        self.assertEqual(len(group.get_children(False)), 2)
        self.assertEqual(len(group_copy.get_children(False)), 0)

        self.assertTrue(group_copy.paste(10))
        clips = self.layer.get_clips()
        self.assertEqual(len(clips), 3)
        self.assertEqual(clips[1].props.start, 10)

    def test_move_clips_between_layers_with_auto_transition(self):
        self.timeline.props.auto_transition = True
        layer2 = self.timeline.append_layer()
        clip1 = GES.TestClip.new()
        clip1.props.start = 0
        clip1.props.duration = 30

        clip2 = GES.TestClip.new()
        clip2.props.start = 20
        clip2.props.duration = 20

        self.layer.add_clip(clip1)
        self.layer.add_clip(clip2)

        clips = self.layer.get_clips()
        self.assertEqual(len(clips), 4)
        self.assertEqual(layer2.get_clips(), [])

        group = GES.Container.group(clips)
        self.assertIsNotNone(group)

        self.assertTrue(clip1.edit(
            self.timeline.get_layers(), 1, GES.EditMode.EDIT_NORMAL, GES.Edge.EDGE_NONE, 0))
        self.assertEqual(self.layer.get_clips(), [])

        clips = layer2.get_clips()
        self.assertEqual(len(clips), 4)
