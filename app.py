"""
AquaPure – Local Development Server
Serves static files from public/ for local testing.

For production: deploy to Vercel (see vercel.json).
No Python or server is needed in production — Vercel serves static HTML directly.

Usage:
    python app.py
    → Open http://localhost:5000
"""
from flask import Flask, send_from_directory
import os

app = Flask(__name__, static_folder='public')

@app.route('/')
def index():
    return send_from_directory('public', 'index.html')

@app.route('/tool')
def tool():
    return send_from_directory('public', 'tool.html')

@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory('public', filename)

def analyze_water(data):
    results = {}
    is_safe = True
    warnings = []
    recs = []

    # pH Analysis
    ph = float(data.get('ph', 0))
    if ph < 6.5:
        is_safe = False
        warnings.append(f"pH level ({ph}) is acidic (below 6.5).")
        recs.append("Add a pH Neutralizer or calcite filter to prevent pipe corrosion and metallic taste.")
    elif ph > 8.5:
        is_safe = False
        warnings.append(f"pH level ({ph}) is basic (above 8.5).")
        recs.append("Use a mild acid injection system or specialized ion exchange to lower alkalinity.")
    results['ph'] = {'value': ph, 'status': 'Safe' if 6.5 <= ph <= 8.5 else 'Unsafe'}

    # TDS Analysis
    tds = float(data.get('tds', 0))
    if tds > 1000:
        is_safe = False
        warnings.append(f"High TDS ({tds} mg/L) detected.")
        recs.append("Install an Reverse Osmosis (RO) system to remove dissolved solids, heavy metals, and salts.")
    elif tds > 500:
        warnings.append(f"TDS level ({tds} mg/L) is acceptable but slightly above ideal.")
        recs.append("Consider a basic activated carbon filter to improve taste.")
    results['tds'] = {'value': tds, 'status': 'Safe' if tds <= 1000 else 'Unsafe'}

    # Turbidity Analysis
    turbidity = float(data.get('turbidity', 0))
    if turbidity > 5:
        is_safe = False
        warnings.append(f"High Turbidity ({turbidity} NTU) makes water cloudy.")
        recs.append("Use a Sediment Filter (5-micron) or a Flocculation system to remove suspended particles.")
    results['turbidity'] = {'value': turbidity, 'status': 'Safe' if turbidity <= 5 else 'Unsafe'}

    # Hardness Analysis
    hardness = float(data.get('hardness', 0))
    if hardness > 300:
        is_safe = False
        warnings.append(f"Hardness ({hardness} mg/L) is high.")
        recs.append("Install a Water Softener (Ion Exchange) to prevent scale buildup in appliances and improve lather.")
    results['hardness'] = {'value': hardness, 'status': 'Safe' if hardness <= 300 else 'Unsafe'}

    if is_safe and not recs:
        final_rec = "Your water meets all major safety standards. No immediate action required."
    else:
        final_rec = " | ".join(recs) if recs else "Water is safe but could be improved."

    return {
        'is_safe': is_safe,
        'results': results,
        'warnings': warnings,
        'recommendation': final_rec
    }

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f'\n  AquaPure dev server running at http://localhost:{port}\n')
    app.run(debug=True, port=port)
