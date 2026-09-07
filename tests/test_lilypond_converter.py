"""Unit tests for LilyPond converter (json_to_lilypond)."""

import json
import os
import unittest
from src.utils.lilypond_converter import (
    midi_to_lilypond_pitch,
    ticks_to_lilypond_duration,
    ticks_to_spacers,
    process_element,
    json_to_lilypond
)

class TestLilyPondConverter(unittest.TestCase):

    def test_midi_to_lilypond_pitch(self):
        # Middle C
        self.assertEqual(midi_to_lilypond_pitch(60, 14), "c'")
        # Octaves
        self.assertEqual(midi_to_lilypond_pitch(48, 14), "c")
        self.assertEqual(midi_to_lilypond_pitch(36, 14), "c,")
        self.assertEqual(midi_to_lilypond_pitch(72, 14), "c''")
        self.assertEqual(midi_to_lilypond_pitch(84, 14), "c'''")

        # Accidentals via TPC
        self.assertEqual(midi_to_lilypond_pitch(66, 20), "fis'")
        self.assertEqual(midi_to_lilypond_pitch(70, 12), "bes'")
        self.assertEqual(midi_to_lilypond_pitch(61, 21), "cis'")
        self.assertEqual(midi_to_lilypond_pitch(61, 9), "des'")

    def test_ticks_to_lilypond_duration(self):
        self.assertEqual(ticks_to_lilypond_duration(1920), "1")
        self.assertEqual(ticks_to_lilypond_duration(1440), "2.")
        self.assertEqual(ticks_to_lilypond_duration(960), "2")
        self.assertEqual(ticks_to_lilypond_duration(720), "4.")
        self.assertEqual(ticks_to_lilypond_duration(480), "4")
        self.assertEqual(ticks_to_lilypond_duration(240), "8")
        self.assertEqual(ticks_to_lilypond_duration(120), "16")

    def test_ticks_to_spacers(self):
        self.assertEqual(ticks_to_spacers(480), ["s4"])
        self.assertEqual(ticks_to_spacers(960), ["s2"])
        self.assertEqual(ticks_to_spacers(1440), ["s2."])
        self.assertEqual(ticks_to_spacers(0), [])

    def test_process_element_rest(self):
        el = {"name": "Rest", "durationTicks": 480}
        lily, lyric = process_element(el)
        self.assertEqual(lily, "r4")
        self.assertEqual(lyric, "")

    def test_process_element_chord(self):
        # Single note chord
        el_single = {
            "name": "Chord",
            "durationTicks": 480,
            "notes": [{"pitchMidi": 60, "tpc": 14}]
        }
        lily, lyric = process_element(el_single)
        self.assertEqual(lily, "c'4")
        self.assertEqual(lyric, "_")

        # Multi-note chord
        el_chord = {
            "name": "Chord",
            "durationTicks": 960,
            "notes": [
                {"pitchMidi": 60, "tpc": 14},
                {"pitchMidi": 64, "tpc": 18},
                {"pitchMidi": 67, "tpc": 15}
            ]
        }
        lily, lyric = process_element(el_chord)
        self.assertEqual(lily, "<c' e' g'>2")

    def test_process_element_signatures(self):
        el_time = {"name": "TimeSig", "timesig": "4/4"}
        lily, _ = process_element(el_time)
        self.assertEqual(lily, "\\time 4/4")

        el_key = {"name": "KeySig", "key": 2}
        lily, _ = process_element(el_key)
        self.assertEqual(lily, "\\key d \\major")

    def test_json_to_lilypond_with_fixture(self):
        fixture_path = os.path.join(os.path.dirname(__file__), "fixtures", "score_dump.json")
        if not os.path.exists(fixture_path):
            self.skipTest(f"Fixture {fixture_path} not found")

        with open(fixture_path, "r", encoding="utf-8") as f:
            dump_data = json.load(f)

        score_analysis = dump_data.get("result", {}).get("analysis", {})
        self.assertTrue(score_analysis, "Analysis data should not be empty")

        output = json_to_lilypond(score_analysis)
        self.assertIsInstance(output, str)
        self.assertTrue(output.startswith("<<"))
        self.assertTrue(output.endswith(">>"))
        self.assertIn("\\new Staff", output)
        self.assertIn("\\new Voice", output)

    def test_json_to_lilypond_edge_cases(self):
        # Empty input
        self.assertEqual(json_to_lilypond({}), "<<\n>>")

        # Missing optional fields
        sparse_data = {
            "staves": [{"name": "Staff1", "visible": True}],
            "measures": [
                {
                    "measure": 1,
                    "elements": {
                        "Staff1": [
                            {"name": "Chord", "durationTicks": 480, "notes": []},
                            {"name": "UnknownElement"}
                        ]
                    }
                }
            ]
        }
        output = json_to_lilypond(sparse_data)
        self.assertIsInstance(output, str)
        self.assertIn("r4", output)


if __name__ == "__main__":
    unittest.main()
