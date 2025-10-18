#![forbid(unsafe_code)]
//! dsg: Minimal Energy Control (MEC) crate.
//! Architect: Alexis Adams (@devdollzai)

/// Health check function - returns crate identifier
pub fn ping() -> &'static str {
    "dsg::ok"
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn ping_ok() {
        assert_eq!(ping(), "dsg::ok");
    }
}