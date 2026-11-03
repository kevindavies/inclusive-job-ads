"""Tests for decode.py. Run: python3 -m unittest discover tests"""
import importlib.util
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location(
    "decode", ROOT / "inclusive-job-ads" / "scripts" / "decode.py")
decode = importlib.util.module_from_spec(spec)
spec.loader.exec_module(decode)


def words_in(result, key):
    return [h["word"] for h in result[key]]


class WordLists(unittest.TestCase):
    def test_sea_of_dudes_counts(self):
        r = decode.analyse((ROOT / "examples" / "sea-of-dudes.md").read_text())
        self.assertEqual(r["raw"]["communal"], 0)
        self.assertEqual(r["raw"]["agentic"], 15)
        self.assertEqual(r["raw"]["gender_decoder_label"], "strongly masculine-coded")

    def test_each_word_counts_once(self):
        # "dominant" matches two stems; the Gender Decoder counts it twice.
        r = decode.analyse("A dominant personality.")
        self.assertEqual(r["raw"]["agentic"], 1)

    def test_sharepoint_is_not_communal(self):
        self.assertEqual(decode.analyse("SharePoint admin")["raw"]["communal"], 0)

    def test_non_breaking_hyphen(self):
        r = decode.analyse("Self‑reliant and co‑operative")
        self.assertIn("self-reliant", words_in(r, "agentic_hits"))
        self.assertIn("co-operative", words_in(r, "communal_hits"))

    def test_empty(self):
        self.assertEqual(decode.analyse("")["raw"]["lean"], "no trait words found")


class FixedTerms(unittest.TestCase):
    def test_fixed_terms_are_tagged_not_dropped(self):
        r = decode.analyse("Competitive salary. Join our customer support team.")
        hits = r["agentic_hits"] + r["communal_hits"]
        self.assertEqual(len(hits), 2)
        self.assertTrue(all("check" in h for h in hits))
        self.assertEqual(r["script_adjusted"]["lean"], "no trait words found")

    def test_trait_use_is_kept(self):
        r = decode.analyse("You are competitive and supportive.")
        self.assertFalse(any("check" in h for h in r["agentic_hits"] + r["communal_hits"]))

    def test_lead_generation_vs_leading_a_team(self):
        r = decode.analyse("Own lead generation.\nYou will lead a team of four.")
        tagged = [h["line"] for h in r["agentic_hits"] if "check" in h]
        kept = [h["line"] for h in r["agentic_hits"] if "check" not in h]
        self.assertEqual(tagged, [1])
        self.assertEqual(kept, [2])


class Nouns(unittest.TestCase):
    def test_noun_uses_are_tagged(self):
        r = decode.analyse("We help independent cafés. Salary: competitive. Business decisions.")
        self.assertTrue(all("check" in h for h in r["agentic_hits"]))

    def test_summary_runs(self):
        self.assertIn("Script-adjusted", decode.summary(decode.analyse("A driven leader. £30k-£35k")))


class Pay(unittest.TestCase):
    def test_two_different_ranges(self):
        r = decode.analyse("Salary: £30k – £40k\n...\nAn attractive salary from £35–45K")
        self.assertTrue(r["pay"]["more_than_one_salary_figure"])
        self.assertEqual(len(r["pay"]["mentions"]), 2)

    def test_one_range_said_twice(self):
        r = decode.analyse("£40,000 to £48,000\nWe pay £40,000 to £48,000.")
        self.assertFalse(r["pay"]["more_than_one_salary_figure"])

    def test_no_figure(self):
        r = decode.analyse("Competitive salary, depending on experience.")
        self.assertTrue(r["pay"]["no_salary_figure"])
        self.assertEqual(len(r["pay"]["mentions"]), 1)

    def test_small_amounts_are_not_salary(self):
        r = decode.analyse("A learning budget of £1,000 a year")
        self.assertTrue(r["pay"]["no_salary_figure"])

    def test_same_range_written_two_ways(self):
        r = decode.analyse("£35k to £45k\nAn attractive salary of £35k–£45k")
        self.assertFalse(r["pay"]["more_than_one_salary_figure"])

    def test_negotiable(self):
        self.assertTrue(decode.analyse("£40k-£48k, negotiable")["pay"]["says_negotiable"])


if __name__ == "__main__":
    unittest.main()
