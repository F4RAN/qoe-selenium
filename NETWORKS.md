Each configs contains 2 blocks '-incoming' and '-outgoing' in your config.txt file you should use this keys or leave it empty at all ( In the windows systems )


**4G Profiles with Jitter:**

Good 4G with Jitter:

```md
-incoming
delay 20ms
delay-distro 5ms
loss 0%
rate 10Mbps
-outgoing
delay 20ms
delay-distro 5ms
loss 0%
rate 5Mbps
```

Medium 4G with Jitter:

```md
-incoming
delay 40ms
delay-distro 10ms
loss 1%
rate 5Mbps
-outgoing
delay 40ms
delay-distro 10ms
loss 1%
rate 2.5Mbps
```

Poor 4G with Jitter:

```md
-incoming
delay 60ms
delay-distro 15ms
loss 2%
rate 2.5Mbps
-outgoing
delay 60ms
delay-distro 15ms
loss 2%
rate 1.25Mbps
```

**3G Profiles with Jitter:**

Good 3G with Jitter:

```md
-incoming
delay 30ms
delay-distro 7ms
loss 0%
rate 1Mbps
-outgoing
delay 30ms
delay-distro 7ms
loss 0%
rate 500Kbps
```

Medium 3G with Jitter:

```md
-incoming
delay 60ms
delay-distro 15ms
loss 1%
rate 500Kbps
-outgoing
delay 60ms
delay-distro 15ms
loss 1%
rate 250Kbps
```

Poor 3G with Jitter:

```md
-incoming
delay 90ms
delay-distro 22ms
loss 2%
rate 250Kbps
-outgoing
delay 90ms
delay-distro 22ms
loss 2%
rate 125Kbps
```

**2G Profiles with Jitter:**

Good 2G with Jitter:

```md
-incoming
delay 100ms
delay-distro 25ms
loss 0%
rate 200Kbps
-outgoing
delay 100ms
delay-distro 25ms
loss 0%
rate 100Kbps
```

Medium 2G with Jitter:

```md
-incoming
delay 200ms
delay-distro 50ms
loss 2%
rate 100Kbps
-outgoing
delay 200ms
delay-distro 50ms
loss 2%
rate 50Kbps
```

Poor 2G with Jitter:

```md
-incoming
delay 300ms
delay-distro 75ms
loss 4%
rate 50Kbps
-outgoing
delay 300ms
delay-distro 75ms
loss 4%
rate 25Kbps
```

**DSL Profiles with Jitter:**

Good DSL with Jitter:

```md
-incoming
delay 40ms
delay-distro 10ms
loss 3%
rate 2Mbps
-outgoing
delay 40ms
delay-distro 10ms
loss 3%
rate 1Mbps
```

Medium DSL with Jitter:

```md
-incoming
delay 80ms
delay-distro 20ms
loss 5%
rate 1Mbps
-outgoing
delay 80ms
delay-distro 20ms
loss 5%
rate 500Kbps
```

Poor DSL with Jitter:

```md
-incoming
delay 120ms
delay-distro 30ms
loss 7%
rate 500Kbps
-outgoing
delay 120ms
delay-distro 30ms
loss 7%
rate 250Kbps
```

**Dial-up Profiles with Jitter:**

Good Dial-up with Jitter:

```md
-incoming
delay 100ms
delay-distro 25ms
loss 2%
rate 2Mbps
-outgoing
delay 100ms
delay-distro 25ms
loss 2%
rate 1Mbps
```

Medium Dial-up with Jitter:

```md
-incoming
delay 200ms
delay-distro 50ms
loss 4%
rate 1Mbps
-outgoing
delay 200ms
delay-distro 50ms
loss 4%
rate 500Kbps
```

Poor Dial-up with Jitter:

```md
-incoming
delay 300ms
delay-distro 75ms
loss 6%
rate 500Kbps
-outgoing
delay 300ms
delay-distro 75ms
loss 6%
rate 250Kbps
```

**Wi-Fi Profiles with Jitter:**

Good Wi-Fi with Jitter:

```md
-incoming
delay 10ms
delay-distro 2ms
loss 0%
rate 10Mbps
-outgoing
delay 10ms
delay-distro 2ms
loss 0%
rate 5Mbps
```

Medium Wi-Fi with Jitter:

```md
-incoming
delay 20ms
delay-distro 5ms
loss 1%
rate 5Mbps
-outgoing
delay 20ms
delay-distro 5ms
loss 1%
rate 2.5Mbps
```

Poor Wi-Fi with Jitter:

```md
-incoming
delay 30ms
delay-distro 7ms
loss 2%
rate 2.5Mbps
-outgoing
delay 30ms
delay-distro 7ms
loss 2%
rate 1.25Mbps
```

**Satellite Profiles with Jitter:**

Good Satellite with Jitter:

```md
-incoming
delay 600ms
delay-distro 150ms
loss 0%
rate 1Mbps


-outgoing
delay 600ms
delay-distro 150ms
loss 0%
rate 500Kbps
```

Medium Satellite with Jitter:

```md
-incoming
delay 800ms
delay-distro 200ms
loss 1%
rate 500Kbps
-outgoing
delay 800ms
delay-distro 200ms
loss 1%
rate 250Kbps
```

Poor Satellite with Jitter:

```md
-incoming
delay 1000ms
delay-distro 250ms
loss 2%
rate 250Kbps
-outgoing
delay 1000ms
delay-distro 250ms
loss 2%
rate 125Kbps
```
