# tzutil

This utility finds the current time zone so it can be stashed dynamically against the TZ variable.

It tries, in order:

1. `/etc/timezone`
2. the `/etc/localtime` symlink target
3. `timedatectl show -p Timezone --value`
4. the [`iana-time-zone`](https://docs.rs/iana-time-zone) crate, as a last-resort fallback

## Build & run

```sh
cargo build --release
./target/release/tzutil
```

## Test

```sh
cargo test
```
