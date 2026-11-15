"""Run offline schema and export regression tests."""
import copy
import unittest
from validar_especies import load, validate_schema, main as validate_all
from exportar_especies_web import export_species

class SpeciesSchemaTests(unittest.TestCase):
    def setUp(self):
        self.species = load("especies.csv")
        self.records = {r["id"]: r for r in self.species}
        self.base = copy.deepcopy(self.records["anchoveta"])

    def fails(self, record, message):
        self.assertTrue(any(message in e for e in validate_schema(record)), validate_schema(record))

    def test_current_records_and_existing_rules(self):
        self.assertEqual(validate_all(), 0)
        for record in self.species:
            self.assertEqual(validate_schema(record), [])

    def test_temperature_basis_required_for_either_endpoint(self):
        for endpoint in ("temperature_min_c", "temperature_max_c"):
            r = {"id":"test", endpoint:"14"}
            self.fails(r, "temperature_basis required")

    def test_invalid_temperature_basis(self):
        self.base["temperature_basis"] = "unknown"
        self.fails(self.base, "invalid temperature_basis")

    def test_comparison_disabled_for_mixed_and_lab(self):
        for sid in ("pota", "concha_abanico"):
            r = copy.deepcopy(self.records[sid])
            r["temperature_comparable"] = "true"
            self.fails(r, "temperature_comparable cannot be true")
            r["temperature_comparable"] = "false"
            self.assertEqual(validate_schema(r), [])

    def test_depth_basis_required_for_either_endpoint(self):
        for endpoint in ("depth_min_m", "depth_max_m"):
            self.fails({"id":"test", endpoint:"0"}, "depth_basis required")

    def test_warning_requires_recorded_context_and_not_limits(self):
        for note in ("", "Field observations.", "Not limits.", "Field observations are limits."):
            self.base["temperature_note"] = note
            self.fails(self.base, "temperature_note must describe")
        self.base["temperature_note"] = "Field observations, not limits."
        self.assertEqual(validate_schema(self.base), [])

    def test_allowed_depth_bases_and_boolean(self):
        for basis in ("distribution_range", "dive_depth_observation", "survey_stratum"):
            self.base["depth_basis"] = basis
            self.assertEqual(validate_schema(self.base), [])
        self.base["depth_basis"] = "unknown"
        self.fails(self.base, "invalid depth_basis")
        self.base["temperature_comparable"] = "yes"
        self.fails(self.base, "must be true or false")

    def test_export(self):
        result = {r["id"]:r for r in export_species(self.species, load("especies_fuentes.csv"))}
        for sid in ("concha_abanico", "pota"):
            t = result[sid]["recorded_temperature"]
            self.assertIs(t["use_in_comparison"], False)
            self.assertIs(t["comparable"], False)
            self.assertTrue(t["caveat"])
        for sid in ("anchoveta", "pulpo", "merluza"):
            self.assertIs(result[sid]["recorded_temperature"]["comparable"], True)
        self.assertIsNone(result["cachema"]["recorded_temperature"]["min"])
        self.assertEqual(result["pota"]["recorded_depth"]["label"], "Deepest recorded dive")
        for sid, row in result.items():
            for kind, prefix in (("recorded_temperature", "temperature"), ("recorded_depth", "depth")):
                for endpoint in ("min", "max"):
                    original = self.records[sid][f"{prefix}_{endpoint}_{'c' if prefix == 'temperature' else 'm'}"]
                    self.assertEqual(row[kind][endpoint], float(original) if original else None)
        def check_keys(value):
            if isinstance(value, dict):
                for key, child in value.items():
                    self.assertFalse(any(word in key.lower() for word in ("preferred", "optimum", "suitability")))
                    check_keys(child)
            elif isinstance(value, list):
                for child in value: check_keys(child)
        check_keys(list(result.values()))

if __name__ == "__main__":
    unittest.main(verbosity=2)
