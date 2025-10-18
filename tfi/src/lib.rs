#![forbid(unsafe_code)]
//! tfi: Minimal Energy Control (MEC) crate.
//! Architect: Alexis Adams (@devdollzai)

/// Health check function - returns crate identifier
pub fn ping() -> &'static str {
    "tfi::ok"
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn ping_ok() {
        assert_eq!(ping(), "tfi::ok");
    }
}