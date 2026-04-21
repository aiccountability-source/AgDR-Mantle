// AgDR-Mantle Rust core extension.
//
// In the production build this module links to AgDR-Phoenix (the AKI
// Implementation) and re-exports AKIEngine to Python. This placeholder
// returns deterministic test bytes until Phoenix linkage is wired.

use pyo3::prelude::*;
use pyo3::types::PyAny;
use pyo3::Bound;

#[pyclass]
struct AKIEngine {
    fo_i: String,
}

#[pymethods]
impl AKIEngine {
    #[new]
    fn new(fo_i: String) -> Self {
        AKIEngine { fo_i }
    }

    /// Seal a PPP record. Production version delegates to AgDR-Phoenix.
    fn seal_ppp(&self, _ppp: &Bound<'_, PyAny>) -> PyResult<Vec<u8>> {
        Ok(vec![0xAA, 0xBB, 0xCC])
    }

    #[getter]
    fn fo_i(&self) -> &str {
        &self.fo_i
    }
}

#[pymodule]
fn _core(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<AKIEngine>()?;
    Ok(())
}