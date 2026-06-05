import pandas as pd

def load_tle_file(file_path, prefix, source):
    objects = []
    
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    lines = [l.strip() for l in lines if l.strip() != ""]
    
    assert len(lines) % 2 == 0, "TLE format error"

    count = 1
    
    for i in range(0, len(lines), 2):
        line1 = lines[i]
        line2 = lines[i+1]
        
        obj_id = f"{prefix}_{count:03d}"
        
        objects.append({
            "object_id": obj_id,
            "line1": line1,
            "line2": line2,
            "source": source
        })
        
        count += 1
    
    return objects


fy1c = load_tle_file("fengyun.txt", "FY1C", "Fengyun-1C")
ir33 = load_tle_file("iridium.txt", "IR33", "Iridium-33")
cosmos = load_tle_file("cosmos.txt", "COS2251", "Cosmos-2251")

master_dataset = fy1c + ir33 + cosmos

df = pd.DataFrame(master_dataset)
df.to_csv("combined_tle_dataset.csv", index=False)

print("✅ Dataset created!")