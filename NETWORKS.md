Each Configs Contains 2 blocks '-incoming' and '-outgoing' in your config.txt file you should use this keys or leave it empty at all ( In windows systems )

**4G Profiles:**

Good 4G:

```md
-incoming
delay 20ms
loss 0%
rate 10Mbps
-outgoing
delay 20ms
loss 0%
rate 5Mbps
```

Medium 4G:

```md
-incoming
delay 40ms
loss 1%
rate 5Mbps
-outgoing
delay 40ms
loss 1%
rate 2.5Mbps
```

Poor 4G:

```md
-incoming
delay 60ms
loss 2%
rate 2.5Mbps
-outgoing
delay 60ms
loss 2%
rate 1.25Mbps
```

**3G Profiles:**

Good 3G:

```md
-incoming
delay 30ms
loss 0%
rate 1Mbps
-outgoing
delay 30ms
loss 0%
rate 500Kbps
```

Medium 3G:

```md
-incoming
delay 60ms
loss 1%
rate 500Kbps
-outgoing
delay 60ms
loss 1%
rate 250Kbps
```

Poor 3G:

```md
-incoming
delay 90ms
loss 2%
rate 250Kbps
-outgoing
delay 90ms
loss 2%
rate 125Kbps
```

**2G Profiles:**

Good 2G:

```md
-incoming
delay 100ms
loss 0%
rate 200Kbps
-outgoing
delay 100ms
loss 0%
rate 100Kbps
```

Medium 2G:

```md
-incoming
delay 200ms
loss 1%
rate 100Kbps
-outgoing
delay 200ms
loss 1%
rate 50Kbps
```

Poor 2G:

```md
-incoming
delay 300ms
loss 2%
rate 50Kbps
-outgoing
delay 300ms
loss 2%
rate 25Kbps
```

**Wi-Fi Profiles:**

Good Wi-Fi:

```md
-incoming
delay 10ms
loss 0%
rate 10Mbps
-outgoing
delay 10ms
loss 0%
rate 5Mbps
```

Medium Wi-Fi:

```md
-incoming
delay 20ms
loss 1%
rate 5Mbps
-outgoing
delay 20ms
loss 1%
rate 2.5Mbps
```

Poor Wi-Fi:

```md
-incoming
delay 30ms
loss 2%
rate 2.5Mbps
-outgoing
delay 30ms
loss 2%
rate 1.25Mbps
```

**Dial-up Profiles:**

Good Dial-up:

```md
-incoming
delay 300ms
loss 0%
rate 100Kbps
-outgoing
delay 300ms
loss 0%
rate 50Kbps
```

Medium Dial-up:

```md
-incoming
delay 500ms
loss 1%
rate 50Kbps
-outgoing
delay 500ms
loss 1%
rate 25Kbps
```

Poor Dial-up:

```md
-incoming
delay 700ms
loss 2%
rate 25Kbps
-outgoing
delay 700ms
loss 2%
rate 12.5Kbps
```

**Satellite Profiles:**

Good Satellite:

```md
-incoming
delay 600ms
loss 0%
rate 1Mbps
-outgoing
delay 600ms
loss 0%
rate 500Kbps
```

Medium Satellite:

```md
-incoming
delay 800ms
loss 1%
rate 500Kbps
-outgoing
delay 800ms
loss 1%
rate 250Kbps
```

Poor Satellite:

```md
-incoming
delay 1000ms
loss 2%
rate 250Kbps
-outgoing
delay 1000ms
loss 2%
rate 125Kbps
```


**Poor 4G with Custom Loss:**

```md
-incoming
delay 60ms
loss 10%
rate 2Mbps
-outgoing
delay 60ms
loss 10%
rate 1Mbps
```

**Poor 3G with Custom Loss:**

```md
-incoming
delay 80ms
loss 15%
rate 1Mbps
-outgoing
delay 80ms
loss 15%
rate 500Kbps
```

**Medium 4G with Custom Loss:**

```md
-incoming
delay 40ms
loss 5%
rate 5Mbps
-outgoing
delay 40ms
loss 5%
rate 2.5Mbps
```

**Wi-Fi with Custom Loss:**

```md
-incoming
delay 30ms
loss 5%
rate 10Mbps
-outgoing
delay 30ms
loss 5%
rate 5Mbps
```

