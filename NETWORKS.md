Each configs contains 2 blocks '-incoming' and '-outgoing' in your config.txt file you should use this keys or leave it empty at all ( In the windows systems )

in each config you can just remove `delay-distro` to have natural config ( delay-distro = jitter )

**5G Profiles**

Ultra-Low Latency 5G:
```md
-incoming
delay 1ms
loss 0%
rate 1000Mbps
-outgoing
delay 1ms
loss 0%
rate 500Mbps
```
High-Speed 5G:
```md
-incoming
delay 10ms
loss 0%
rate 800Mbps
-outgoing
delay 10ms
loss 0%
rate 400Mbps
```
Standard 5G:
```md
-incoming
delay 20ms
loss 0.1%
rate 300Mbps
-outgoing
delay 20ms
loss 0.1%
rate 150Mbps
```
Reduced Speed 5G:
```md
-incoming
delay 30ms
loss 0.5%
rate 100Mbps
-outgoing
delay 30ms
loss 0.5%
rate 50Mbps
```

Congested 5G:
```md
-incoming
delay 50ms
loss 1%
rate 50Mbps
-outgoing
delay 50ms
loss 1%
rate 25Mbps
```


Good 5G with Jitter:

```md
-incoming
delay 10ms
delay-distro 2ms
loss 0%
rate 100Mbps
-outgoing
delay 10ms
delay-distro 2ms
loss 0%
rate 50Mbps
```

Medium 5G with Jitter:

```
-incoming
delay 20ms
delay-distro 5ms
loss 0.5%
rate 50Mbps
-outgoing
delay 20ms
delay-distro 5ms
loss 0.5%
rate 25Mbps
```

Poor 5G with Jitter:

```
-incoming
delay 40ms
delay-distro 10ms
loss 1%
rate 25Mbps
-outgoing
delay 40ms
delay-distro 10ms
loss 1%
rate 12.5Mbps
```

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

## Custom Profiles

High Delay:
```md
-incoming
delay 500ms
delay-distro 5ms
loss 0%
rate 10Mbps
-outgoing
delay 500ms
delay-distro 5ms
loss 0%
rate 5Mbps
```

High Jitter:
```md
-incoming
delay 30ms
delay-distro 100ms
loss 0%
rate 10Mbps
-outgoing
delay 30ms
delay-distro 100ms
loss 0%
rate 5Mbps
```

High Loss:
```md
-incoming
delay 30ms
delay-distro 10ms
loss 20%
rate 10Mbps
-outgoing
delay 30ms
delay-distro 10ms
loss 20%
rate 5Mbps
```

Low Rate:
```md
-incoming
delay 30ms
delay-distro 10ms
loss 5%
rate 100Kbps
-outgoing
delay 30ms
delay-distro 10ms
loss 5%
rate 50Kbps
```

**Custom 1**

Poor Network with High Jitter and Loss:

```md
-incoming
delay 100ms
delay-distro 40ms
loss 15%
rate 500Kbps
-outgoing
delay 100ms
delay-distro 40ms
loss 15%
rate 250Kbps
```

**Custom 2**

Medium Network with Moderate Jitter and Loss:

```md
-incoming
delay 50ms
delay-distro 20ms
loss 5%
rate 2Mbps
-outgoing
delay 50ms
delay-distro 20ms
loss 5%
rate 1Mbps
```

**Custom 3**

Medium Network with Higher Jitter and Loss:

```md
-incoming
delay 70ms
delay-distro 25ms
loss 15%
rate 1.5Mbps
-outgoing
delay 70ms
delay-distro 25ms
loss 15%
rate 750Kbps
```

**Custom 4**

Network with Variable Jitter and Loss:
```md
-incoming
delay 70ms
delay-distro 10ms
loss 5%
rate 1.8Mbps
-outgoing
delay 70ms
delay-distro 10ms
loss 5%
rate 900Kbps
```

**Custom 5**

Chaotic Network with High Jitter and Variable Loss:
```md
-incoming
delay 70ms
delay-distro 40ms
loss 15%
rate 900Kbps
-outgoing
delay 70ms
delay-distro 40ms
loss 15%
rate 450Kbps
```

**Custom 6**

Random Network with Periodic Jitter and Loss:
```md
-incoming
delay 80ms
delay-distro 10ms
loss 8%
rate 1.2Mbps
-outgoing
delay 80ms
delay-distro 10ms
loss 8%
rate 600Kbps
```

**Custom 7**

Fluctuating Network with Oscillating Jitter and Loss:
```md
-incoming
delay 60ms
delay-distro 30ms
loss 10%
rate 1.5Mbps
-outgoing
delay 60ms
delay-distro 30ms
loss 10%
rate 750Kbps
```

**Custom 8**

Unpredictable Network with Rapid Jitter and Loss:

```md
-incoming
delay 40ms
delay-distro 5ms
loss 6%
rate 2.5Mbps
-outgoing
delay 40ms
delay-distro 5ms
loss 6%
rate 1.25Mbps
```

**Custom 9**

Variable Network with Sudden Jitter Spikes and Loss:

```md
-incoming
delay 60ms
delay-distro 20ms
loss 10%
rate 1.8Mbps
-outgoing
delay 60ms
delay-distro 20ms
loss 10%
rate 900Kbps
```
**Custom 10**

Intermittent Network with Periodic Outages and Recovery:

```md
-incoming
delay 80ms
delay-distro 10ms
loss 8%
rate 1.2Mbps
-outgoing
delay 80ms
delay-distro 10ms
loss 8%
rate 600Kbps
```


**Custom 11**

Pulsating Network with Pulsed Jitter and Loss:

```md
-incoming
delay 50ms
delay-distro 15ms
loss 7%
rate 1.5Mbps
-outgoing
delay 50ms
delay-distro 15ms
loss 7%
rate 750Kbps
```

**Custom 12**

Stochastic Network with Randomized Jitter and Loss:

```md
-incoming
delay 70ms
delay-distro 25ms
loss 12%
rate 1.2Mbps
-outgoing
delay 70ms
delay-distro 25ms
loss 12%
rate 600Kbps
```


**Custom 13**

Wave-like Network with Wavy Jitter and Loss:

```md
-incoming
delay 60ms
delay-distro 30ms
loss 10%
rate 1.8Mbps
-outgoing
delay 60ms
delay-distro 30ms
loss 10%
rate 900Kbps
```


**Custom 14**

Chaotic Network with Intermittent Jitter and Loss:

```md
-incoming
delay 60ms
delay-distro 20ms
loss 15%
rate 1.5Mbps
-outgoing
delay 60ms
delay-distro 20ms
loss 15%
rate 750Kbps
```

**Custom 15**

Bursty Network with Burst Jitter and Loss:

```md
-incoming
delay 40ms
delay-distro 5ms
loss 8%
rate 2Mbps
-outgoing
delay 40ms
delay-distro 5ms
loss 8%
rate 1Mbps
```

**Custom 16**
Ephemeral Network with Flickering Jitter and Loss:

```md
-incoming
delay 70ms
delay-distro 15ms
loss 12%
rate 1.2Mbps
-outgoing
delay 70ms
delay-distro 15ms
loss 12%
rate 600Kbps
```


