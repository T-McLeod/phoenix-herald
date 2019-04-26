import unittest
import os
import sys
import responses

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + "/../")
from phoenix.PhoenixParser import PhoenixParser  # noqa: E402

player_url = 'https://herald.playphoenix.online/c'


def file_get_contents(file):
    with open(file) as f:
        return f.read()


class TestRealmRanks(unittest.TestCase):

    @responses.activate
    def test_player_name(self):
        name = "Gorbys"
        expected = "Gorbys"
        responses.add(responses.GET,
                      '{}/{}'.format(player_url, name),
                      body=file_get_contents('./test/fixtures/gorbys.html'),
                      status=200)
        char = PhoenixParser(expected)
        p = char.info
        self.assertEqual(p.player_name, expected)

    @responses.activate
    def test_player_guild(self):
        name = "Gorbys"
        expected = "Svea Bordercontrol"
        responses.add(responses.GET,
                      '{}/{}'.format(player_url, name),
                      body=file_get_contents('./test/fixtures/gorbys.html'),
                      status=200)
        char = PhoenixParser(name)
        p = char.info
        self.assertEqual(p.player_guild, expected)

    @responses.activate
    def test_player_class(self):
        name = "Gorbys"
        expected = "Cleric"
        responses.add(responses.GET,
                      '{}/{}'.format(player_url, name),
                      body=file_get_contents('./test/fixtures/gorbys.html'),
                      status=200)
        char = PhoenixParser(name)
        p = char.info
        self.assertEqual(p.player_class, expected)

    @responses.activate
    def test_player_level(self):
        name = "Gorbys"
        expected = "50"
        responses.add(responses.GET,
                      '{}/{}'.format(player_url, name),
                      body=file_get_contents('./test/fixtures/gorbys.html'),
                      status=200)
        char = PhoenixParser(name)
        p = char.info
        self.assertEqual(p.player_level, expected)

    @responses.activate
    def test_player_rr(self):
        name = "Gorbys"
        expected = "4L6"
        responses.add(responses.GET,
                      '{}/{}'.format(player_url, name),
                      body=file_get_contents('./test/fixtures/gorbys.html'),
                      status=200)
        char = PhoenixParser(name)
        p = char.info
        self.assertEqual(p.player_rr, expected)

    @responses.activate
    def test_player_race(self):
        name = "Gorbys"
        expected = "Briton"
        responses.add(responses.GET,
                      '{}/{}'.format(player_url, name),
                      body=file_get_contents('./test/fixtures/gorbys.html'),
                      status=200)
        char = PhoenixParser(name)
        p = char.info
        self.assertEqual(p.player_race, expected)

    @responses.activate
    def test_player_pretty_rr(self):
        name = "Gorbys"
        expected = "Gryphon Knight"
        responses.add(responses.GET,
                      '{}/{}'.format(player_url, name),
                      body=file_get_contents('./test/fixtures/gorbys.html'),
                      status=200)
        char = PhoenixParser(name)
        p = char.info
        self.assertEqual(p.player_pretty_rr, expected)

    @responses.activate
    def test_get_last_updated(self):
        name = "Gorbys"
        expected = "4/26/19 9:05:45 AM"
        responses.add(responses.GET,
                      '{}/{}'.format(player_url, name),
                      body=file_get_contents('./test/fixtures/gorbys.html'),
                      status=200)
        char = PhoenixParser(name)
        p = char.info
        self.assertEqual(p.last_updated, expected)

    @responses.activate
    def test_get_unknown_player(self):
        with self.assertRaises(Exception):
            name = "Gorbys"
            responses.add(responses.GET,
                          '{}/{}'.format(player_url, name),
                          body=file_get_contents(
                                './test/fixtures/unknown-player.html'),
                          status=200)
            PhoenixParser(name)


if __name__ == '__main__':
    unittest.main()
