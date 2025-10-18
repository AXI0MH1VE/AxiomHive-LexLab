#![forbid(unsafe_code)]
//! ahn: Minimal Energy Control (MEC) crate.
//! Architect: Alexis Adams (@devdollzai)

/// Health check function - returns crate identifier
pub fn ping() -> &'static str {
    "ahn::ok"
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn ping_ok() {
        assert_eq!(ping(), "ahn::ok");
    }
}