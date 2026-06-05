from flask import Flask, jsonify, request, render_template
import pandas as pd
import numpy as np
from skyfield.api import load, EarthSatellite
from sgp4.api import Satrec
from datetime import datetime, timezone
import os

app = Flask(__name__)
ts = load.timescale()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
main_sat_df = pd.read_csv(os.path.join(BASE_DIR, 'Collision', 'main satellite.txt'))
tle_df = pd.read_csv(os.path.join(BASE_DIR, 'Tracking', 'combined_tle_dataset.csv'))


def make_main_satellite():
    row = main_sat_df.iloc[0]
    epoch_dt = datetime.fromisoformat(row['EPOCH']).replace(tzinfo=timezone.utc)
    j2000 = datetime(2000, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
    jd = 2451545.0 + (epoch_dt - j2000).total_seconds() / 86400.0
    satrec = Satrec()
    satrec.sgp4init(
        0, 'i',
        int(row['NORAD_CAT_ID']),
        jd - 2433281.5,
        float(row['BSTAR']),
        float(row['MEAN_MOTION_DOT']),
        float(row['MEAN_MOTION_DDOT']),
        float(row['ECCENTRICITY']),
        np.radians(float(row['ARG_OF_PERICENTER'])),
        np.radians(float(row['INCLINATION'])),
        np.radians(float(row['MEAN_ANOMALY'])),
        float(row['MEAN_MOTION']) * 2 * np.pi / 1440.0,
        np.radians(float(row['RA_OF_ASC_NODE']))
    )
    return EarthSatellite.from_satrec(satrec, ts)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/simulation')
def simulation():
    debris_count = max(1, min(int(request.args.get('debris_count', 10)), len(tle_df)))
    threshold = max(10.0, min(float(request.args.get('threshold', 1000)), 10000.0))

    main_sat = make_main_satellite()
    main_name = str(main_sat_df.iloc[0]['OBJECT_NAME'])

    # Proportional stratified random sample across all three debris sources
    source_counts = tle_df['source'].value_counts()
    total_available = len(tle_df)
    sampled_frames = []
    remaining = debris_count
    sources = source_counts.index.tolist()
    for i, src in enumerate(sources):
        src_df = tle_df[tle_df['source'] == src]
        is_last = (i == len(sources) - 1)
        n = remaining if is_last else round(debris_count * len(src_df) / total_available)
        n = min(n, len(src_df))
        sampled_frames.append(src_df.sample(n=n, random_state=None))
        remaining -= n
        if remaining <= 0:
            break
    selected = pd.concat(sampled_frames).sample(frac=1).reset_index(drop=True)  # shuffle

    # Compute timesteps to cover one full orbit of the slowest object (longest period)
    main_period_min = 1440.0 / float(main_sat_df.iloc[0]['MEAN_MOTION'])
    debris_periods = []
    for _, row in selected.iterrows():
        try:
            debris_periods.append(1440.0 / float(row['line2'][52:63]))
        except Exception:
            debris_periods.append(110.0)
    n_steps = int(max([main_period_min] + debris_periods)) + 3

    times = ts.utc(2026, 5, 15, 5, range(0, n_steps))
    timestamp_list = [t.utc_iso() for t in times]

    main_positions = []
    for t in times:
        pos = main_sat.at(t).position.km
        main_positions.append([round(float(pos[0]), 2), round(float(pos[1]), 2), round(float(pos[2]), 2)])

    debris_list = []
    total_collision_events = 0

    for _, row in selected.iterrows():
        try:
            sat = EarthSatellite(row['line1'], row['line2'], str(row['object_id']), ts)
            positions = []
            collision_risks = []
            min_dist = float('inf')

            for i, t in enumerate(times):
                pos = sat.at(t).position.km
                p = [round(float(pos[0]), 2), round(float(pos[1]), 2), round(float(pos[2]), 2)]
                positions.append(p)

                mp = main_positions[i]
                dist = float(np.sqrt((p[0]-mp[0])**2 + (p[1]-mp[1])**2 + (p[2]-mp[2])**2))
                min_dist = min(min_dist, dist)

                if dist < threshold:
                    collision_risks.append({'time_index': i, 'distance_km': round(dist, 2)})
                    total_collision_events += 1

            debris_list.append({
                'object_id': str(row['object_id']),
                'source': str(row['source']),
                'positions': positions,
                'collision_risks': collision_risks,
                'min_distance_km': round(min_dist, 2)
            })
        except Exception:
            continue

    debris_at_risk = sum(1 for d in debris_list if d['collision_risks'])
    min_overall = min((d['min_distance_km'] for d in debris_list), default=None)

    return jsonify({
        'timestamps': timestamp_list,
        'main_satellite': {'name': main_name, 'positions': main_positions},
        'debris': debris_list,
        'total_collision_events': total_collision_events,
        'debris_at_risk': debris_at_risk,
        'min_distance_km': round(min_overall, 2) if min_overall is not None else None,
        'threshold': threshold,
        'debris_count': len(debris_list)
    })


if __name__ == '__main__':
    app.run(debug=True, port=5000)
