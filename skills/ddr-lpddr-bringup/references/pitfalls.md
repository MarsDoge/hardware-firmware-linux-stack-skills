# DDR/LPDDR Pitfalls

1. Debugging Linux before training logs and rails are proven.
2. Treating one warm boot as stability. Test cold boot, reboot, suspend/resume, thermal corners.
3. Ignoring board BOM/memory vendor changes.
4. Masking SI/timing issues by lowering speed without root cause.
5. Forgetting ECC/RAS logs when system appears to run.
