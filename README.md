# IMU-EXTRACT

This script(s) process the raw input from different IMU devices.

---

## SOMI (IMU data as MIDI)

#### Usage:

Activate venv

```python
source .venv/bin/activate
```

Run main script:

```python
python IMUEXTRACT.py
```

Plot it :

```python
python combine_plot.py
```

Both the resulting `CC-combined.csv` and the plot `CC-combined.png` will be stored in the folder `OUTPUT/`.

---

### Open questions

- How do I find out the `max_datapoint` in general?

- Is it a problem that I don't have data for ALL the timestamp values? should I resample it to the same sampling as MPIPE or AUDIO

---

### To-Do

[Trello](https://trello.com/b/eNrZMJnA/salta-segmentation-app)